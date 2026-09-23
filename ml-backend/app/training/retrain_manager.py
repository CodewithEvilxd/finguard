"""
Automated Model Retraining Manager for FinGuard AI.
Handles periodic 12-hour automated model training, evaluation, artifact persistence,
hot-reloading into the live inference engine, and run history logging.
"""

import os
import sys
import json
import logging
import threading
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

from app.core.config import ml_settings
from app.inference.engine import inference_engine

logger = logging.getLogger("finguard.retraining")
logger.setLevel(logging.INFO)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
REPORTS_DIR = os.path.join(ROOT_DIR, "training/reports")
HISTORY_FILE = os.path.join(REPORTS_DIR, "retraining_history.json")


class RetrainManager:
    def __init__(self):
        self._lock = threading.Lock()
        self.is_running: bool = False
        self.status: str = "idle"
        self.interval_hours: int = ml_settings.RETRAIN_INTERVAL_HOURS
        self.total_runs: int = 0
        self.last_run_timestamp: Optional[str] = None
        self.next_run_dt: Optional[datetime] = None
        self.latest_metrics: Dict[str, Any] = {}
        self.last_error: Optional[str] = None

        self._init_history()
        self.schedule_next_run()

    def _init_history(self):
        """Loads previous training history from disk if available."""
        os.makedirs(REPORTS_DIR, exist_ok=True)
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    history = json.load(f)
                    if isinstance(history, list) and len(history) > 0:
                        last_entry = history[-1]
                        self.last_run_timestamp = last_entry.get("timestamp")
                        self.total_runs = len(history)
                        self.latest_metrics = last_entry.get("metrics", {})
                        self.status = last_entry.get("status", "idle")
            except Exception as e:
                logger.warning(f"Could not read retraining history from {HISTORY_FILE}: {e}")

    def schedule_next_run(self):
        """Calculates next scheduled execution time."""
        now = datetime.now(timezone.utc)
        if self.last_run_timestamp:
            try:
                last_dt = datetime.fromisoformat(self.last_run_timestamp.replace("Z", "+00:00"))
                target_dt = last_dt + timedelta(hours=self.interval_hours)
                if target_dt > now:
                    self.next_run_dt = target_dt
                    return
            except Exception:
                pass
        self.next_run_dt = now + timedelta(hours=self.interval_hours)

    def should_run(self) -> bool:
        """Determines if a 12-hour scheduled cycle has elapsed."""
        if not ml_settings.ENABLE_AUTO_RETRAINING:
            return False
        if self.is_running:
            return False
        if self.next_run_dt is None:
            return True
        return datetime.now(timezone.utc) >= self.next_run_dt

    def run_retraining_job(self, trigger: str = "scheduled_12h") -> Dict[str, Any]:
        """
        Executes the end-to-end model retraining pipeline:
        1. Trains and evaluates XGBoost classifier.
        2. Trains and evaluates Isolation Forest anomaly detector.
        3. Hot-reloads fresh models into inference_engine in memory.
        4. Logs metrics and updates 12-hour schedule.
        """
        with self._lock:
            if self.is_running:
                return {
                    "status": "already_running",
                    "message": "Retraining job is currently in progress",
                    "started_at": self.last_run_timestamp,
                }
            self.is_running = True
            self.status = "running"
            self.last_error = None

        start_time = datetime.now(timezone.utc)
        run_id = f"RETRAIN-{start_time.strftime('%Y%m%d-%H%M%S')}"
        logger.info(f"Starting automated model retraining run [{run_id}] triggered by: {trigger}")

        try:
            # Ensure ROOT_DIR is in sys.path
            if ROOT_DIR not in sys.path:
                sys.path.insert(0, ROOT_DIR)

            # 1. Train XGBoost
            from training.pipelines.train_xgboost import train_and_evaluate as train_xgb
            logger.info("Executing XGBoost classification retraining...")
            xgb_metrics = train_xgb()

            # 2. Train Isolation Forest
            from training.pipelines.train_isolation_forest import (
                train_and_evaluate_isolation_forest as train_iforest,
            )
            logger.info("Executing Isolation Forest anomaly detector retraining...")
            iforest_metrics = train_iforest()

            # 3. Hot-Reload Models into running Inference Engine
            logger.info("Hot-reloading newly trained models into active inference engine...")
            inference_engine.load_models()

            duration_sec = round((datetime.now(timezone.utc) - start_time).total_seconds(), 2)
            end_time = datetime.now(timezone.utc)

            combined_metrics = {
                "xgboost": {
                    "roc_auc": xgb_metrics.get("metrics", {}).get("roc_auc"),
                    "pr_auc": xgb_metrics.get("metrics", {}).get("pr_auc"),
                    "f1": xgb_metrics.get("metrics", {}).get("f1"),
                    "samples": xgb_metrics.get("training_samples"),
                },
                "isolation_forest": {
                    "contamination": iforest_metrics.get("contamination"),
                    "samples": iforest_metrics.get("training_samples"),
                },
            }

            run_record = {
                "run_id": run_id,
                "timestamp": end_time.isoformat(),
                "trigger": trigger,
                "duration_seconds": duration_sec,
                "status": "completed",
                "metrics": combined_metrics,
            }

            self._append_history(run_record)

            self.status = "completed"
            self.last_run_timestamp = end_time.isoformat()
            self.latest_metrics = combined_metrics
            self.total_runs += 1
            self.next_run_dt = end_time + timedelta(hours=self.interval_hours)
            self.is_running = False

            logger.info(
                f"Retraining run [{run_id}] successfully completed in {duration_sec}s. "
                f"Next automated run scheduled for: {self.next_run_dt.isoformat()}"
            )

            return {
                "status": "completed",
                "run_id": run_id,
                "duration_seconds": duration_sec,
                "timestamp": self.last_run_timestamp,
                "next_scheduled_run": self.next_run_dt.isoformat(),
                "metrics": combined_metrics,
            }

        except Exception as e:
            logger.error(f"Retraining run [{run_id}] failed: {e}", exc_info=True)
            self.status = "failed"
            self.last_error = str(e)
            self.is_running = False
            self.next_run_dt = datetime.now(timezone.utc) + timedelta(hours=1)  # Retry in 1h on error

            failed_record = {
                "run_id": run_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "trigger": trigger,
                "status": "failed",
                "error": str(e),
            }
            self._append_history(failed_record)

            return {
                "status": "failed",
                "run_id": run_id,
                "error": str(e),
            }

    def _append_history(self, record: Dict[str, Any]):
        """Persists run record to history JSON file."""
        try:
            history = []
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    try:
                        history = json.load(f)
                    except Exception:
                        history = []
            history.append(record)
            # Keep last 50 runs
            if len(history) > 50:
                history = history[-50:]
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not append to retraining history: {e}")

    def get_status(self) -> Dict[str, Any]:
        """Returns comprehensive status dictionary for API and UI."""
        return {
            "auto_retraining_enabled": ml_settings.ENABLE_AUTO_RETRAINING,
            "scheduler_interval_hours": self.interval_hours,
            "status": self.status,
            "is_running": self.is_running,
            "last_retrained_at": self.last_run_timestamp,
            "next_scheduled_run": self.next_run_dt.isoformat() if self.next_run_dt else None,
            "total_completed_runs": self.total_runs,
            "latest_metrics": self.latest_metrics,
            "last_error": self.last_error,
        }

    def get_history(self) -> List[Dict[str, Any]]:
        """Returns past training run history."""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []


retrain_manager = RetrainManager()
