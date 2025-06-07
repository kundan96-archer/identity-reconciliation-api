# Identity Reconciliation API

This is a FastAPI backend service that identifies and links customers by email/phone, maintaining a single customer identity.

## 🔢 Seeding the Database

This project includes a `seed_data.py` script to pre-populate the database with sample contact entries. This helps with initial testing of the API without manually inserting data.

# 📦 What it does
- Adds realistic contact entries with both `primary` and `secondary` linkages.
- Useful for quickly testing the `/identify` endpoint behavior.

## 🚀 How to Run

Before you seed the data, ensure:
1. Your PostgreSQL (or SQLite) database is set up and the tables are created using the models.
2. The `.env` file or `database.py` is correctly pointing to your local database.

Then run the script before connecting to endpoint API:

```bash
python seed_data.py


### Endpoint

**POST** `/identify`

#### Request Body (JSON)
```json
{
  "email": "test@example.com",
  "phoneNumber": "0123456789"
}

## Hosted Endpoint

The `/identify` API endpoint is live at:

🔗 https://your-app-name.onrender.com/identify

📝 **Request Type**: POST  
📦 **Request Body**: JSON (not form-data)

### Example Payload:
```json
{
  "email": "mcfly@hillvalley.edu",
  "phoneNumber": "123456"
}

