# Identity Reconciliation API

This is a FastAPI backend service that identifies and links customers by email/phone, maintaining a single customer identity.

## Endpoint

**POST** `/identify`

### Request Body (JSON)
```json
{
  "email": "test@example.com",
  "phoneNumber": "0123456789"
}
