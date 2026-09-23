import uuid
import pytest


@pytest.mark.asyncio
async def test_batch_transaction_ingestion(client):
    tx1 = f"TX-BATCH-{uuid.uuid4().hex[:6]}"
    tx2 = f"TX-BATCH-{uuid.uuid4().hex[:6]}"
    batch_payload = {
        "transactions": [
            {
                "transaction_id": tx1,
                "account_id": "ACC-CORP-99",
                "amount": 1500.0,
                "currency": "USD",
                "transaction_type": "purchase",
                "channel": "web",
                "country": "US",
            },
            {
                "transaction_id": tx2,
                "account_id": "ACC-CORP-99",
                "amount": 75000.0,
                "currency": "USD",
                "transaction_type": "wire",
                "channel": "web",
                "country": "US",
            },
        ]
    }
    res = await client.post("/api/v1/transactions/batch", json=batch_payload)
    assert res.status_code == 201
    data = res.json()
    assert data["total_received"] == 2
    assert data["created"] == 2
    assert len(data["items"]) == 2

    # Idempotency re-run test
    res_dup = await client.post("/api/v1/transactions/batch", json=batch_payload)
    assert res_dup.status_code == 201
    data_dup = res_dup.json()
    assert data_dup["skipped_duplicates"] == 2


@pytest.mark.asyncio
async def test_account_intelligence_endpoints(client):
    # List accounts
    res = await client.get("/api/v1/accounts")
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert len(data["items"]) > 0

    account_id = data["items"][0]["account_number"]

    # Account risk profile
    risk_res = await client.get(f"/api/v1/accounts/{account_id}/risk")
    assert risk_res.status_code == 200
    risk_data = risk_res.json()
    assert risk_data["account_id"] == account_id
    assert "average_risk_score" in risk_data
    assert "total_transactions" in risk_data


@pytest.mark.asyncio
async def test_investigations_list_and_detail(client):
    res = await client.get("/api/v1/investigations")
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert "total" in data
