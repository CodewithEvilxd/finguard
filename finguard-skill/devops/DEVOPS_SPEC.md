# DevOps Specification

## Environment model
- local
- staging
- production

Each environment must have independent configuration and credentials.

## Local development
Docker Compose should provide PostgreSQL + pgvector and optional supporting services.

## CI
1. dependency install
2. formatting/lint
3. frontend typecheck
4. backend tests
5. ML tests
6. integration tests
7. security/dependency scan
8. frontend production build
9. container build

## Deployment
Frontend: Vercel or equivalent.
Backend: container deployment such as Railway, Render, AWS, or equivalent.
ML backend: independently deployed container or colocated with backend only if resource and scaling requirements remain small.
Database: managed PostgreSQL with pgvector.

## Observability
Structured JSON logs, request IDs, health/readiness endpoints, error tracking, latency monitoring, model inference latency, alert creation latency, and AI request latency.

## Release practice
Use semantic versioning where practical, migration checks, rollback notes, and a release checklist before production deployment.
