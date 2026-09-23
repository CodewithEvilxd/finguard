# Backend Specification

## Framework
FastAPI + Pydantic + SQLAlchemy/SQLModel + Alembic.

## Domain modules
- auth
- users
- transactions
- accounts
- vendors
- beneficiaries
- devices
- alerts
- investigations
- analytics
- reports
- audit
- ai_assistant

## API rules
- version APIs under `/api/v1`
- validate every request and response
- pagination for collection endpoints
- stable error envelope
- consistent status codes
- idempotency keys for ingest endpoints
- request IDs in logs and responses
- authorization enforced server-side

## Suggested endpoints
POST `/api/v1/transactions`
GET `/api/v1/transactions`
GET `/api/v1/transactions/{id}`
GET `/api/v1/alerts`
GET `/api/v1/alerts/{id}`
PATCH `/api/v1/alerts/{id}`
POST `/api/v1/investigations`
GET `/api/v1/investigations/{id}`
POST `/api/v1/assistant/query`
GET `/api/v1/accounts/{id}/risk`
GET `/api/v1/analytics/overview`
GET `/api/v1/health`
GET `/api/v1/ready`

## Error contract
Return machine-readable code, human-readable message, request ID, and optional field errors. Never leak stack traces to clients.
