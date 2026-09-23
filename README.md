# FinGuard AI

Explainable AI Platform for Financial Fraud and Anomaly Intelligence.

## Overview

FinGuard AI is an enterprise financial intelligence platform delivering real-time fraud classification, unsupervised anomaly detection, configurable deterministic risk scoring, SHAP explainability, investigation workflows, grounded AI assistance with source citations, and immutable audit logs.

The platform enforces human-in-the-loop decision-making: the system detects, scores, and contextualizes risk signals, while authorized analysts confirm, clear, or escalate cases.

## Core Capabilities

1. Transaction Ingestion and Validation: Idempotent ingestion pipeline with schema validation and deduplication.
2. Hybrid Detection Engine:
   - Supervised classification using XGBoost for labelled fraud patterns.
   - Unsupervised anomaly detection using Isolation Forest for novel behaviors.
   - Deterministic rule engine for high-velocity and geographic policy checks.
3. Configurable Unified Risk Scoring: Transparent, versioned scoring combining model outputs and deterministic signals.
4. Explainable Risk Factors: SHAP attribution values explaining top contributors for every alert.
5. Investigation Workspace: Consolidated view of transaction facts, account history, timeline, risk factors, and related entities.
6. Grounded AI Assistant: Retrieval-Augmented Generation (RAG) backed by pgvector, citing approved policies and standard operating procedures without hallucinating transaction data.
7. Immutable Audit Trail: Every analyst decision and system evaluation is permanently recorded.

## Data & Machine Learning Pipeline

The single canonical source of truth for all dataset acquisition, physical storage, preprocessing, feature engineering, model training, evaluation reports, model versioning, TreeSHAP explainability, and production inference is documented in [finguard-skill/data/DATA_ML_PIPELINE.md](file:///d:/finguard/finguard-skill/data/DATA_ML_PIPELINE.md).

### Pipeline Flow:
```
External Sources (Kaggle IEEE-CIS & ULB)
  --> Raw Data (backend/data/raw/ieee_cis/, backend/data/raw/ulb_credit_card/)
  --> Validation & Quality Audit (schema, duplicates, missingness, target leakage)
  --> Processed Parquet Storage (backend/data/processed/ieee_cis/)
  --> Feature Engineering (ml-backend/data/features/ -> train/, validation/, test/)
  --> Real Model Training (XGBoost v1.0.0, Isolation Forest v1.0.0)
  --> Rigorous Evaluation (ml-backend/training/reports/)
  --> Model Registry & Metadata (ml-backend/models/registry/model_registry.json)
  --> Production Inference (ml-backend:8001 -> /predict, /explain)
  --> Core Backend (backend:8000 -> /api/v1/transactions)
  --> Next.js 15 Frontend (frontend:3000)
```

### Reproducible Data Acquisition:
```bash
# Acquire and validate IEEE-CIS and ULB raw datasets
cd ml-backend
.venv/Scripts/python.exe scripts/dataset_setup.py --validate
```

## Architecture

The platform is organized into three decoupled services:

```
Browser
  |
  +---> [frontend/] (Next.js 15, TypeScript, Tailwind CSS, Lucide, Recharts)
          |-- / (Public Editorial Product Landing Page)
          |-- /demo (Interactive Sandbox Demo)
          |-- /dashboard (Operational Risk Overview)
          |-- /transactions, /alerts, /investigations, /analytics, /settings
          |
          +---> [backend/] (FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic)
                  |-- /api/v1/transactions (Ingest, validate, query)
                  |-- /api/v1/alerts (Lifecycle, status management)
                  |-- /api/v1/investigations (Evidence synthesis, analyst decisions)
                  |-- /api/v1/assistant/query (Grounded RAG assistant)
                  |-- /api/v1/analytics (Risk metrics and trends)
                  |-- /api/v1/health & /ready (Service probes)
                  |
                  +---> [ml-backend/] (FastAPI, Scikit-learn, XGBoost, Isolation Forest, SHAP)
                  |       |-- /predict (Supervised + Anomaly + Rule inference)
                  |       |-- /explain/{id} (SHAP force values)
                  |       |-- /health & /ready (Inference probes)
                  |
                  +---> [Database] (PostgreSQL 16 + pgvector)
                          |-- Relational domain entities and pgvector document embeddings
```

## Repository Structure

```
finguard/
|-- frontend/           Next.js 15 web client and editorial UI
|-- backend/            FastAPI core service, database, RAG pipeline, and audit
|-- ml-backend/         FastAPI ML inference service, models, and feature pipeline
|-- finguard-skill/     Project specifications, requirements, and tracking
|-- README.md           Project overview and operational guide
|-- .env.example        Master environment variable template
|-- .gitignore          Source control ignore rules
`-- docker-compose.yml  Container orchestration definition
```

## Service Ports

| Service | Port | Description |
|---|---|---|
| frontend | 3000 | Next.js web application |
| backend | 8000 | Core FastAPI backend API (`/api/v1`) |
| ml-backend | 8001 | ML inference microservice |
| postgres | 5432 | PostgreSQL 16 database with pgvector |

## Environment Setup

1. Copy the master environment template:
   ```bash
   cp .env.example .env
   ```

2. Configure environment credentials in `.env` as required. For local development with demo fallback, default settings are operational.

3. For frontend local overrides:
   ```bash
   cp frontend/.env.example frontend/.env.local
   ```

## Development Commands

### Local Native Execution

Prerequisites: Node.js 20+, Python 3.12, and PostgreSQL 16.

1. Start Core Backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. Start ML Backend:
   ```bash
   cd ml-backend
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
   ```

3. Start Frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Docker Compose Execution

Start all four services with a single command:
```bash
docker compose up --build
```

Access points:
- Landing Page: http://localhost:3000
- Demo Sandbox: http://localhost:3000/demo
- Operational Dashboard: http://localhost:3000/dashboard
- Core Backend Docs: http://localhost:8000/docs
- ML Backend Docs: http://localhost:8001/docs

## Verification and Testing

- Frontend type check and build:
  ```bash
  cd frontend && npm run typecheck && npm run build
  ```
- Backend test suite:
  ```bash
  cd backend && pytest tests/
  ```
- ML Backend test suite:
  ```bash
  cd ml-backend && pytest tests/
  ```

## Security and Compliance Notes

- No secrets or credentials are saved in source control.
- All client-facing variables use the `NEXT_PUBLIC_` prefix.
- All analyst decisions produce immutable audit records.
- Zero mock statistics or fabricated metrics are presented as verified facts.
