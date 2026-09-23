# Product Acceptance Criteria

## Landing
A new visitor understands the problem, product value, detection/explainability flow, and can enter demo or sign in without seeing the operational dashboard as the first screen.

## Detection
Given a valid transaction, the system returns a prediction record with versioned metadata and risk score. If models are unavailable, the system fails safely with a clear state.

## Alerting
A high-risk score according to the active configuration creates one alert. Reprocessing the same transaction idempotently must not create duplicates.

## Explanation
Supported model outputs include top risk factors and enough context for an analyst to understand the decision signal without reading raw model internals.

## Investigation
An analyst can inspect transaction facts, related activity, risk factors, and relevant approved documents in one workspace.

## AI assistant
The assistant answers from retrieved context, identifies missing information, and never invents transaction details.

## Decision
An authorized analyst can clear, review, confirm suspicious activity, or escalate according to configured workflow. Each decision is audited.

## Reliability
The application has meaningful loading, empty, error, and unavailable-service states.
