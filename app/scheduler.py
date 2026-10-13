import logging
import threading
import time
from datetime import timedelta

from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.services.polling_service import PollingService

logger = logging.getLogger("pluton.scheduler")
logger.setLevel(logging.INFO)


def scheduler_loop(interval_seconds: int = 60):
    """
    Simple scheduler loop that polls all active sports every interval_seconds.
    This is intentionally simple and error-safe: exceptions are caught and logged.
    """
    # define the sports you want to poll automatically
    sports = ["football", "basketball", "handball"]
    while True:
        try:
            db: Session = next(get_db())
            try:
                service = PollingService(db)
                for sport in sports:
                    logger.info("Scheduler polling sport=%s", sport)
                    try:
                        res = service.poll_sport(sport)
                        logger.info("Scheduler result sport=%s processed=%d success=%d failure=%d", sport, res["processed_sources"], res["success_count"], res["failure_count"])
                    except Exception as e:
                        logger.exception("Polling failed for sport=%s: %s", sport, e)
            finally:
                db.close()
        except Exception:
            logger.exception("Scheduler outer exception")
        time.sleep(interval_seconds)


def start_scheduler_in_thread(interval_seconds: int = 60):
    t = threading.Thread(target=scheduler_loop, args=(interval_seconds,), daemon=True)
    t.start()
    return t
