from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import init_db, get_db
from models import Contact, get_or_create_contact
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS (for frontend/testing if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

class IdentifyRequest(BaseModel):
    email: str | None = None
    phoneNumber: str | None = None

@app.post("/identify")
def identify(payload: IdentifyRequest):
    if not payload.email and not payload.phoneNumber:
        raise HTTPException(status_code=400, detail="At least one of email or phoneNumber is required")

    db = get_db()
    contact_data = get_or_create_contact(db, payload.email, payload.phoneNumber)
    return {"contact": contact_data}
