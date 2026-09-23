import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_assistant_query_grounded_response():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # First ingest a test transaction
        tx_payload = {
            "transaction_id": "TX-RAG-TEST-001",
            "account_id": "ACC-RAG-999",
            "amount": 85000.0,
            "currency": "USD",
            "transaction_type": "wire",
            "channel": "web",
            "country": "US",
        }
        tx_res = await client.post("/api/v1/transactions", json=tx_payload)
        assert tx_res.status_code == 201

        # Query assistant
        query_payload = {
            "query": "Why was this transaction flagged and what standard operating procedure applies?",
            "transaction_id": "TX-RAG-TEST-001",
        }
        res = await client.post("/api/v1/assistant/query", json=query_payload)
        assert res.status_code == 200
        data = res.json()
        assert "response_text" in data
        assert "query_id" in data
        assert "disclaimer" in data
        assert len(data["response_text"]) > 50
        # Sources should be retrieved
        assert "sources" in data
        assert isinstance(data["sources"], list)
