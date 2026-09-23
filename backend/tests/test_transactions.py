import uuid
import pytest


@pytest.mark.asyncio
async def test_transaction_ingestion_and_idempotency(client):
    tx_payload = {
        "transaction_id": "TEST-TXN-1001",
        "account_id": "ACC-TEST-001",
        "amount": 1500.0,
        "currency": "USD",
        "transaction_type": "purchase",
        "channel": "web",
    }

    # First ingestion
    res1 = await client.post("/api/v1/transactions", json=tx_payload)
    assert res1.status_code == 201
    data1 = res1.json()
    assert data1["transaction_id"] == "TEST-TXN-1001"
    assert data1["amount"] == 1500.0
    assert data1["status"] in {"completed", "flagged"}

    # Second ingestion with identical idempotency key must NOT duplicate
    res2 = await client.post("/api/v1/transactions", json=tx_payload)
    assert res2.status_code == 201
    data2 = res2.json()
    assert data2["id"] == data1["id"]
    assert data2["transaction_id"] == "TEST-TXN-1001"

    # Query list
    list_res = await client.get("/api/v1/transactions")
    assert list_res.status_code == 200
    list_data = list_res.json()
    assert list_data["total"] == 1


@pytest.mark.asyncio
async def test_high_risk_transaction_creates_alert(client):
    tx_id = f"TEST-WIRE-{uuid.uuid4().hex[:6]}"
    high_risk_payload = {
        "transaction_id": tx_id,
        "account_id": "ACC-TEST-002",
        "amount": 85000.0,
        "currency": "USD",
        "transaction_type": "wire",
        "channel": "web",
        "country": "KY",
    }

    res = await client.post("/api/v1/transactions", json=high_risk_payload)
    assert res.status_code == 201
    data = res.json()
    assert data["risk_score"] is not None
    assert data["risk_score"] >= 60.0

    # Verify alert exists
    alert_res = await client.get("/api/v1/alerts")
    assert alert_res.status_code == 200
    alert_data = alert_res.json()
    assert alert_data["total"] >= 1
    assert any(a["transaction_id"] == tx_id for a in alert_data["items"])
