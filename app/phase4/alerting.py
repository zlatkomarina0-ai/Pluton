from typing import Any, Dict


class AlertingService:
    async def send_alert(self, message: str, level: str = "warning") -> Dict[str, Any]:
        return {
            "status": "sent",
            "level": level,
            "message": message,
        }


__all__ = ["AlertingService"]
