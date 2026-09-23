import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from sqlalchemy import select

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.core.database import get_db, init_db
from app.models.user import User, Role, UserRole
from app.models.entity import Account, Vendor, Beneficiary, Device, Location
from app.models.document import Document, DocumentChunk
from app.models.transaction import Transaction
from app.models.ml import ModelPrediction
from app.models.alert import Alert, Investigation, InvestigationNote
from rag.embeddings.embedder import embedder
from app.core.logging import logger


async def seed():
    logger.info("Initializing database schema...")
    await init_db()

    async for session in get_db():
        # Check if already seeded
        q = await session.execute(select(Role))
        if q.scalars().first():
            logger.info("Database already seeded. Skipping.")
            return

        logger.info("Seeding roles and users...")
        roles = [
            Role(name="Admin", description="Platform administrator with full configuration privileges"),
            Role(name="Risk Manager", description="Senior manager managing fraud rules and alert queues"),
            Role(name="Analyst", description="Fraud analyst reviewing flagged cases and submitting decisions"),
            Role(name="Viewer", description="Read-only access for compliance auditors"),
        ]
        session.add_all(roles)
        await session.flush()

        analyst_user = User(
            email="analyst@finguard.ai",
            full_name="Sarah Chen",
            is_active=True,
            is_superuser=False,
        )
        session.add(analyst_user)
        await session.flush()

        session.add(UserRole(user_id=analyst_user.id, role_id=roles[2].id))

        logger.info("Seeding financial accounts...")
        accounts = [
            Account(account_number="ACC-100482", account_holder="Apex Global Logistics", balance=245000.0, currency="USD", risk_tier="low"),
            Account(account_number="ACC-829104", account_holder="Helios Semiconductor Corp", balance=890000.0, currency="USD", risk_tier="low"),
            Account(account_number="ACC-552019", account_holder="Vanguard Retail Holdings", balance=42000.0, currency="USD", risk_tier="medium"),
            Account(account_number="ACC-330192", account_holder="Elena Rostova", balance=18500.0, currency="USD", risk_tier="low"),
        ]
        session.add_all(accounts)
        await session.flush()

        logger.info("Seeding knowledge base compliance documents...")
        docs = [
            (
                "SOP-104: Rapid Multi-Hop Wire Verification",
                "standard_operating_procedure",
                "When an international wire exceeding $25,000 is initiated from a previously unseen device, the analyst must verify whether multi-factor authentication was completed. If the beneficiary country differs from the account's historical trade corridors, request secondary phone verification before approving release.",
            ),
            (
                "POL-201: Unusual Velocity & Geo-IP Deviations",
                "policy",
                "Transactions executed within 15 minutes across distinct geographical jurisdictions exceeding 500 miles imply credential compromise or proxy rotation. The associated card or account should be temporarily marked under review while contacting the accountholder.",
            ),
            (
                "REG-04: Bank Secrecy Act Suspicious Activity Reporting Guidelines",
                "regulation",
                "Financial institutions must document objective risk indicators when filing Suspicious Activity Reports (SARs). Model predictions alone cannot constitute sole grounds for filing; verifiable transactional anomalies and human analyst review must be present in the case dossier.",
            ),
        ]

        for title, category, content in docs:
            doc = Document(title=title, category=category, version="v1.0")
            session.add(doc)
            await session.flush()

            embedding = embedder.get_embedding(content)
            chunk = DocumentChunk(
                document_id=doc.id,
                chunk_index=0,
                content=content,
                metadata_json=json.dumps({"source": title, "category": category}),
                embedding_json=json.dumps(embedding),
            )
            session.add(chunk)

        logger.info("Seeding sample transactions, alerts, and investigations...")
        now = datetime.now(timezone.utc)

        # 1. Normal low-risk transaction
        tx1 = Transaction(
            transaction_id="TXN-20260922-001",
            account_id=accounts[0].id,
            amount=420.50,
            currency="USD",
            transaction_type="purchase",
            channel="web",
            status="completed",
            timestamp=now,
        )
        session.add(tx1)
        await session.flush()

        pred1 = ModelPrediction(
            transaction_id=tx1.id,
            fraud_probability=0.02,
            anomaly_score=0.08,
            rule_score=0.0,
            final_risk_score=12.0,
            risk_level="low",
            feature_version="v1.0",
            scoring_version="v1.0",
            explanation_payload=json.dumps({"factors": [{"factor": "Consistent merchant pattern", "contribution": -0.4}]}),
        )
        session.add(pred1)

        # 2. Suspicious high-risk wire transaction
        tx2 = Transaction(
            transaction_id="TXN-20260922-002",
            account_id=accounts[2].id,
            amount=84500.00,
            currency="USD",
            transaction_type="wire",
            channel="web",
            status="flagged",
            timestamp=now,
        )
        session.add(tx2)
        await session.flush()

        pred2 = ModelPrediction(
            transaction_id=tx2.id,
            fraud_probability=0.88,
            anomaly_score=0.92,
            rule_score=45.0,
            final_risk_score=87.5,
            risk_level="high",
            feature_version="v1.0",
            scoring_version="v1.0",
            explanation_payload=json.dumps({
                "factors": [
                    {"factor": "Amount exceeds 10x 30-day average", "contribution": 0.42},
                    {"factor": "First wire transfer to unverified foreign corridor", "contribution": 0.31},
                    {"factor": "New device fingerprint with masked subnet", "contribution": 0.15},
                ]
            }),
        )
        session.add(pred2)

        alert2 = Alert(
            transaction_id=tx2.id,
            risk_score=87.5,
            risk_level="high",
            status="investigating",
            trigger_reason="Automated risk trigger: HIGH score (87.5) on foreign wire velocity spike",
            factors_summary=pred2.explanation_payload,
        )
        session.add(alert2)
        await session.flush()

        inv2 = Investigation(
            alert_id=alert2.id,
            assigned_analyst_id=analyst_user.id,
            status="under_review",
            priority="urgent",
        )
        session.add(inv2)
        await session.flush()

        note2 = InvestigationNote(
            investigation_id=inv2.id,
            author_id=analyst_user.id,
            note_type="analyst",
            content="Account balance drained by 80% in single international wire transfer. Contacting accountholder for verbal authorization.",
        )
        session.add(note2)

        await session.commit()
        logger.info("Database seeding completed successfully.")


if __name__ == "__main__":
    asyncio.run(seed())
