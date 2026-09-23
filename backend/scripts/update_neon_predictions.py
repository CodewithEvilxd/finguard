"""
Updates all Neon PostgreSQL transactions with live inferences from ml-backend:8001.
Chunked into small transactions of 25 to guarantee clean commits over Neon network.
"""

import sys
import os
import json
import urllib.request
import time
import psycopg2

ML_URL = "http://127.0.0.1:8001/batch-predict"

# Read DATABASE_URL from backend/.env
env_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env"))
db_url = None
with open(env_file, "r") as f:
    for line in f:
        if line.startswith("DATABASE_URL="):
            db_url = line.split("=", 1)[1].strip().strip("'\"")

conn = psycopg2.connect(db_url)
cur = conn.cursor()

print("Connected to Neon. Fetching transactions...", flush=True)
cur.execute("SELECT id, transaction_id, account_id, amount, currency, transaction_type, channel, timestamp FROM transactions ORDER BY timestamp")
tx_rows = cur.fetchall()
print(f"Fetched {len(tx_rows)} transactions.", flush=True)

chunk_size = 25
updated = 0
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
    with urllib.request.urlopen(req, timeout=15) as resp:
        ml_res = json.loads(resp.read().decode())

    pred_map = {p["transaction_id"]: p for p in ml_res.get("predictions", [])}

    for r in chunk:
        p = pred_map.get(r[1])
        if not p:
            continue

        score = float(p["final_risk_score"])
        status = "flagged" if score >= 80.0 else ("under_review" if score >= 60.0 else "completed")
        tx_id = r[0]

        cur.execute(
            """
            UPDATE model_predictions 
            SET model_version_name = %s,
                fraud_probability = %s,
                anomaly_score = %s,
                rule_score = %s,
                final_risk_score = %s,
                risk_level = %s,
                explanation_payload = %s
            WHERE transaction_id = %s
            """,
            (
                p["model_version"],
                p["fraud_probability"],
                p["anomaly_score"],
                p["rule_score"],
                score,
                p["risk_level"],
                p["explanation_payload"],
                tx_id
            )
        )
        cur.execute("UPDATE transactions SET status = %s WHERE id = %s", (status, tx_id))
        updated += 1

    conn.commit()
    print(f"Committed {updated}/{len(tx_rows)} transactions to Neon...", flush=True)

elapsed = time.time() - t0
print(f"\nAll {updated} transactions re-scored with live ML models in {elapsed:.2f}s!", flush=True)

cur.execute("SELECT model_version_name, count(*) FROM model_predictions GROUP BY model_version_name")
for r in cur.fetchall():
    print(f"  Model Version: {r[0]} -> {r[1]} rows")

cur.close()
conn.close()
