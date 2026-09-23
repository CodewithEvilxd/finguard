import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_ml_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"
        assert data["service"] == "finguard-ml-backend"


@pytest.mark.asyncio
async def test_low_risk_prediction():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "transaction_id": "TXN-LOW-001",
            "amount": 45.0,
            "currency": "USD",
            "transaction_type": "purchase",
            "channel": "pos",
            "country": "US",
            "account_id": "ACC-100",
        }
        res = await client.post("/predict", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["final_risk_score"] < 40.0
        assert data["risk_level"] == "low"
        assert "explanation_payload" in data


@pytest.mark.asyncio
async def test_high_risk_wire_prediction():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "transaction_id": "TXN-HIGH-002",
            "amount": 85000.0,
            "currency": "USD",
            "transaction_type": "wire",
            "channel": "web",
            "country": "KY",  # Cayman Islands / offshore
            "account_id": "ACC-100",
        }
        res = await client.post("/predict", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["final_risk_score"] >= 65.0
        assert data["risk_level"] in {"high", "critical"}
        assert data["rule_score"] > 0
