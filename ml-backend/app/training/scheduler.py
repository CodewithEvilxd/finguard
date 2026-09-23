"""
Background Async Scheduler for 12-Hour Automated Retraining.
Continuously runs in the background of FastAPI without blocking HTTP traffic.
"""

import asyncio
import logging
from typing import Optional

from app.training.retrain_manager import retrain_manager

logger = logging.getLogger("finguard.scheduler")
logger.setLevel(logging.INFO)

_scheduler_task: Optional[asyncio.Task] = None


async def _retraining_loop():
    """Background polling loop that checks every 60 seconds if the 12-hour cycle is due."""
    logger.info(
        f"Automated retraining scheduler initialized. Cycle interval: {retrain_manager.interval_hours} hours. "
        f"Next run at: {retrain_manager.next_run_dt}"
    )

    while True:
        try:
            await asyncio.sleep(60)

            if retrain_manager.should_run():
                logger.info("12-Hour retraining interval reached. Spawning background training job...")
                loop = asyncio.get_running_loop()
                # Run CPU-bound model training in threadpool executor so FastAPI never blocks
                await loop.run_in_executor(None, retrain_manager.run_retraining_job, "scheduled_12h")

        except asyncio.CancelledError:
            logger.info("Automated retraining scheduler task cancelled.")
            break
        except Exception as e:
            logger.error(f"Error in automated retraining scheduler loop: {e}", exc_info=True)
            await asyncio.sleep(60)


def start_scheduler():
    """Starts the 12-hour automated retraining background task."""
    global _scheduler_task
    if _scheduler_task is None or _scheduler_task.done():
        _scheduler_task = asyncio.create_task(_retraining_loop())
        logger.info("Automated 12-hour retraining scheduler background worker started.")


def stop_scheduler():
    """Cancels the automated retraining background task gracefully."""
    global _scheduler_task
    if _scheduler_task and not _scheduler_task.done():
        _scheduler_task.cancel()
        logger.info("Automated 12-hour retraining scheduler background worker stopped.")
