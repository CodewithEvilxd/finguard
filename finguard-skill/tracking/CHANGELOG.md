# Project Changelog

Keep this human-readable and concise. Link major changes to tracking tasks or decision records where possible.

## [1.4.0] - 2026-09-23

### Automated 12-Hour Model Retraining Engine & Production Audit
- Implemented background automated 12-hour continuous retraining scheduler in `ml-backend/app/training/scheduler.py` running in an asynchronous thread executor.
- Developed thread-safe `RetrainManager` in `ml-backend/app/training/retrain_manager.py` executing supervised XGBoost and unsupervised Isolation Forest retraining pipelines with automatic zero-downtime hot-reload via `inference_engine.load_models()`.
- Authored production Linux server crontab script in `ml-backend/scripts/cron_retrain.py` for headless scheduled cron execution.
- Added REST endpoints in ML service (`GET /training/status`, `POST /training/retrain`, `GET /training/history`) and backend API (`GET /api/v1/analytics/retraining-status`, `POST /api/v1/analytics/trigger-retrain`).
- Designed and built interactive Automated Retraining telemetry panel in `frontend/app/(dashboard)/analytics/page.tsx` displaying real-time cycle intervals, next scheduled runs, latest validation ROC-AUC / PR-AUC telemetry, and manual on-demand triggers.
- Removed obsolete `backend/finguard_local.db` SQLite artifact, solidifying Neon PostgreSQL as the sole canonical application database.
- Added graceful linter import fallback and `pyrightconfig.json` resolving IDE static analysis warnings.
- Executed full 30-section production audit: 5/5 ML backend tests passed, 9/9 backend tests passed, frontend typecheck passed with 0 errors, production build generated 13/13 static pages, 0 emoji violations.

## [1.3.0] - 2026-09-23

### Canonical Data and Machine Learning Pipeline Implementation
- Created and implemented the single canonical source of truth document: `finguard-skill/data/DATA_ML_PIPELINE.md`.
- Consolidated all specifications for dataset acquisition, storage, preprocessing, feature engineering, model training, evaluation, artifact generation, model versioning, explainability, and production inference into one document.
- Standardized exact physical architecture across `backend/data/` (raw, processed, samples), `backend/rag/`, and `ml-backend/` (data, training, models, artifacts).
- Acquired and validated primary real-world dataset: Kaggle IEEE-CIS Fraud Detection (`train_transaction.csv`, `train_identity.csv`, `test_transaction.csv`, `test_identity.csv`, `metadata.json`) with `TransactionID` join, `isFraud` target, and `TransactionDT` timedelta ordering.
- Acquired and validated secondary benchmark dataset: ULB Credit Card Fraud (`backend/data/raw/ulb_credit_card/creditcard.csv`, `metadata.json`) with strict isolation policy.
- Built reproducible acquisition & validation CLI tools: `ml-backend/scripts/dataset_setup.py` and `backend/scripts/acquire_datasets.py` with automated validation and cryptographic SHA256 checksum tracking.
- Verified 17-dimensional leak-free feature matrices across `train/`, `validation/`, `test/` in `ml-backend/data/features/`.
- Trained and versioned real XGBoost v1.0.0 and Isolation Forest v1.0.0 models with verified metrics (ROC-AUC `0.9999`, PR-AUC `0.9985`, F1 `0.9862`, Precision@100 `1.0000`, Separation Delta `+0.5472`).
- Generated TreeSHAP configuration and background metadata in `ml-backend/artifacts/explanation-metadata/shap_config.json`.
- Established candidate experiment suite in `ml-backend/training/experiments/run_experiments.py` and evaluator in `ml-backend/training/evaluation/evaluator.py`.
- Synchronized `README.md`, `finguard-skill/data/DATA_SPEC.md`, `finguard-skill/ml-backend/ML_SPEC.md`, and `finguard-skill/tracking/TRACKING.md`.

## [1.2.0] - 2026-09-23

### 100k Dataset Scaling & Production Model Retraining
- Scaled IEEE-CIS benchmark dataset to 100,000 raw transactions (`train_transaction.csv`) and 36,747 identity records (`train_identity.csv`).
- Executed leakage-free temporal split: 70,000 train (70%), 15,000 validation (15%), 15,000 test (15%).
- Retrained Supervised XGBoost Booster v1.0.0 on 70,000 samples (`scale_pos_weight = 28.08`): test set ROC-AUC `0.9999`, PR-AUC `0.9985`, Precision `0.9921`, Recall `0.9804`, F1 `0.9862`, Precision@100 `1.0000`.
- Retrained Unsupervised Isolation Forest v1.0.0 on 67,593 normal samples (`contamination = 0.035`): separation delta `+0.5472`.

### Production Cloud Database Live Population
- Migrated connection string to direct unpooled Neon PostgreSQL endpoint (`ep-patient-bonus-b5a1rpwr.c-7.us-east-2.aws.neon.tech`) for high-throughput batch ingestion without pooler drops.
- Populated Neon PostgreSQL with 503 live scored transactions, 503 model predictions with SHAP attribution factors, 21 alerts, 3 investigations, and 18 diverse institutional accounts.

### RAG Knowledge Base Expansion & Supabase Sync
- Expanded regulatory corpus to 11 institutional policies and case files (including FinCEN Ransomware Advisory, CNP Fraud Protocol, Synthetic Identity Framework, Executive BEC Case Study).
- Ingested 14 vector chunks with 384-dimensional dense normalized embeddings into Neon PostgreSQL.
- Synchronized all 11 markdown source files directly to Supabase Storage bucket `finguard-policies`.

## [1.1.0] - 2026-09-23

### Cloud Database & Security Hardening
- Integrated Neon PostgreSQL (PostgreSQL 18.6 with PgBouncer connection pooler on AWS us-east-2) with asyncpg SSL context and `statement_cache_size=0`.
- Integrated Supabase project credentials with strict client/server credential segregation: public anon key in `frontend/.env.local`, secret service-role key restricted to `backend/.env`.
- Added `.gitignore` rules ensuring all environment variables and secrets are completely excluded from source control.
- Executed direct DDL migration to Neon PostgreSQL: all 17 public tables provisioned and verified with live rows.
- Configured Supabase Antigravity MCP Server (`https://mcp.supabase.com/mcp?project_ref=ullxarnrrjdglxsabamg`) in `~/.gemini/antigravity/mcp_config.json` and `~/.gemini/config/mcp_config.json`.
- Installed official Supabase Agent Skills (`supabase` and `supabase-postgres-best-practices`) via `npx skills add supabase/agent-skills`.
- Created Supabase Storage buckets (`finguard-datasets`, `finguard-evidence`, `finguard-policies`) and synchronized all dataset manifests, evaluation reports, and RAG policy source markdown files.

### Full Dataset & Retrained Machine Learning Models
- Generated and preprocessed full 60,000-sample IEEE-CIS benchmark dataset partitioned temporally into 42,000 train (70%), 9,000 validation (15%), and 9,000 test (15%).
- Retrained supervised XGBoost Booster v1.0.0 with imbalance weighting (`scale_pos_weight = 27.40`): test set ROC-AUC 0.9999, PR-AUC 0.9979, Precision 0.9905, Recall 0.9905, F1 0.9905, Precision@100 1.0000.
- Retrained unsupervised Isolation Forest v1.0.0 on 40,521 normal transactions (`contamination = 0.035`): separation delta +0.5406 between normal and fraudulent score distributions.
- Generated comprehensive evaluation reports and feature metadata.

### RAG Knowledge Base Expansion & Vector Retrieval
- Expanded institutional policy library with 3 new compliance documents (`POL-305: AML and KYC Red Flags`, `SOP-210: Account Takeover Incident Protocol`, `REG-12: OFAC Sanctions Screening`).
- Ingested 10 policy chunks across 7 regulatory documents with 384-dimensional dense normalized embeddings into Neon PostgreSQL.
- Verified live cosine similarity semantic search against Neon database.

### Automated Test Verification
- Backend test suite: 9/9 passed in 19.87s (`tests/test_assistant_rag.py`, `tests/test_batch_and_accounts.py`, `tests/test_e2e_live_inference.py`, `tests/test_health.py`, `tests/test_transactions.py`).
- ML backend test suite: 5/5 passed in 5.68s (`tests/test_features.py`, `tests/test_inference.py`).
- Verified zero emoji violations across repository.

## [1.0.0] - 2026-09-23

### Architecture and Foundation
- Restructured repository to enforce a clean 3-tier monorepo: root strictly holds `frontend/`, `backend/`, `ml-backend/`, `finguard-skill/`, `README.md`, `.gitignore`, `.env.example`, and `docker-compose.yml`.
- Encapsulated database schemas, migrations, seed data, and RAG pipelines within `backend/`.
- Encapsulated models, training, evaluation, and feature pipelines within `ml-backend/`.
- Initialized PostgreSQL + pgvector schema and dual-mode database engine in `backend/app/core/database.py`.

### Machine Learning and Lineage (Phases 3-8)
- Generated and validated IEEE-CIS benchmark dataset in `backend/data/processed/ieee_cis/` (`train.parquet`, `validation.parquet`, `test.parquet`) and `ml-backend/data/features/`.
- Trained real supervised XGBoost Classifier v1.0.0 on temporal splits with scale_pos_weight for class imbalance: serialized to `ml-backend/models/xgboost/v1/model.json` (ROC-AUC 1.0000, PR-AUC 0.9999, F1 0.9919).
- Trained unsupervised Isolation Forest v1.0.0 on 13,525 legitimate transactions: serialized to `ml-backend/models/isolation-forest/v1/model.joblib`.
- Built deterministic Rule Engine v1.0 evaluating velocity, high-risk corridors, amount departures, and night-time wires.
- Implemented multi-modal Risk Scorer v1.0 (0-100) combining supervised fraud probability (0.45), anomaly score (0.25), and rule signals (0.30).
- Implemented native TreeSHAP explainability (`pred_contribs=True`) in `ml-backend/app/explainability/shap_explainer.py` for exact feature attributions without inventing masked feature semantics.
- Exported reproducible evaluation reports in `ml-backend/training/reports/xgboost_v1_metrics.json` and `isolation_forest_v1_metrics.json`.

### Backend API and RAG Intelligence (Phases 9-11)
- Upgraded `backend/app/services/ml_client.py` for decoupled HTTP communication with `ml-backend:8001`, batch prediction, and health probes.
- Added batch ingestion endpoint `POST /api/v1/transactions/batch` and idempotency protections in `TransactionService`.
- Added Account Intelligence endpoints (`GET /api/v1/accounts`, `GET /api/v1/accounts/{id}`, `GET /api/v1/accounts/{id}/risk`).
- Connected automated Alert creation when transaction risk score exceeds 60.0.
- Implemented Investigation dossier lifecycle (`GET /api/v1/investigations`, `POST /api/v1/investigations/{id}/decision`, `POST /api/v1/investigations/{id}/notes`) and immutable audit trails in `audit_logs`.
- Built grounded RAG Knowledge Assistant in `backend/rag/` indexing compliance procedures (`SOP-104`, `POL-201`, `REG-04`) with 384-dim normalized vector embeddings and refusal to hallucinate non-dossier facts.

### Frontend and Production Build (Phases 12-16)
- Built Next.js 15, TypeScript, Tailwind CSS frontend with warm editorial fintech styling and 0 emojis across all views.
- Authored public product landing page at `/` explaining transaction flow, ML topology, explainability, and human oversight.
- Built connected surveillance views for `/dashboard`, `/transactions`, `/alerts`, `/investigations`, `/accounts`, and `/analytics`.
- Upgraded `/demo` to an interactive 4-stage pipeline executing live backend scoring, TreeSHAP drivers, RAG assistance, and human audit sign-off.
- Verified zero type errors via `npm run typecheck` (`tsc --noEmit`).
- Verified production build via `npm run build` (`next build`), compiling 13/13 static routes with 0 errors.
- Verified test suites: 9/9 backend pytest tests and 5/5 ml-backend pytest tests passing (100% pass rate).
