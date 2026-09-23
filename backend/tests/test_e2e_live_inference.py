import json
import uuid
import pytest
from sqlalchemy import select
from app.models.audit import AuditLog
from app.services.ml_client import ml_client


@pytest.mark.asyncio
async def test_complete_end_to_end_investigation_lifecycle(client, db_session):
    """
    Validates the 12-step DEMO REQUIREMENT workflow:
    1. Verify real trained model is live on ML backend.
    2. Submit transaction to backend API.
    3. Real feature extraction and ML inference occurs.
    4. Real anomaly score generated.
    5. Real risk score computed (0-100).
    6. Real TreeSHAP explanation generated.
    7. Automated alert created by backend logic.
    8. Analyst opens investigation dossier.
    9. AI assistant retrieves grounded context without hallucinating facts.
    10. Human decision recorded.
    11. Immutable audit trail generated.
    """
    # 1. Health check ML service
    ml_health = await ml_client.check_health()
    assert ml_health["status"] in {"ready", "healthy"}
    assert ml_health["models_loaded"] is True
    assert "xgboost" in ml_health["active_version"]

    tx_id = f"TX-E2E-LIVE-{uuid.uuid4().hex[:8]}"
    tx_payload = {
        "transaction_id": tx_id,
        "account_id": "ACC-100482",
        "amount": 84500.0,
        "currency": "USD",
        "transaction_type": "wire",
        "channel": "web",
        "country": "KY",
    }
    tx_res = await client.post("/api/v1/transactions", json=tx_payload)
    assert tx_res.status_code == 201
    tx_data = tx_res.json()

    # 3 - 6. Verify real ML scoring, fraud probability, anomaly score, and TreeSHAP factors
    assert tx_data["risk_score"] is not None
    assert tx_data["risk_score"] >= 80.0
    assert tx_data["risk_level"] == "critical"
    assert tx_data["fraud_probability"] is not None
    assert tx_data["fraud_probability"] > 0.50
    assert tx_data["anomaly_score"] is not None
    assert tx_data["model_version"] == "finguard-xgboost-v1.0.0"

    # Verify explanation payload contains TreeSHAP attributions
    explanation = json.loads(tx_data["explanation_payload"])
    assert "top_risk_factors" in explanation
    assert len(explanation["top_risk_factors"]) > 0

    # 7. Verify automated alert creation
    alert_res = await client.get("/api/v1/alerts")
    assert alert_res.status_code == 200
    alerts = alert_res.json()["items"]
    matched_alert = next(
        (a for a in alerts if a["transaction_id"] in {tx_data["id"], tx_data["transaction_id"]}),
        None,
    )
    assert matched_alert is not None
    assert matched_alert["risk_level"] == "critical"

    # 8. Analyst opens investigation
    inv_payload = {
        "alert_id": matched_alert["id"],
        "priority": "urgent",
        "initial_notes": "Unrecognized offshore IP initiating high magnitude corporate wire.",
    }
    inv_res = await client.post("/api/v1/investigations", json=inv_payload)
    assert inv_res.status_code == 201
    inv_data = inv_res.json()
    assert inv_data["status"] == "open"
    assert inv_data["priority"] == "urgent"

    # 9. AI assistant grounded policy retrieval
    rag_query = {
        "query": "Why was this transaction flagged and what standard operating procedure applies?",
        "transaction_id": tx_data["id"],
        "alert_id": matched_alert["id"],
    }
    assistant_res = await client.post("/api/v1/assistant/query", json=rag_query)
    assert assistant_res.status_code == 200
    rag_data = assistant_res.json()
    assert "Flagging Rationale & Evidence" in rag_data["response_text"]
    assert "Supervised Fraud Probability" in rag_data["response_text"]
    assert len(rag_data["sources"]) > 0
    assert "disclaimer" in rag_data

    # 10. Human analyst decision sign-off
    decision_payload = {
        "decision": "confirmed_fraud",
        "rationale": "Contacted authorized controller under SOP-104 Section 2. Confirmed credentials compromised; wire halted.",
    }
    dec_res = await client.post(
        f"/api/v1/investigations/{inv_data['id']}/decision",
        json=decision_payload,
    )
    assert dec_res.status_code == 200
    dec_data = dec_res.json()
    assert dec_data["decision"] == "confirmed_fraud"
    assert dec_data["status"] in {"confirmed_fraud", "closed"}

    # 11. Immutable audit trail verification
    audit_stmt = select(AuditLog).where(
        AuditLog.entity_id == inv_data["id"]
    )
    audit_records = (await db_session.execute(audit_stmt)).scalars().all()
    assert len(audit_records) > 0
    assert any("INVESTIGATION_DECIDED" in a.action for a in audit_records)
