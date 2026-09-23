# Data Specification

> **Canonical Pipeline Specification**: For the single source of truth on all dataset acquisition, physical storage, preprocessing, feature engineering, model training, evaluation, artifact generation, model versioning, and inference, refer to [DATA_ML_PIPELINE.md](file:///d:/finguard/finguard-skill/data/DATA_ML_PIPELINE.md).

## Entity model
User, Role, Account, Transaction, Vendor, Beneficiary, Device, Location, Alert, RiskScore, Investigation, InvestigationNote, ModelPrediction, ModelVersion, RuleVersion, Document, DocumentChunk, AuditLog.

## Transaction fields
transaction_id, account_id, amount, currency, transaction_type, timestamp, channel, beneficiary_id, vendor_id, device_id, location_id, status, ingestion_id, created_at, updated_at.

## Prediction fields
fraud_probability, anomaly_score, rule_score, final_risk_score, risk_level, model_version, feature_version, score_version, explanation_version, predicted_at.

## Data quality & Integrity
- Validate required fields and data types.
- Normalize timestamps (elapsed relative timedelta `TransactionDT`) and currencies.
- Deduplicate by stable transaction identifier/idempotency key.
- Isolate malformed records and record data-quality events.
- Raw datasets are strictly immutable and never committed to Git.
- Clearly label synthetic/demo data (`backend/data/samples/demo/`) and never use demo data for real model training performance claims.

## Physical Dataset Layout
- Raw Data: `backend/data/raw/` (`ieee_cis/`, `ulb_credit_card/`)
- Processed Data: `backend/data/processed/` (`ieee_cis/` train/validation/test parquet partitions)
- Feature Matrices: `ml-backend/data/features/` (`train/`, `validation/`, `test/`)
- Demo Scenarios: `backend/data/samples/demo/`
