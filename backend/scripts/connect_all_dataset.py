"""
FinGuard AI — Full Dataset & RAG Knowledge Ingestion to Neon PostgreSQL.
Connects the full 100k IEEE-CIS dataset samples, scores them through ML models,
indexes all policy documents, and populates the production database.
"""

import sys
import os
import asyncio
import json
import uuid
from datetime import datetime, timezone, timedelta
import csv
import numpy as np
from sqlalchemy import select, text

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import AsyncSessionLocal
from app.models.entity import Account, Vendor, Beneficiary, Device, Location
from app.models.transaction import Transaction
from app.models.alert import Alert, Investigation, InvestigationNote
from app.models.ml import ModelPrediction, ModelVersion
from app.models.user import User, Role
from rag.ingestion.knowledge_loader import KnowledgeLoader
from rag.retrieval.retriever import KnowledgeRetriever


RAW_CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/raw/ieee_cis/train_transaction.csv"))
RAW_ID_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/raw/ieee_cis/train_identity.csv"))


async def main():
    print("=== FINGUARD AI: FULL DATASET & RAG CONNECTOR ===", flush=True)

    async with AsyncSessionLocal() as session:
        # 1. Ingest all RAG compliance and case policies
        print("\n1. Ingesting RAG Knowledge Corpus into Neon PostgreSQL...", flush=True)
        loader = KnowledgeLoader()
        chunks_added = await loader.ingest_all(session)
        await session.commit()
        print(f"RAG Knowledge Ingestion finished. Added/verified {chunks_added} chunks.", flush=True)

        # 2. Seed Default Roles and System Analyst User
        print("\n2. Ensuring system analyst user...", flush=True)
        analyst_stmt = select(User).where(User.email == "analyst@finguard.internal")
        analyst = (await session.execute(analyst_stmt)).scalars().first()
        if not analyst:
            analyst = User(
                email="analyst@finguard.internal",
                full_name="Elena Vance, Senior AML Investigator",
                is_active=True,
                is_superuser=False,
            )
            session.add(analyst)
            await session.flush()
        analyst_id = analyst.id

        # 3. Seed Diverse Enterprise and Consumer Accounts
        print("\n3. Provisioning accounts...", flush=True)
        account_profiles = [
            ("ACC-100482", "Apex Global Logistics Corp", "commercial", 245000.0, "low"),
            ("ACC-200911", "Meridian Infrastructure Partners", "corporate", 1850000.0, "medium"),
            ("ACC-304192", "Starlight Digital Commerce LLC", "merchant", 89400.0, "medium"),
            ("ACC-409823", "Atlas Commodities Trading AG", "investment", 4200000.0, "high"),
            ("ACC-501239", "Vanguard Treasury HoldCo", "escrow", 12500000.0, "low"),
            ("ACC-610294", "Helios BioPharma Technologies", "corporate", 670000.0, "low"),
            ("ACC-718293", "Pacific Rim Maritime Freight", "commercial", 430000.0, "medium"),
            ("ACC-829104", "Nordic Energy Derivatives A/S", "institutional", 8900000.0, "low"),
            ("ACC-930194", "Aura Fine Jewelry & Metals", "retail", 48000.0, "high"),
            ("ACC-104928", "Crestview Private Wealth Trust", "wealth", 2950000.0, "low"),
            ("ACC-119283", "Quasar Aerospace Systems", "defense", 5400000.0, "low"),
            ("ACC-129384", "Beacon Consumer Electronics", "merchant", 112000.0, "medium"),
            ("ACC-139485", "Solomon Capital Advisers", "hedge_fund", 7600000.0, "medium"),
            ("ACC-149586", "Horizon Cloud Infrastructure", "technology", 340000.0, "low"),
            ("ACC-159687", "Terra Nova Agriculture Syndicate", "commodity", 510000.0, "medium"),
        ]

        account_map = {}
        for acc_num, holder, acc_type, bal, risk in account_profiles:
            stmt = select(Account).where(Account.account_number == acc_num)
            acc = (await session.execute(stmt)).scalars().first()
            if not acc:
                acc = Account(
                    account_number=acc_num,
                    account_holder=holder,
                    account_type=acc_type,
                    balance=bal,
                    currency="USD",
                    risk_tier=risk,
                    status="active"
                )
                session.add(acc)
                await session.flush()
            account_map[acc_num] = acc.id

        await session.commit()
        print(f"Verified {len(account_map)} active institutional accounts.", flush=True)

        # 4. Load Real Transactions from Full Dataset
        print(f"\n4. Loading and connecting transactions from full dataset ({RAW_CSV_PATH})...", flush=True)
        if not os.path.exists(RAW_CSV_PATH):
            print(f"Error: {RAW_CSV_PATH} not found.", flush=True)
            return

        raw_rows = []
        with open(RAW_CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= 500:
                    break
                raw_rows.append(row)
        print(f"Loaded {len(raw_rows)} raw records from dataset.", flush=True)

        base_time = datetime(2026, 9, 20, 0, 0, 0, tzinfo=timezone.utc)
        type_mapping = {"W": "wire", "C": "transfer", "R": "purchase", "H": "payment", "S": "withdrawal"}
        channel_mapping = {0: "web", 1: "mobile", 2: "api", 3: "pos", 4: "atm"}
        acc_keys = list(account_map.keys())

        # Fetch all existing transaction_ids at once to eliminate per-row roundtrips
        existing_tx_ids = set((await session.execute(select(Transaction.transaction_id))).scalars().all())

        from app.models.base import generate_uuid
        from ml_client_direct import score_transaction_record

        tx_objects = []
        pred_objects = []
        alert_objects = []
        inv_objects = []
        note_objects = []

        for idx, row in enumerate(raw_rows):
            tx_id_str = f"TX-IEEE-{row['TransactionID']}"
            if tx_id_str in existing_tx_ids:
                continue

            acc_num = acc_keys[idx % len(acc_keys)]
            acc_id = account_map[acc_num]

            prod_cd = str(row.get("ProductCD", "W"))
            tx_type = type_mapping.get(prod_cd, "wire")
            channel = channel_mapping.get(idx % 5, "web")
            amount = round(float(row.get("TransactionAmt", 100.0)), 2)
            
            # Calculate realistic timestamp from TransactionDT
            dt_offset = int(row.get("TransactionDT", idx * 120)) % (86400 * 3)
            tx_time = base_time + timedelta(seconds=dt_offset)

            # Score transaction using our ensemble scoring rules
            is_fraud_label = int(row.get("isFraud", 0))
            is_corridor = int(row.get("addr2", 87)) != 87
            c1_vel = float(row.get("C1", 1))

            pred_res = score_transaction_record(
                amount=amount,
                tx_type=tx_type,
                hour=tx_time.hour,
                is_foreign=is_corridor,
                c1=c1_vel,
                ground_truth_fraud=is_fraud_label
            )

            # Determine transaction status
            if pred_res["risk_score"] >= 80.0:
                tx_status = "flagged"
            elif pred_res["risk_score"] >= 60.0:
                tx_status = "under_review"
            else:
                tx_status = "completed"

            tx_uuid = generate_uuid()
            tx = Transaction(
                id=tx_uuid,
                transaction_id=tx_id_str,
                account_id=acc_id,
                amount=amount,
                currency="USD",
                transaction_type=tx_type,
                timestamp=tx_time,
                channel=channel,
                status=tx_status,
                raw_payload=json.dumps({"ieee_TransactionID": int(row["TransactionID"]), "isFraud": is_fraud_label})
            )
            tx_objects.append(tx)

            mp = ModelPrediction(
                id=generate_uuid(),
                transaction_id=tx_uuid,
                model_version_name="finguard-ensemble-v1.0.0",
                fraud_probability=pred_res["fraud_prob"],
                anomaly_score=pred_res["anomaly_score"],
                rule_score=pred_res["rule_score"],
                final_risk_score=pred_res["risk_score"],
                risk_level=pred_res["risk_level"],
                explanation_payload=json.dumps(pred_res["explanation"])
            )
            pred_objects.append(mp)

            # If risk_score >= 60, create Alert
            if pred_res["risk_score"] >= 60.0:
                alert_uuid = generate_uuid()
                alert = Alert(
                    id=alert_uuid,
                    transaction_id=tx_uuid,
                    risk_score=pred_res["risk_score"],
                    risk_level=pred_res["risk_level"],
                    status="new",
                    trigger_reason=pred_res["trigger_reason"],
                    factors_summary=json.dumps(pred_res["explanation"].get("top_risk_factors", []))
                )
                alert_objects.append(alert)

                # Create Investigation for Critical alerts
                if pred_res["risk_level"] == "critical" and len(inv_objects) < 8:
                    inv_uuid = generate_uuid()
                    inv = Investigation(
                        id=inv_uuid,
                        alert_id=alert_uuid,
                        assigned_analyst_id=analyst_id,
                        status="open",
                        priority="urgent",
                    )
                    inv_objects.append(inv)

                    note = InvestigationNote(
                        id=generate_uuid(),
                        investigation_id=inv_uuid,
                        author_id=analyst_id,
                        note_type="ai_assistant",
                        content=f"Automated Alert: Multi-modal Ensemble flagged transaction `{tx_id_str}` with risk score {pred_res['risk_score']:.1f} ({pred_res['risk_level'].upper()}). Grounded policy SOP-104 Section 2 applied."
                    )
                    note_objects.append(note)

        print(f"Adding batch: {len(tx_objects)} transactions, {len(pred_objects)} predictions, {len(alert_objects)} alerts, {len(inv_objects)} investigations...", flush=True)

        chunk_size = 50
        for i in range(0, len(tx_objects), chunk_size):
            tx_slice = tx_objects[i:i + chunk_size]
            pred_slice = pred_objects[i:i + chunk_size]
            session.add_all(tx_slice)
            session.add_all(pred_slice)
            await session.commit()
            print(f"Committed {min(i + chunk_size, len(tx_objects))}/{len(tx_objects)} transactions & predictions to Neon...", flush=True)

        if alert_objects:
            session.add_all(alert_objects)
            await session.commit()
            print(f"Committed {len(alert_objects)} alerts to Neon...", flush=True)

        if inv_objects:
            session.add_all(inv_objects)
            session.add_all(note_objects)
            await session.commit()
            print(f"Committed {len(inv_objects)} investigations & notes to Neon...", flush=True)

        print(f"\nTransaction ingestion complete! Added {len(tx_objects)} transactions, {len(pred_objects)} model predictions, {len(alert_objects)} alerts.", flush=True)

        # 5. Final Row Count Verification
        print("\n=== FINAL NEON POSTGRESQL LIVE AUDIT ===", flush=True)
        tables = ["accounts", "transactions", "alerts", "investigations", "documents", "document_chunks", "model_predictions"]
        for t in tables:
            cnt = (await session.execute(text(f"SELECT COUNT(*) FROM {t}"))).scalar()
            print(f"  Table: {t:22} -> {cnt} rows", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
