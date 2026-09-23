# Observability Specification

## Logs
Use structured logs with:
- timestamp
- service
- severity
- request ID
- user/actor ID where appropriate
- operation
- duration
- outcome

Never log tokens, secrets, full sensitive payment credentials, or raw private customer payloads by default.

## Metrics
Application: request rate, error rate, latency.
ML: inference count, latency, score distribution, model version.
Alerts: alert creation latency, active alerts, resolution time.
AI: request count, latency, retrieval count, failure rate.

## Tracing
Carry a request/trace ID across frontend -> backend -> ML/RAG services.

## Health
Each service provides liveness and readiness checks. Readiness must fail when required dependencies are unavailable.
