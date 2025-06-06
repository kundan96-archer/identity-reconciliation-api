from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, or_
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime
import enum

Base = declarative_base()

class LinkPrecedence(str, enum.Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    phoneNumber = Column(String, nullable=True)
    email = Column(String, nullable=True)
    linkedId = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    linkPrecedence = Column(Enum(LinkPrecedence), default=LinkPrecedence.PRIMARY)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deletedAt = Column(DateTime, nullable=True)


#######
def get_or_create_contact(db: Session, email: str | None, phone: str | None):
    matched = db.query(Contact).filter(
        or_(Contact.email == email, Contact.phoneNumber == phone)
    ).all()

    if not matched:
        # New contact
        new = Contact(email=email, phoneNumber=phone, linkPrecedence=LinkPrecedence.PRIMARY)
        db.add(new)
        db.commit()
        db.refresh(new)
        return {
            "primaryContatctId": new.id,
            "emails": [new.email] if new.email else [],
            "phoneNumbers": [new.phoneNumber] if new.phoneNumber else [],
            "secondaryContactIds": []
        }

    # Identify all related contacts
    all_contacts = set(matched)
    to_check = list(matched)

    while to_check:
        contact = to_check.pop()
        if contact.linkPrecedence == LinkPrecedence.SECONDARY and contact.linkedId:
            related = db.query(Contact).filter(Contact.id == contact.linkedId).all()
        else:
            related = db.query(Contact).filter(Contact.linkedId == contact.id).all()
        for r in related:
            if r not in all_contacts:
                all_contacts.add(r)
                to_check.append(r)

    all_contacts = list(all_contacts)

    # Identify all primaries
    primaries = [c for c in all_contacts if c.linkPrecedence == LinkPrecedence.PRIMARY]

    # Select earliest primary
    true_primary = min(primaries, key=lambda c: c.createdAt)
    primary_id = true_primary.id

    # Rewire any other primary to become secondary
    for p in primaries:
        if p.id != primary_id:
            p.linkPrecedence = LinkPrecedence.SECONDARY
            p.linkedId = primary_id
            p.updatedAt = datetime.utcnow()
            db.add(p)

    # Update all secondaries to point to the true primary
    for c in all_contacts:
        if c.linkPrecedence == LinkPrecedence.SECONDARY and c.linkedId != primary_id:
            c.linkedId = primary_id
            c.updatedAt = datetime.utcnow()
            db.add(c)

    db.commit()

    # Check if contact exists already (partial match)
    existing = any(
        (email and c.email == email) or (phone and c.phoneNumber == phone)
        for c in all_contacts
    )

    if not existing:
        # Insert new secondary
        new_secondary = Contact(
            email=email, phoneNumber=phone, linkedId=primary_id, linkPrecedence=LinkPrecedence.SECONDARY
        )
        db.add(new_secondary)
        db.commit()
        db.refresh(new_secondary)
        all_contacts.append(new_secondary)

    # Build the response
    emails = list({c.email for c in all_contacts if c.email})
    phones = list({c.phoneNumber for c in all_contacts if c.phoneNumber})
    secondary_ids = [c.id for c in all_contacts if c.id != primary_id]

    return {
        "primaryContatctId": primary_id,
        "emails": emails,
        "phoneNumbers": phones,
        "secondaryContactIds": secondary_ids,
    }

