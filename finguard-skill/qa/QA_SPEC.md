# Quality Assurance Specification

## Unit tests
- feature calculations
- risk scoring
- rule evaluation
- API validators
- UI utilities

## Integration tests
- API + database
- backend + ML backend
- alert lifecycle
- RAG retrieval
- realtime event delivery

## End-to-end tests
Visitor landing page -> demo/login -> transaction ingestion -> risk prediction -> alert -> investigation -> analyst decision -> audit entry.

## ML validation
- reproducible training run
- preprocessing parity between training and inference
- model artifact checksum validation
- metric report linked to dataset/model versions
- threshold sensitivity analysis where relevant

## Acceptance criteria
- protected operations require authorization
- repeated idempotent ingestion does not duplicate state
- every prediction has model/feature/scoring version metadata
- supported alerts expose explanations
- AI assistant never fabricates unavailable transaction details
- analyst decisions create immutable audit entries
