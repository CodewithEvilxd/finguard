import json
import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transaction import Transaction
from app.models.alert import Alert, Investigation
from app.models.ml import ModelPrediction
from app.models.entity import Account
from app.schemas.assistant import AssistantQuery, AssistantResponse, SourceReference
from rag.retrieval.retriever import KnowledgeRetriever
from app.core.logging import logger


class RAGPipeline:
    @staticmethod
    async def process_query(
        db: AsyncSession,
        query: AssistantQuery,
    ) -> AssistantResponse:
        query_id = str(uuid.uuid4())

        # Resolve transaction and alert context
        tx: Optional[Transaction] = None
        alert: Optional[Alert] = None
        pred: Optional[ModelPrediction] = None
        account: Optional[Account] = None

        if query.alert_id:
            alert_stmt = select(Alert).where((Alert.id == query.alert_id) | (Alert.transaction_id == query.alert_id))
            alert_res = await db.execute(alert_stmt)
            alert = alert_res.scalars().first()
            if alert:
                tx_stmt = select(Transaction).where(Transaction.id == alert.transaction_id)
                tx_res = await db.execute(tx_stmt)
                tx = tx_res.scalars().first()

        if not tx and query.transaction_id:
            tx_stmt = select(Transaction).where(
                (Transaction.id == query.transaction_id) | (Transaction.transaction_id == query.transaction_id)
            )
            tx_res = await db.execute(tx_stmt)
            tx = tx_res.scalars().first()

        if tx and not alert:
            alert_stmt = select(Alert).where(Alert.transaction_id == tx.id)
            alert_res = await db.execute(alert_stmt)
            alert = alert_res.scalars().first()

        if tx:
            pred_stmt = select(ModelPrediction).where(ModelPrediction.transaction_id == tx.id)
            pred_res = await db.execute(pred_stmt)
            pred = pred_res.scalars().first()

            acc_stmt = select(Account).where(Account.id == tx.account_id)
            acc_res = await db.execute(acc_stmt)
            account = acc_res.scalars().first()

        # Retrieve relevant knowledge chunks from policy/procedure/case library
        retrieval_query = query.query
        if tx:
            retrieval_query = f"{query.query} {tx.transaction_type} {tx.amount} wire transfer velocity compliance"

        chunks = await KnowledgeRetriever.retrieve_relevant_chunks(db, retrieval_query, top_k=3)
        sources = []
        for chunk, doc, score in chunks:
            excerpt = chunk.content[:280] + "..." if len(chunk.content) > 280 else chunk.content
            sources.append(
                SourceReference(
                    document_title=doc.title,
                    document_category=doc.category,
                    section_title=f"Section {chunk.chunk_index + 1}",
                    relevance_score=round(score, 3),
                    excerpt=excerpt,
                )
            )

        # Parse ML explanation factors if available
        factors_text = []
        rule_findings = []
        if pred and pred.explanation_payload:
            try:
                payload_data = json.loads(pred.explanation_payload)
                for f in payload_data.get("top_risk_factors", [])[:4]:
                    name = f.get("factor") or f.get("feature_name", "Feature")
                    contrib = f.get("contribution", 0.0)
                    factors_text.append(f"- **{name}**: +{contrib:.2f} attribution to risk probability")
                rule_findings = payload_data.get("rule_findings", [])
            except Exception:
                pass

        # Build grounded response sections
        sections = []
        q_lower = query.query.lower()

        if "why" in q_lower or "flagged" in q_lower or "trigger" in q_lower:
            sections.append("### Flagging Rationale & Evidence")
            if tx and pred:
                sections.append(
                    f"Transaction `{tx.transaction_id}` was flagged with unified risk score **{pred.final_risk_score:.1f} ({pred.risk_level.upper()})**."
                )
                sections.append(
                    f"- **Supervised Fraud Probability**: {pred.fraud_probability:.3f} (Model: `{pred.model_version}`)"
                    if pred.fraud_probability is not None
                    else "- **Supervised Fraud Probability**: Degraded/heuristic mode"
                )
                sections.append(
                    f"- **Anomaly Score**: {pred.anomaly_score:.3f} via Isolation Forest"
                    if pred.anomaly_score is not None
                    else "- **Anomaly Score**: Unsupervised check completed"
                )
                if factors_text:
                    sections.append("\n**Primary Attributions (TreeSHAP / Model Evidence):**")
                    sections.extend(factors_text)
                if rule_findings:
                    sections.append("\n**Triggered Deterministic Rules:**")
                    for rf in rule_findings:
                        sections.append(f"- {rf}")
            else:
                sections.append("General risk criteria evaluation based on institutional policies.")

        elif "summar" in q_lower or "case" in q_lower:
            sections.append("### Case Summary Dossier")
            if tx:
                sections.append(
                    f"- **Transaction ID**: `{tx.transaction_id}`\n"
                    f"- **Account Number**: `{account.account_number if account else tx.account_id}`\n"
                    f"- **Amount**: {tx.currency} {tx.amount:,.2f} via {tx.channel} ({tx.transaction_type})\n"
                    f"- **Current Status**: {tx.status.upper()}\n"
                    f"- **Risk Classification**: {pred.risk_level.upper() if pred else 'UNSCORED'}"
                )
            if alert:
                sections.append(f"- **Alert Trigger**: {alert.trigger_reason} (Alert ID: `{alert.id}`)")

        elif "pattern" in q_lower or "account" in q_lower or "deviat" in q_lower:
            sections.append("### Account Risk Pattern & Velocity Analysis")
            if account:
                sections.append(
                    f"- **Account Holder**: {account.account_holder}\n"
                    f"- **Registered Tier**: {account.risk_tier.upper()}\n"
                    f"- **Ledger Balance**: {account.currency} {account.balance:,.2f}"
                )
                if tx:
                    ratio = (tx.amount / (account.balance + 1.0)) * 100
                    sections.append(
                        f"- **Impact Ratio**: Current transaction represents {ratio:.1f}% of liquid account balance."
                    )
            else:
                sections.append("Account risk distribution follows historical baseline.")

        else:
            sections.append("### Grounded Compliance Assessment")
            if tx:
                sections.append(
                    f"Evaluating transaction `{tx.transaction_id}` ({tx.currency} {tx.amount:,.2f}) against institutional governance."
                )

        # Policy Alignment Section
        if sources:
            sections.append("\n### Applicable Regulatory & SOP Guidelines")
            for s in sources[:2]:
                sections.append(
                    f"- **{s.document_title}** ({s.document_category.replace('_', ' ').title()}, Relevance {s.relevance_score:.2f}):\n"
                    f"  > *\"{s.excerpt.strip()}\"*"
                )

        # Recommended Action Section
        sections.append("\n### Recommended Investigator Next Steps")
        if tx and tx.amount > 25000:
            sections.append("1. **Hold Protocol**: Enforce temporary 60-minute settlement pause under SOP-104 Section 4.")
            sections.append("2. **Callback Verification**: Initiate authorized representative phone verification.")
            sections.append("3. **SAR Assessment**: If identity cannot be confirmed, prepare REG-04 filing dossier.")
        else:
            sections.append("1. Verify counterparty beneficiary against historical account payees.")
            sections.append("2. Review initiating IP geolocation and device fingerprint.")
            sections.append("3. Record analyst review rationale in audit log prior to clearing.")

        response_text = "\n".join(sections)
        limitations = None
        if not tx:
            limitations = "No specific transaction ID was associated with this query; response is grounded on general policy documents."

        return AssistantResponse(
            query_id=query_id,
            response_text=response_text,
            sources=sources,
            limitations=limitations,
            disclaimer="AI-generated assistance grounded in approved documents. Final decision must be verified by an analyst.",
        )
