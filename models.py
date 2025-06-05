from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, or_
from sqlalchemy.orm import declarative_base, Session
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

    # Gather all related contacts
    contact_ids = set()
    for m in matched:
        if m.linkPrecedence == LinkPrecedence.PRIMARY:
            contact_ids.add(m.id)
        elif m.linkedId:
            contact_ids.add(m.linkedId)

    primary_id = min(contact_ids)
    all_related = db.query(Contact).filter(
        (Contact.id == primary_id) | (Contact.linkedId == primary_id)
    ).all()

    emails = []
    phones = []
    secondary_ids = []

    for contact in all_related:
        if contact.email and contact.email not in emails:
            emails.append(contact.email)
        if contact.phoneNumber and contact.phoneNumber not in phones:
            phones.append(contact.phoneNumber)
        if contact.id != primary_id:
            secondary_ids.append(contact.id)

    # Add new secondary if info not matched
    existing = any(c.email == email and c.phoneNumber == phone for c in all_related)
    if not existing:
        new_secondary = Contact(
            email=email, phoneNumber=phone, linkedId=primary_id, linkPrecedence=LinkPrecedence.SECONDARY
        )
        db.add(new_secondary)
        db.commit()
        db.refresh(new_secondary)
        secondary_ids.append(new_secondary.id)
        if new_secondary.email and new_secondary.email not in emails:
            emails.append(new_secondary.email)
        if new_secondary.phoneNumber and new_secondary.phoneNumber not in phones:
            phones.append(new_secondary.phoneNumber)

    return {
        "primaryContatctId": primary_id,
        "emails": emails,
        "phoneNumbers": phones,
        "secondaryContactIds": secondary_ids,
    }
