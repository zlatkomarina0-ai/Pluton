import logging
import threading
import time

from sqlalchemy.orm import Session

from app.config import settings
from app.dependencies import get_db
from app.services.polling_service import PollingService

logger = logging.getLogger("pluton.scheduler")
logger.setLevel(logging.INFO)


def scheduler_loop(interval_seconds: int = 60):
    if interval_seconds <= 0:
        logger.warning("Scheduler disabled: invalid interval_seconds=%s", interval_seconds)
        return

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
                        logger.info(
                            "Scheduler result sport=%s processed=%d success=%d failure=%d",
                            sport,
                            res["processed_sources"],
                            res["success_count"],
                            res["failure_count"],
                        )
                    except Exception as e:
                        logger.exception("Polling failed for sport=%s: %s", sport, e)
            finally:
                db.close()
        except Exception:
            logger.exception("Scheduler outer exception")
        time.sleep(interval_seconds)


def start_scheduler_in_thread(interval_seconds: int = 60):
    if not settings.ENABLE_SCHEDULER:
        logger.info("Scheduler disabled by settings")
        return None
    if interval_seconds <= 0:
        logger.warning("Scheduler not started because interval_seconds is invalid: %s", interval_seconds)
        return None
    t = threading.Thread(target=scheduler_loop, args=(interval_seconds,), daemon=True)
    t.start()
    return t
