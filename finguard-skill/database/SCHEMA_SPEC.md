# Database Specification

## PostgreSQL
Use PostgreSQL as the system of record.

## Core tables
- users
- roles
- user_roles
- accounts
- vendors
- beneficiaries
- devices
- locations
- transactions
- model_versions
- model_predictions
- risk_scores
- alerts
- investigations
- investigation_notes
- documents
- document_chunks
- audit_logs

## Principles
- UUID or similarly safe non-sequential public identifiers
- foreign keys and appropriate indexes
- created_at/updated_at on mutable domain entities
- status fields with explicit lifecycle values
- immutable audit rows
- database migrations through Alembic
- soft delete only where business requirements demand it
- use transactions for multi-table state transitions

## Important indexes
- transactions(account_id, timestamp)
- transactions(created_at)
- alerts(status, risk_level, created_at)
- investigations(status, updated_at)
- model_predictions(transaction_id, created_at)
- document_chunks on vector column plus metadata filters

## pgvector
Use pgvector for embeddings needed by the investigation knowledge base.
