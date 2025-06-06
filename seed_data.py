# seed_data.py
from database import SessionLocal, engine
from models import Base, Contact
from datetime import datetime

# Create the database tables
Base.metadata.create_all(bind=engine)

# Create a session
db = SessionLocal()

# Sample contact data
contacts = [
    Contact(
        phoneNumber="123456",
        email="lorraine@hillvalley.edu",
        linkPrecedence="primary",
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow(),
    ),
    Contact(
        phoneNumber="123456",
        email="mcfly@hillvalley.edu",
        linkPrecedence="secondary",
        linkedId=1,
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow(),
    ),
]

# Add and commit contacts
db.add_all(contacts)
db.commit()
db.close()

print("✅ Sample contacts added.")
