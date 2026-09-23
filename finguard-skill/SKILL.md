# FinGuard AI - Master Build Skill

## Purpose
This folder is the single source of truth for building FinGuard AI as a production-quality, hackathon-winning financial fraud and anomaly intelligence platform.

## Product
FinGuard AI is an AI-powered financial intelligence platform focused on fraud and anomaly detection, dynamic risk scoring, explainable alerts, investigation workflows, and AI-assisted investigation. The Finance problem statement requires analysis of financial data, anomaly detection, workflow automation, forecasting or intelligent decision support, and clear explanations behind AI-generated decisions.

## Non-negotiable engineering rules
1. Build production-quality software, not a demo-only prototype.
2. Keep frontend, backend, and ml-backend separated as independent services.
3. Keep root clean and modular.
4. No emoji anywhere in source code, UI copy, documentation, logs, commit messages, or generated sample data.
5. No fake accuracy numbers, fake compliance claims, fake production metrics, or fabricated financial data presented as real.
6. Every ML metric shown in the UI or documentation must come from a recorded experiment.
7. Every AI answer must distinguish retrieved evidence from model-generated interpretation.
8. Keep humans in the loop for consequential financial decisions. The system recommends and prioritizes; an authorized analyst confirms, clears, or escalates.
9. Do not hard-code business thresholds that are presented as universal rules; store configurable thresholds and document their purpose.
10. Never expose secrets or sensitive data in client code, logs, screenshots, fixtures, or Git history.
11. Use type-safe APIs and validated schemas across service boundaries.
12. Add tests for every critical path before marking the task complete.
13. Prefer simple, auditable architecture over unnecessary microservices.
14. Every completed task must update `skill/tracking/TRACKING.md` and the relevant design document if scope changed.
15. Before implementing any feature, read the relevant skill file and preserve its constraints.

## Required user experience
The first route opened by a visitor must be a polished interface/landing page, not the operational dashboard. The landing page must communicate the product in seconds and provide clear paths to the product demo or sign-in. The dashboard is a separate application surface after authentication or demo entry.

## Design direction
Use a premium editorial fintech style: warm white/off-white canvas, restrained navy/charcoal typography, one primary accent family based on warm orange with optional muted blue support, generous whitespace, thin dividers, simple flat icons, subtle hand-drawn annotations, strong typographic hierarchy, and realistic product UI only where it directly supports the story. Avoid glossy cyberpunk visuals, neon gradients, excessive glassmorphism, floating-card overload, generic AI brain graphics, stock photography, and visually noisy dashboard walls.

The visual language may take inspiration from the user's previous clean presentation style, but must not copy another project's layout, wording, branding, or assets.

## Core product loop
Transaction ingestion -> validation -> feature engineering -> hybrid detection -> risk scoring -> explainability -> alerting -> investigation context -> AI-assisted investigation -> human decision -> audit trail -> monitoring.

## Preferred stack
Frontend: Next.js 15+, TypeScript, Tailwind CSS, shadcn/ui, Recharts, Lucide React.
Backend: Python, FastAPI, Pydantic, SQLAlchemy or SQLModel, Alembic.
ML: Python, Pandas, NumPy, scikit-learn, XGBoost, Isolation Forest, SHAP.
AI/RAG: OpenAI-compatible LLM API, LangGraph only where orchestration materially helps, pgvector, sentence-transformers or equivalent embeddings.
Database: PostgreSQL.
Realtime: Supabase Realtime or WebSockets.
Auth: Supabase Auth or a clearly documented equivalent.
DevOps: Docker, Docker Compose, GitHub Actions, Vercel for frontend and Railway/Render/AWS-class backend hosting as appropriate.

## Service boundaries
- frontend owns presentation, routing, client state, accessibility, and UX.
- backend owns auth integration, business logic, database access, alert lifecycle, investigations, audit records, and orchestration.
- ml-backend owns feature engineering, model loading, inference, scoring, explainability artifacts, and ML health endpoints.
- rag owns ingestion/retrieval contracts and prompt/context assembly; it may run within backend initially if that keeps deployment simpler.

## Definition of done
A feature is done only when implementation, validation, tests, docs, telemetry, error states, loading states, empty states, accessibility, and tracking are updated.
