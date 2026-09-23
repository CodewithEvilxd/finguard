# Security Specification

## Authentication
Use Supabase Auth or an equivalent managed identity provider.

## Authorization
RBAC is enforced server-side. Suggested roles: Admin, Risk Manager, Analyst, Viewer.

## Required controls
- TLS/HTTPS
- secure session handling
- JWT validation where used
- least-privilege service credentials
- secrets outside source control
- parameterized database access/ORM
- validation of all external input
- rate limiting on sensitive endpoints
- audit logging
- dependency and image scanning
- separate staging and production credentials

## Data handling
- only synthetic data in public demos
- redact sensitive values from logs
- never log authorization tokens or full payment credentials
- avoid unnecessary retention of sensitive data
- restrict access by role

## AI security
- prompt injection resistance for retrieved documents
- tool allow-list
- output schema validation
- no direct secret access from the LLM
- no autonomous irreversible financial actions
- log model/prompt/retrieval versions for traceability
