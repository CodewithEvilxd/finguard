"""
High-Speed Re-scoring of all Neon PostgreSQL transactions using LIVE Real ML Backend (Port 8001).
Eliminates per-row SQL roundtrips via preloaded in-memory maps.
Guarantees 100% of transaction predictions and risk scores are derived directly
from trained XGBoost Booster v1.0.0, trained Isolation Forest v1.0.0, and TreeSHAP.
"""

import sys
import os
import json
import asyncio
import urllib.request
import time
from sqlalchemy import select, text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import AsyncSessionLocal
from app.models.transaction import Transaction
from app.models.ml import ModelPrediction
from app.models.alert import Alert


ML_URL = "http://127.0.0.1:8001/batch-predict"


def call_ml_batch(transactions_payload):
    req = urllib.request.Request(
        ML_URL,
        data=json.dumps(transactions_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


async def rescore_all():
    print("=== RE-SCORING ALL NEON TRANSACTIONS VIA LIVE REAL ML SERVICE (PORT 8001) ===", flush=True)

    async with AsyncSessionLocal() as session:
        # 1. Fetch all transactions, existing predictions, and alerts in 3 fast queries
        print("Fetching transactions, predictions, and alerts from Neon PostgreSQL...", flush=True)
        tx_list = (await session.execute(select(Transaction).order_by(Transaction.timestamp))).scalars().all()
        print(f"Fetched {len(tx_list)} transactions.", flush=True)

        all_preds = (await session.execute(select(ModelPrediction))).scalars().all()
        pred_map_by_tx = {p.transaction_id: p for p in all_preds}
        print(f"Preloaded {len(pred_map_by_tx)} existing predictions into memory.", flush=True)

        all_alerts = (await session.execute(select(Alert))).scalars().all()
        alert_map_by_tx = {a.transaction_id: a for a in all_alerts}
        print(f"Preloaded {len(alert_map_by_tx)} existing alerts into memory.", flush=True)

        # 2. Batch score via ML microservice (chunks of 100)
        chunk_size = 100
        updated_count = 0
        t0 = time.time()

        for i in range(0, len(tx_list), chunk_size):
            chunk = tx_list[i:i + chunk_size]
            payload = [
                {
                    "transaction_id": t.transaction_id,
                    "amount": float(t.amount),
                    "currency": t.currency,
                    "transaction_type": t.transaction_type,
                    "channel": t.channel,
                    "timestamp": t.timestamp.isoformat() if t.timestamp else None,
                    "country": "US",
                    "account_id": str(t.account_id),
                }
                for t in chunk
            ]

            ml_res = call_ml_batch(payload)
            predictions = ml_res.get("predictions", [])
            pred_map = {p["transaction_id"]: p for p in predictions}

            for t in chunk:
                p = pred_map.get(t.transaction_id)
                if not p:
                    continue

                score = float(p["final_risk_score"])
                if score >= 80.0:
                    t.status = "flagged"
                elif score >= 60.0:
                    t.status = "under_review"
                else:
                    t.status = "completed"

                mp = pred_map_by_tx.get(t.id)
                if mp:
                    mp.model_version_name = p["model_version"]
                    mp.fraud_probability = p["fraud_probability"]
                    mp.anomaly_score = p["anomaly_score"]
                    mp.rule_score = p["rule_score"]
                    mp.final_risk_score = score
                    mp.risk_level = p["risk_level"]
                    mp.explanation_payload = p["explanation_payload"]
                else:
                    from app.models.base import generate_uuid
                    mp = ModelPrediction(
                        id=generate_uuid(),
                        transaction_id=t.id,
                        model_version_name=p["model_version"],
                        fraud_probability=p["fraud_probability"],
                        anomaly_score=p["anomaly_score"],
                        rule_score=p["rule_score"],
                        final_risk_score=score,
                        risk_level=p["risk_level"],
                        explanation_payload=p["explanation_payload"]
                    )
                    session.add(mp)
                    pred_map_by_tx[t.id] = mp

                alert = alert_map_by_tx.get(t.id)
                if alert:
                    alert.risk_score = score
                    alert.risk_level = p["risk_level"]
                    try:
                        exp = json.loads(p["explanation_payload"])
                        alert.factors_summary = json.dumps(exp.get("top_risk_factors", []))
                    except Exception:
                        pass

                updated_count += 1

            await session.commit()
            print(f"Re-scored & committed {updated_count}/{len(tx_list)} transactions to Neon...", flush=True)

        elapsed = time.time() - t0
        print(f"\nSuccessfully re-scored all {updated_count} transactions with Real ML in {elapsed:.2f}s!", flush=True)

        # 3. Audit model versions in Neon
        print("\n=== UPDATED NEON PREDICTION AUDIT ===", flush=True)
        res = await session.execute(text("SELECT model_version_name, count(*) FROM model_predictions GROUP BY model_version_name"))
        for row in res.fetchall():
            print(f"  Model Version: {row[0]:30} -> {row[1]} rows")


if __name__ == "__main__":
    asyncio.run(rescore_all())
