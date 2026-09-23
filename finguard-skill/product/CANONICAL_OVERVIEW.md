# FinGuard AI — Canonical Project Overview & Accurate Definition

This document represents the single canonical, accurate project definition for FinGuard AI, calibrated against current codebase implementations and NIST Explainable AI principles. Use this text for PPT presentations, mentor reviews, README definitions, and architectural pitches.

---

## FinGuard AI Kya Hai?

FinGuard AI ek **AI-Powered Financial Fraud Detection & Anomaly Intelligence Platform** hai jo financial transactions ko analyze karke potentially suspicious activity aur abnormal transaction behavior identify karta hai, risk score generate karta hai, aur model-driven explanations provide karta hai.

### In Simple Words:
> "FinGuard AI financial transactions ko analyze karta hai, suspicious patterns identify karta hai, 0–100 risk score generate karta hai, aur explain karta hai ki transaction ko risky banane wale major factors kya hain, taaki a financial-risk analyst investigation ko faster aur more systematically perform kar sake."

---

## Traditional Systems Se Difference

Traditional systems often rely heavily on predefined rules such as fixed amount thresholds or isolated transaction conditions.

FinGuard AI ka architecture multiple signals combine karta hai:
```text
Transaction Features + Behavioral Features + ML + Anomaly Detection + Rules
```
Isme transaction amount, transaction timing, behavioral deviation, frequency, identity/device-related information aur other available dataset features use kiye jate hain.

---

## Complete Workflow

```text
Incoming Transaction
        ↓
Data Validation
        ↓
Feature Engineering
        ↓
┌─────────────────────────────────────────┐
│            Detection Layer              │
│                                         │
│   XGBoost + Isolation Forest            │
│   + Deterministic Rule Engine           │
└─────────────────────────────────────────┘
        ↓
Unified Risk Scoring
        ↓
Risk Score: 0–100 & Risk Tier
        ↓
SHAP / Rule-Based Explanation
        ↓
Risk Alert
        ↓
Investigation Workspace
        ↓
AI Investigation Assistant (RAG)
        ↓
Human Analyst Review
        ↓
Clear / Escalate / Confirm
        ↓
Append-Only Audit Trail
```

---

## Detailed Step-by-Step Breakdown

### Step 1 — Data Ingestion & Feature Engineering
- Transaction backend receive karega aur schema-validate karega.
- Uske baad feature pipeline transaction ko ML-ready representation me convert karegi.
- **Feature Categories**:
  1. Transaction Amount & Value Metrics
  2. Temporal & Timing Patterns
  3. Velocity & Frequency Accelerations
  4. Account & Identity Signals
  5. Device & Network Footprint
  6. Geographic Corridor Deviations
  7. Historical Behavior Baselines

### Step 2 — Three-Layer Detection Triad
1. **XGBoost (Supervised Classification)**:
   - Historical labelled fraud patterns identify karne ke liye.
   - **Output**: Fraud Probability (0 to 1).
   - *Dataset Benchmark*: IEEE-CIS Fraud Detection dataset is project ka primary real-world benchmark aur training source hai, jisme transaction aur identity data `TransactionID` se linked hain aur `isFraud` supervised target hai.
2. **Isolation Forest (Unsupervised Anomaly Detection)**:
   - Novel aur previously unseen anomalous patterns detect karne ke liye.
   - **Output**: Anomaly Score (normalized 0 to 1).
3. **Deterministic Rule Engine**:
   - High-risk thresholds, velocity spikes, aur policy rules check karne ke liye.
   - **Output**: Rule Risk Signals & Scores.

### Step 3 — Unified Risk Scoring
System teeno detection signals ko combine karke transparent **Risk Score (0–100)** aur Risk Tier (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`) generate karta hai:
```text
Fraud Probability + Anomaly Signal + Rule Signal + Behavioral Risk
                               ↓
                      Unified Risk Score
```
Thresholds configurable hain taaki business policies ke according tune kiya ja sake.

### Step 4 — Explainability (TreeSHAP)
High-risk transactions par system mathematically ground kiye gaye contributing factors display karta hai:
- *Why was this transaction flagged?*
- High amount deviation relative to historical baseline
- Unusual transaction timing
- New or unfamiliar entity/device signals
- Velocity acceleration across short observation windows

XGBoost ke liye TreeSHAP methodology use ki jaati hai (NIST Explainable AI principles ke mutabiq actual model logic aur feature values par based, fabricated reasons par nahi).

### Step 5 — AI Investigation Assistant (Grounded RAG)
High-risk transaction ke liye analyst dedicated investigation workspace me case dossier open karta hai.
AI assistant relevant evidence retrieve karke analyst ke natural language questions ka answer deta hai:
- *"Why was this transaction flagged?"*
- *"Show related suspicious activity across this account."*
- *"Summarize compliance violations and applicable standard operating procedures."*

RAG ka purpose approved compliance policies aur case facts ke basis par **grounded investigation assistance** dena hai without hallucinations.

### Step 6 — Human-in-the-Loop Decision & Audit
Final decision hamesha authorized human analyst ke paas rehta hai:
- **Clear**: False positive mark karke case close karna.
- **Escalate**: Senior compliance officer ya tier-2 team ko forward karna.
- **Confirm**: Suspicious activity confirm karke further compliance action ke liye mark karna.

System analyst action, timestamp, case state, justification, aur investigation history ko **append-only audit trail** me permanently record karta hai.

---

## Core Operational Principle

> **"AI assists the investigation; the analyst remains responsible for the final workflow decision."**

NIST guidelines ke according explainable AI systems me meaningful explanations, explanation accuracy, aur clear operating boundaries essential hain.

---

## One-Line Final Definition

> **FinGuard AI = Detect Suspicious Activity → Quantify Risk → Explain the Risk → Investigate with Grounded AI → Human Review → Append-Only Audit.**
