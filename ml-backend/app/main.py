import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, status
from pydantic import BaseModel

from app.core.config import ml_settings
from app.inference.engine import inference_engine
from app.training.retrain_manager import retrain_manager
from app.training.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Launch 12-hour automated model retraining scheduler
    start_scheduler()
    yield
    # Shutdown: Gracefully stop scheduler
    stop_scheduler()


app = FastAPI(
    title="FinGuard AI ML Inference Service",
    version="1.0.0",
    description="Machine learning inference, feature transformations, anomaly detection, explainability, and automated retraining microservice",
    lifespan=lifespan,
)


class TransactionInferenceRequest(BaseModel):
    transaction_id: str
    amount: float
    currency: str = "USD"
    transaction_type: str = "purchase"
    channel: str = "web"
    timestamp: Optional[str] = None
    country: str = "US"
    account_id: str = "ACC-000"


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {
        "status": "healthy",
        "service": "finguard-ml-backend",
        "environment": ml_settings.ENVIRONMENT,
        "scheduler_enabled": ml_settings.ENABLE_AUTO_RETRAINING,
        "retrain_interval_hours": ml_settings.RETRAIN_INTERVAL_HOURS,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/ready", status_code=status.HTTP_200_OK)
async def ready():
    return {
        "status": "ready",
        "service": "finguard-ml-backend",
        "models_loaded": True,
        "active_version": inference_engine.model_version,
    }


@app.get("/models")
async def get_models():
    return {
        "active_models": [
            {
                "name": "xgboost-fraud-classifier",
                "type": "supervised",
                "version": "v1.0",
                "status": "active",
            },
            {
                "name": "isolation-forest-anomaly-detector",
                "type": "unsupervised",
                "version": "v1.0",
                "status": "active",
            },
            {
                "name": "deterministic-business-rules",
                "type": "rules",
                "version": "v1.0",
                "status": "active",
            },
        ],
        "retraining_schedule": {
            "frequency": f"Every {retrain_manager.interval_hours} hours",
            "status": retrain_manager.status,
            "last_retrained_at": retrain_manager.last_run_timestamp,
            "next_scheduled_run": retrain_manager.next_run_dt.isoformat() if retrain_manager.next_run_dt else None,
        },
    }


@app.get("/training/status", status_code=status.HTTP_200_OK)
async def get_training_status():
    """Returns real-time status of the 12-hour automated model retraining system."""
    return retrain_manager.get_status()


@app.get("/training/history", status_code=status.HTTP_200_OK)
async def get_training_history():
    """Returns past retraining run history logs with metrics and timestamps."""
    return {
        "history": retrain_manager.get_history(),
        "total_runs": retrain_manager.total_runs,
    }


@app.post("/training/retrain", status_code=status.HTTP_202_ACCEPTED)
async def trigger_retrain(background_tasks: BackgroundTasks):
    """
    Triggers an immediate model retraining run in the background.
    Hot-reloads the active models once training completes.
    """
    if retrain_manager.is_running:
        return {
            "status": "in_progress",
            "message": "Model retraining is already running in the background",
            "current_status": retrain_manager.get_status(),
        }

    # Execute in background thread so HTTP call returns immediately with 202 Accepted
    loop = asyncio.get_running_loop()

    def run_job():
        retrain_manager.run_retraining_job(trigger="api_manual")

    background_tasks.add_task(loop.run_in_executor, None, run_job)

    return {
        "status": "initiated",
        "message": "Automated model retraining successfully initiated in background",
        "interval_hours": retrain_manager.interval_hours,
        "check_status_url": "/training/status",
    }


@app.post("/predict", status_code=status.HTTP_200_OK)
async def predict(payload: TransactionInferenceRequest):
    try:
        result = inference_engine.predict(payload.model_dump())
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(e)}",
        )


@app.post("/batch-predict", status_code=status.HTTP_200_OK)
async def batch_predict(transactions: List[TransactionInferenceRequest]):
    results = []
    for tx in transactions:
        results.append(inference_engine.predict(tx.model_dump()))
    return {"predictions": results, "count": len(results)}


@app.get("/")
async def root():
    return {
        "service": "FinGuard AI ML Inference Service",
        "status": "operational",
        "retraining": {
            "schedule": f"Every {retrain_manager.interval_hours} hours",
            "status_endpoint": "/training/status",
            "trigger_endpoint": "/training/retrain",
        },
        "health": "/health",
        "models": "/models",
    }
