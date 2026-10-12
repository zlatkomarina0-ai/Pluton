from typing import Any, Dict


class SchedulerService:
    def get_schedule(self) -> Dict[str, Any]:
        return {
            "status": "configured",
            "jobs": [
                "refresh_sources",
                "sync_fixtures",
                "run_analysis",
                "healthcheck",
            ],
            "intervals": {
                "refresh_sources": "300s",
                "sync_fixtures": "600s",
                "run_analysis": "900s",
                "healthcheck": "60s",
            },
        }


__all__ = ["SchedulerService"]
