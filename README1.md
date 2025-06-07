# 🧠 Identity Reconciliation API

This is a FastAPI backend service that identifies and links customers by email and/or phone number, maintaining a single unified customer identity.

---

## 🔢 Seeding the Database

This project includes a `seed_data.py` script to pre-populate the database with sample contact entries. This is helpful for initial testing without manual data entry.

### What it does:
- Adds realistic contact entries with both `primary` and `secondary` linkages.
- Useful for quickly testing the behavior of the `/identify` endpoint.

---

## 🚀 How to Run

Before seeding the data, ensure:

1. Your PostgreSQL (or SQLite) database is set up.
2. Tables are created using the SQLAlchemy models.
3. The `.env` file or `database.py` is correctly configured to point to your database.

### Seed the database:

```bash
python seed_data.py


---

## 📍 API Endpoint

### **POST** `/identify`

This endpoint accepts an email and/or phone number, and returns a unified identity based on existing records.

---

## 🌐 Hosted Endpoint

The API is live at:

🔗 **Base URL**: [https://identity-reconciliation-api-e3y9.onrender.com](https://identity-reconciliation-api-e3y9.onrender.com)

Full endpoint URL:


