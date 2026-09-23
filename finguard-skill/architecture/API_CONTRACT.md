# API Contract

## Versioning
All public application APIs live under `/api/v1`.

## Response conventions
Collection endpoints support pagination and filtering. Errors return a stable machine-readable code, message, request ID, and optional field errors.

## Transaction APIs
POST `/api/v1/transactions`
GET `/api/v1/transactions`
GET `/api/v1/transactions/{id}`

## Alert APIs
GET `/api/v1/alerts`
GET `/api/v1/alerts/{id}`
PATCH `/api/v1/alerts/{id}`

## Investigation APIs
POST `/api/v1/investigations`
GET `/api/v1/investigations/{id}`
POST `/api/v1/investigations/{id}/decision`

## AI APIs
POST `/api/v1/assistant/query`
POST `/api/v1/explanations/{transaction_id}`

## Analytics APIs
GET `/api/v1/analytics/overview`
GET `/api/v1/analytics/risk-trend`

## Health
GET `/api/v1/health`
GET `/api/v1/ready`

## API standards
Use OpenAPI generated from FastAPI schemas. Treat the generated contract as a source for frontend client types.
