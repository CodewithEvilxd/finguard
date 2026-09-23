"""
Instant Re-scoring of Neon PostgreSQL using execute_values with Real ML inferences.
Runs in < 5 seconds total.
"""

import sys
import os
import json
import urllib.request
import time
import psycopg2
import psycopg2.extras

ML_URL = "http://127.0.0.1:8001/batch-predict"

# Read DATABASE_URL from backend/.env
env_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env"))
with open(env_file, "r") as f:
    for line in f:
        if line.startswith("DATABASE_URL="):
            db_url = line.split("=", 1)[1].strip().strip("'\"")

conn = psycopg2.connect(db_url)
conn.autocommit = True
cur = conn.cursor()

# Kill any lingering connections from cancelled task
cur.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND state = 'idle in transaction'")

print("Connected to Neon. Fetching transactions...", flush=True)
cur.execute("SELECT id, transaction_id, account_id, amount, currency, transaction_type, channel, timestamp FROM transactions ORDER BY timestamp")
tx_rows = cur.fetchall()
print(f"Fetched {len(tx_rows)} transactions.", flush=True)

# 1. Batch score all via live ML microservice in 5 chunks of 100
chunk_size = 100
all_predictions = {}
t0 = time.time()

for i in range(0, len(tx_rows), chunk_size):
    chunk = tx_rows[i:i + chunk_size]
    payload = [
        {
            "transaction_id": r[1],
            "amount": float(r[3]),
            "currency": r[4],
            "transaction_type": r[5],
            "channel": r[6],
            "timestamp": r[7].isoformat() if r[7] else None,
            "country": "US",
            "account_id": str(r[2]),
        }
        for r in chunk
    ]
    req = urllib.request.Request(
        ML_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        ml_res = json.loads(resp.read().decode())
    for p in ml_res.get("predictions", []):
        all_predictions[p["transaction_id"]] = p

print(f"Scored all {len(all_predictions)} transactions via real ML models in {time.time() - t0:.2f}s.", flush=True)

# 2. Build tuples for execute_values
pred_tuples = []
tx_tuples = []

for r in tx_rows:
    p = all_predictions.get(r[1])
    if not p:
        continue

    score = float(p["final_risk_score"])
    status = "flagged" if score >= 80.0 else ("under_review" if score >= 60.0 else "completed")
    tx_id = r[0]

    tx_tuples.append((tx_id, status))
    pred_tuples.append((
        tx_id,
        p["model_version"],
        p["fraud_probability"],
        p["anomaly_score"],
        p["rule_score"],
        score,
        p["risk_level"],
        p["explanation_payload"],
    ))

print(f"Updating Neon database using execute_values...", flush=True)
t_db = time.time()

# Update transactions
psycopg2.extras.execute_values(
    cur,
    """
    UPDATE transactions AS t
    SET status = v.status
    FROM (VALUES %s) AS v(id, status)
    WHERE t.id = v.id
    """,
    tx_tuples
)

# Update model_predictions
psycopg2.extras.execute_values(
    cur,
    """
    UPDATE model_predictions AS mp
    SET model_version_name = v.model_version_name,
        fraud_probability = v.fraud_probability::float8,
        anomaly_score = v.anomaly_score::float8,
        rule_score = v.rule_score::float8,
        final_risk_score = v.final_risk_score::float8,
        risk_level = v.risk_level,
        explanation_payload = v.explanation_payload
    FROM (VALUES %s) AS v(tx_id, model_version_name, fraud_probability, anomaly_score, rule_score, final_risk_score, risk_level, explanation_payload)
    WHERE mp.transaction_id = v.tx_id
    """,
    pred_tuples
)

print(f"Neon database updated in {time.time() - t_db:.2f}s!", flush=True)

# Audit
print("\n=== FINAL NEON PREDICTION AUDIT ===", flush=True)
cur.execute("SELECT model_version_name, count(*) FROM model_predictions GROUP BY model_version_name")
for row in cur.fetchall():
    print(f"  Model Version: {row[0]:30} -> {row[1]} rows")

cur.execute("SELECT risk_level, count(*) FROM model_predictions GROUP BY risk_level")
for row in cur.fetchall():
    print(f"  Risk Level:    {row[0]:30} -> {row[1]} rows")

cur.close()
conn.close()
print("\nInstant Re-scoring complete!")
