# System Architecture

## Target topology

Browser -> Next.js frontend -> FastAPI backend -> PostgreSQL
                                      |-> ML backend
                                      |-> RAG/AI layer
                                      |-> Realtime channel

## Responsibilities
### Frontend
- App routing
- UI state
- accessibility
- data visualization
- API client
- auth/session UI
- investigation UX

### Backend
- domain logic
- auth/authorization enforcement
- transaction ingestion
- alert lifecycle
- investigation records
- AI orchestration
- audit log
- database access

### ML backend
- feature transformation
- model inference
- anomaly detection
- risk scoring
- SHAP explanations
- model metadata and health

### RAG/AI layer
- knowledge ingestion
- retrieval
- context assembly
- LLM invocation
- structured answer generation
- source references

## Data flow
Transaction -> validation -> normalization -> feature generation -> models/rules -> risk score -> explanation -> alert -> investigation context -> human action -> audit.

## Reliability principles
- idempotent transaction ingestion
- deterministic feature computation for the same input/version
- model version attached to every prediction
- trace/request ID across services
- timeouts on network calls
- retries only for safe/idempotent calls
- graceful degradation when LLM is unavailable
- database transactions around state changes
