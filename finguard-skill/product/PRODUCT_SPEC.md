# Product Specification

## Product name
FinGuard AI

## Positioning
Explainable AI for financial fraud and anomaly detection.

## Primary users
- Financial/risk analysts
- Risk managers
- Compliance investigators
- Administrators

## Core user problem
Analysts need to identify suspicious activity from high-volume financial data, understand why an alert was produced, investigate related evidence, and record an accountable decision.

## Core capabilities
1. Transaction monitoring
2. Fraud classification
3. Unsupervised anomaly detection
4. Configurable rule checks
5. Unified risk score
6. Explainable risk factors
7. Real-time alerts
8. Investigation workspace
9. AI investigation assistant
10. Account/vendor intelligence
11. Audit trail
12. Analytics and reporting

## MVP
- Seeded or synthetic transaction data
- Transaction list/detail
- XGBoost or equivalent supervised model when labels exist
- Isolation Forest anomaly detector
- Rule engine
- Risk scoring service
- SHAP explanations
- Alert lifecycle
- Investigation workspace
- AI assistant with grounded retrieval
- PostgreSQL persistence
- Real-time alert refresh
- Landing interface at `/`

## Phase 2
- Graph relationships across accounts, devices, vendors, beneficiaries
- Advanced case analytics
- Model monitoring and drift detection
- Vendor risk intelligence
- Batch scoring
- scheduled reports

## Out of scope for initial build
- Automatic irreversible financial transactions
- Unsupervised blocking of customer accounts
- Claims of regulatory certification
- Real-world banking integration without explicit authorization and sandbox controls
