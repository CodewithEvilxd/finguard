import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.entity import Account
from app.models.transaction import Transaction
from app.models.ml import ModelPrediction
from app.models.alert import Alert, Investigation
from app.schemas.transaction import TransactionCreate
from app.services.ml_client import ml_client
from app.services.alert_service import AlertService
from app.services.audit_service import AuditService
from app.core.logging import logger


class TransactionService:
    @staticmethod
    async def ingest_transaction(
        db: AsyncSession,
        data: TransactionCreate,
        actor_id: Optional[str] = None,
    ) -> Tuple[Transaction, bool]:
        """
        Idempotent transaction ingestion:
        - If transaction_id already exists, return existing transaction (created=False).
        - If new, create account if not exists, persist transaction, evaluate ML/rules, and return (created=True).
        """
        existing = await db.execute(
            select(Transaction).where(Transaction.transaction_id == data.transaction_id)
        )
        existing_tx = existing.scalars().first()
        if existing_tx:
            logger.info(f"Transaction {data.transaction_id} already ingested. Returning existing record idempotently.")
            return existing_tx, False

        # Ensure account exists
        acc_query = await db.execute(select(Account).where(Account.account_number == data.account_id))
        account = acc_query.scalars().first()
        if not account:
            account = Account(
                account_number=data.account_id,
                account_holder=f"Account Holder ({data.account_id})",
                balance=15000.0,
                currency=data.currency,
                risk_tier="standard",
            )
            db.add(account)
            await db.flush()

        tx_time = data.timestamp or datetime.now(timezone.utc)
        transaction = Transaction(
            transaction_id=data.transaction_id,
            account_id=account.id,
            amount=data.amount,
            currency=data.currency,
            transaction_type=data.transaction_type,
            channel=data.channel,
            timestamp=tx_time,
            status="completed",
        )
        db.add(transaction)
        await db.flush()

        # Invoke ML inference / scoring
        prediction_payload = {
            "transaction_id": transaction.transaction_id,
            "account_id": data.account_id,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "transaction_type": transaction.transaction_type,
            "channel": transaction.channel,
            "timestamp": transaction.timestamp.isoformat(),
            "country": data.country,
        }
        pred_result = await ml_client.predict_transaction(prediction_payload)

        # Store model prediction record
        prediction_record = ModelPrediction(
            transaction_id=transaction.id,
            fraud_probability=pred_result.get("fraud_probability"),
            anomaly_score=pred_result.get("anomaly_score"),
            rule_score=pred_result.get("rule_score"),
            final_risk_score=pred_result.get("final_risk_score", 0.0),
            risk_level=pred_result.get("risk_level", "low"),
            feature_version=pred_result.get("feature_version", "v1.0"),
            scoring_version=pred_result.get("scoring_version", "v1.0"),
            model_version_name=pred_result.get("model_version", "finguard-xgboost-v1.0.0"),
            explanation_payload=pred_result.get("explanation_payload"),
        )
        db.add(prediction_record)
        await db.flush()

        # Generate alert if risk exceeds threshold
        alert = await AlertService.create_alert_if_needed(
            db=db,
            transaction=transaction,
            risk_score=prediction_record.final_risk_score,
            risk_level=prediction_record.risk_level,
            factors_summary=prediction_record.explanation_payload,
        )

        # Record audit log
        await AuditService.record_event(
            db=db,
            action="TRANSACTION_INGESTED",
            entity_type="transaction",
            entity_id=transaction.id,
            actor_id=actor_id,
            description=f"Transaction {transaction.transaction_id} ingested, risk score: {prediction_record.final_risk_score:.1f}",
            payload_after={"amount": transaction.amount, "currency": transaction.currency, "score": prediction_record.final_risk_score},
        )

        return transaction, True

    @staticmethod
    async def ingest_batch(
        db: AsyncSession,
        items: List[TransactionCreate],
        actor_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Batch ingestion of transactions with idempotency, ML scoring, and alert generation.
        """
        created_count = 0
        skipped_count = 0
        flagged_count = 0
        persisted_txs = []

        for item in items:
            tx, created = await TransactionService.ingest_transaction(db, item, actor_id=actor_id)
            persisted_txs.append(tx)
            if created:
                created_count += 1
                if tx.status == "flagged":
                    flagged_count += 1
            else:
                skipped_count += 1

        return {
            "total_received": len(items),
            "created": created_count,
            "skipped_duplicates": skipped_count,
            "flagged_alerts": flagged_count,
            "transactions": persisted_txs,
        }

    @staticmethod
    async def get_account_risk_profile(db: AsyncSession, account_id: str) -> Optional[Dict[str, Any]]:
        """
        Computes the account risk intelligence profile including volume,
        deviation metrics, alert history, and risk distribution.
        """
        acc_stmt = select(Account).where(
            (Account.id == account_id) | (Account.account_number == account_id)
        )
        acc_res = await db.execute(acc_stmt)
        account = acc_res.scalars().first()
        if not account:
            return None

        # Aggregate transaction statistics
        tx_stmt = select(Transaction).where(Transaction.account_id == account.id)
        tx_res = await db.execute(tx_stmt)
        txs = tx_res.scalars().all()

        total_volume = len(txs)
        total_amount = sum(t.amount for t in txs) if txs else 0.0
        avg_amount = total_amount / total_volume if total_volume > 0 else 0.0
        max_amount = max((t.amount for t in txs), default=0.0)

        # Collect risk scores
        scores = []
        high_risk_count = 0
        for t in txs:
            pred_stmt = select(ModelPrediction).where(ModelPrediction.transaction_id == t.id)
            pred_res = await db.execute(pred_stmt)
            pred = pred_res.scalars().first()
            if pred and pred.final_risk_score is not None:
                scores.append(pred.final_risk_score)
                if pred.risk_level in {"high", "critical"}:
                    high_risk_count += 1

        avg_risk = sum(scores) / len(scores) if scores else 0.0
        max_risk = max(scores, default=0.0)

        # Alerts count
        alert_stmt = (
            select(func.count(Alert.id))
            .join(Transaction, Alert.transaction_id == Transaction.id)
            .where(Transaction.account_id == account.id)
        )
        alert_res = await db.execute(alert_stmt)
        alert_count = alert_res.scalar() or 0

        return {
            "account_id": account.account_number,
            "account_internal_id": account.id,
            "holder_name": account.account_holder,
            "balance": account.balance,
            "currency": account.currency,
            "risk_tier": account.risk_tier,
            "total_transactions": total_volume,
            "total_spend": total_amount,
            "average_transaction_amount": round(avg_amount, 2),
            "max_transaction_amount": round(max_amount, 2),
            "average_risk_score": round(avg_risk, 1),
            "peak_risk_score": round(max_risk, 1),
            "high_risk_transactions_count": high_risk_count,
            "total_alerts_count": alert_count,
            "created_at": account.created_at.isoformat() if account.created_at else None,
        }
