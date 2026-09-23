import json
from typing import Any, Dict, List, Optional
import httpx
from app.core.config import settings
from app.core.logging import logger


class MLServiceClient:
    """
    HTTP client for FinGuard AI ML Inference Service.
    Handles communication with ml-backend (default port 8001),
    with robust error handling and deterministic fallback for degraded offline mode.
    """

    def __init__(self, base_url: str = settings.ML_SERVICE_URL):
        self.base_url = base_url.rstrip("/")

    async def check_health(self) -> Dict[str, Any]:
        """Checks if the ML microservice is online and models are loaded."""
        url = f"{self.base_url}/ready"
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            logger.debug(f"ML service health check failed ({url}): {str(e)}")
        return {
            "status": "offline",
            "service": "finguard-ml-backend",
            "models_loaded": False,
            "active_version": "none",
        }

    async def predict_transaction(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submits a transaction payload to the ML backend for:
        - 17-feature extraction
        - Supervised XGBoost fraud classification
        - Unsupervised Isolation Forest anomaly detection
        - Deterministic rule checks
        - Unified risk score computation (0-100)
        - Native TreeSHAP feature attributions
        """
        url = f"{self.base_url}/predict"
        payload = {
            "transaction_id": str(transaction_data.get("transaction_id", "")),
            "amount": float(transaction_data.get("amount", 0.0)),
            "currency": str(transaction_data.get("currency", "USD")),
            "transaction_type": str(transaction_data.get("transaction_type", "purchase")),
            "channel": str(transaction_data.get("channel", "web")),
            "timestamp": str(transaction_data.get("timestamp", "")) if transaction_data.get("timestamp") else None,
            "country": str(transaction_data.get("country", "US")),
            "account_id": str(transaction_data.get("account_id", "ACC-000")),
        }

        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                response = await client.post(url, json=payload)
                if response.status_code == 200:
                    return response.json()
                logger.warning(
                    f"ML service returned non-200 status {response.status_code}: {response.text}"
                )
        except httpx.ConnectError:
            logger.warning(f"ML service offline at {url}. Using deterministic rule fallback.")
        except Exception as e:
            logger.warning(f"ML service call failed ({url}): {str(e)}. Using deterministic rule fallback.")

        return self._generate_fallback_prediction(transaction_data)

    async def predict_batch(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Submits a batch of transactions for bulk ML inference."""
        url = f"{self.base_url}/batch-predict"
        formatted_list = [
            {
                "transaction_id": str(t.get("transaction_id", "")),
                "amount": float(t.get("amount", 0.0)),
                "currency": str(t.get("currency", "USD")),
                "transaction_type": str(t.get("transaction_type", "purchase")),
                "channel": str(t.get("channel", "web")),
                "timestamp": str(t.get("timestamp", "")) if t.get("timestamp") else None,
                "country": str(t.get("country", "US")),
                "account_id": str(t.get("account_id", "ACC-000")),
            }
            for t in transactions
        ]

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, json=formatted_list)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("predictions", [])
                logger.warning(f"ML batch-predict returned status {response.status_code}")
        except Exception as e:
            logger.warning(f"ML batch-predict call failed: {str(e)}. Falling back to individual fallback scoring.")

        return [self._generate_fallback_prediction(t) for t in transactions]

    async def get_training_status(self) -> Dict[str, Any]:
        """Queries the current automated 12-hour retraining status from ml-backend."""
        url = f"{self.base_url}/training/status"
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.get(url)
                if res.status_code == 200:
                    return res.json()
        except Exception as e:
            logger.debug(f"Failed to fetch ML training status ({url}): {e}")
        return {
            "auto_retraining_enabled": True,
            "scheduler_interval_hours": 12,
            "status": "idle",
            "is_running": False,
            "last_retrained_at": None,
            "next_scheduled_run": None,
            "total_completed_runs": 0,
        }

    async def trigger_retraining(self) -> Dict[str, Any]:
        """Triggers an immediate model retraining run on the ML microservice."""
        url = f"{self.base_url}/training/retrain"
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.post(url)
                if res.status_code in [200, 202]:
                    return res.json()
        except Exception as e:
            logger.error(f"Failed to trigger ML retraining ({url}): {e}")
        return {"status": "error", "message": "ML microservice unreachable"}

    def _generate_fallback_prediction(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Safe deterministic fallback when ML microservice is initializing or offline."""
        amount = float(transaction_data.get("amount", 0.0))
        tx_type = str(transaction_data.get("transaction_type", "purchase")).lower()
        channel = str(transaction_data.get("channel", "web")).lower()
        rule_score = 0.0
        factors = []

        if amount > 10000.0:
            rule_score += 45.0
            factors.append({
                "factor": "High single transaction amount",
                "feature_name": "TransactionAmt",
                "contribution": 0.45,
                "importance_rank": 1,
            })
        if tx_type == "wire":
            rule_score += 25.0
            factors.append({
                "factor": "Wire transfer velocity check",
                "feature_name": "transaction_type",
                "contribution": 0.25,
                "importance_rank": 2,
            })
        if channel == "atm" and amount > 2000.0:
            rule_score += 20.0
            factors.append({
                "factor": "High ATM cash withdrawal exceeding threshold",
                "feature_name": "channel",
                "contribution": 0.20,
                "importance_rank": 3,
            })

        final_score = min(rule_score, 100.0)
        risk_level = "low"
        if final_score >= 80:
            risk_level = "critical"
        elif final_score >= 60:
            risk_level = "high"
        elif final_score >= 35:
            risk_level = "medium"

        explanation_payload = {
            "top_risk_factors": factors,
            "rule_findings": [f["factor"] for f in factors],
            "scoring_breakdown": {
                "supervised_component": 0.0,
                "unsupervised_component": 0.0,
                "rule_component": final_score,
                "weights": {"supervised": 0.50, "unsupervised": 0.30, "rules": 0.20},
            },
            "models_used": {
                "classifier": "none (offline fallback)",
                "anomaly_detector": "none (offline fallback)",
            },
            "mode": "degraded_fallback",
        }

        return {
            "transaction_id": transaction_data.get("transaction_id"),
            "fraud_probability": None,
            "anomaly_score": None,
            "rule_score": rule_score,
            "final_risk_score": final_score,
            "risk_level": risk_level,
            "model_version": "fallback-v1.0",
            "feature_version": "fallback-v1.0",
            "scoring_version": "deterministic-fallback",
            "explanation_payload": json.dumps(explanation_payload),
        }


ml_client = MLServiceClient()
