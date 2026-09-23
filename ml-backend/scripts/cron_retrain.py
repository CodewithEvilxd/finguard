#!/usr/bin/env python3
"""
FinGuard AI — Standalone 12-Hour Automated Retraining Script.

Usage:
  python scripts/cron_retrain.py

Crontab Configuration Example (Every 12 hours at 00:00 and 12:00):
  0 */12 * * * cd /path/to/ml-backend && .venv/bin/python scripts/cron_retrain.py >> /var/log/finguard_retrain.log 2>&1
"""

import os
import sys
import json
import logging
from datetime import datetime, timezone

# Ensure project root is in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("finguard.cron_retrain")


def main():
    logger.info("=== FinGuard AI Scheduled Retraining Job Started ===")
    start_ts = datetime.now(timezone.utc)
    logger.info(f"Start Timestamp: {start_ts.isoformat()}")

    try:
        from app.training.retrain_manager import retrain_manager

        result = retrain_manager.run_retraining_job(trigger="cron_cli")
        logger.info(f"Retraining Result: {json.dumps(result, indent=2)}")

        if result.get("status") == "completed":
            logger.info("Model training, artifact persistence, and verification succeeded.")
            sys.exit(0)
        else:
            logger.error(f"Retraining failed: {result.get('error')}")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Fatal error during cron retraining execution: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
