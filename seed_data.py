from sqlalchemy.orm import Session
from database import SessionLocal  # your DB session factory
from models import Contact
from datetime import datetime, timezone

def seed_data():
    db = SessionLocal()
    # Clear old data
    db.query(Contact).delete()
    db.commit()

    now = datetime.now(timezone.utc)  # timezone-aware current UTC time

    contacts = [
        Contact(
            phoneNumber="123456",
            email="lorraine@hillvalley.edu",
            linkPrecedence="primary",
            createdAt=now,
            updatedAt=now,
            deletedAt=None
        ),
        Contact(
            phoneNumber="234567",
            email="mcfly@hillvalley.edu",
            linkPrecedence="primary",
            linkedId=None,
            createdAt=now,
            updatedAt=now,
            deletedAt=None
        ),
    ]

    db.add_all(contacts)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_data()
