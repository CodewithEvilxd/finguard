# ML Backend Specification

> **Canonical Data & ML Pipeline Document**: The single source of truth for end-to-end dataset acquisition, storage, preprocessing, 17-dimensional feature engineering, model training, evaluation reports, model registry, explainability, and inference contracts is [DATA_ML_PIPELINE.md](file:///d:/finguard/finguard-skill/data/DATA_ML_PIPELINE.md).

## Scope
The ML backend is an independently deployable FastAPI Python service (`ml-backend:8001`) responsible for feature computation, model inference, anomaly detection, deterministic risk rules, and TreeSHAP explainability artifacts.

## Detection strategy
Use a hybrid detection stack:
1. Supervised XGBoost Booster (`ml-backend/models/xgboost/v1/model.json`) trained on out-of-time IEEE-CIS fraud distributions.
2. Isolation Forest (`ml-backend/models/isolation-forest/v1/model.joblib`) for unsupervised behavioral anomaly scoring.
3. Configurable deterministic rules (`RuleEngine`) for high-velocity, high-amount, corridor, and night-time wire transfers.

## Physical Directory Architecture
- Processed Data: `ml-backend/data/processed/`
- Feature Matrices: `ml-backend/data/features/` (`train/`, `validation/`, `test/`)
- Manifests: `ml-backend/data/manifests/`
- Preprocessing: `ml-backend/training/preprocessing/`
- Training Pipelines: `ml-backend/training/pipelines/`
- Experiments: `ml-backend/training/experiments/`
- Evaluation: `ml-backend/training/evaluation/`
- Reports: `ml-backend/training/reports/`
- XGBoost Models: `ml-backend/models/xgboost/`
- Isolation Forest Models: `ml-backend/models/isolation-forest/`
- Model Registry: `ml-backend/models/registry/`
- Artifacts: `ml-backend/artifacts/`

## Feature Groups (17 Dimensions)
- Monetary: `amount_log`
- Temporal: `hour_of_day`, `day_of_week`, `is_night`, `is_weekend` (derived from relative timedelta `TransactionDT`)
- Transaction & Card Encodings: `product_code_encoded`, `card4_brand_encoded`, `card6_type_encoded`
- Entity Frequencies: `card1_freq`, `addr1_freq` (fitted strictly on training set to prevent leakage)
- Corridor & Identity Risk: `is_foreign_corridor`, `email_domain_risk`, `has_identity`, `is_mobile_device`
- Behavioral Signals: `c1_velocity`, `d1_recency`, `v100_masked_signal` (preserved as numerical signals without invented semantics)

## Evaluation Standards & Primary Metrics
Because fraud is severely imbalanced, raw accuracy is rejected. Primary metrics:
- PR-AUC (Average Precision)
- ROC-AUC
- F1 Score
- Precision@100
- False Positive Rate (FPR) and False Negative Rate (FNR)
- Reports generated to: `ml-backend/training/reports/`

## Explainability (TreeSHAP)
- Native TreeSHAP via `xgb.Booster.predict(pred_contribs=True)` in `ml-backend/app/explainability/shap_explainer.py`.
- Generates exact feature attributions, direction (`increases_risk`/`decreases_risk`), and values.
- Configuration and feature metadata saved in `ml-backend/artifacts/explanation-metadata/shap_config.json`.
- Strict policy: Do not invent real-world meanings for masked/anonymized fields.

## Model Lineage & Immutability
Every prediction returned from `POST /predict` is traceable to:
`prediction -> model_version -> feature_schema_version -> preprocessing_version -> dataset_identifier -> artifact_checksum`.
