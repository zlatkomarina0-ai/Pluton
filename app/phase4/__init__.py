from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Phase4Module:
    code: str
    name: str
    category: str
    description: str
    status: str = "ready"


PHASE_4_MODULES: List[Phase4Module] = [
    Phase4Module(
        code="RUNTIME_ORCHESTRATION",
        name="Runtime orchestration",
        category="runtime",
        description="Coordinates app startup, dependency health, and environment validation.",
    ),
    Phase4Module(
        code="SCHEDULER_ENGINE",
        name="Scheduler engine",
        category="automation",
        description="Schedules periodic refreshes, revalidation loops, and background jobs.",
    ),
    Phase4Module(
        code="SOURCE_INGESTION",
        name="Source ingestion",
        category="data",
        description="Collects and normalizes external sport-data feeds and registry entries.",
    ),
    Phase4Module(
        code="ANALYSIS_PIPELINE",
        name="Analysis pipeline",
        category="analysis",
        description="Builds scores, consensus values, and PLUTON recommendations per fixture.",
    ),
    Phase4Module(
        code="MONITORING",
        name="Monitoring and logging",
        category="ops",
        description="Tracks service health, freshness, source quality, and runtime anomalies.",
    ),
    Phase4Module(
        code="ALERTING",
        name="Alerting",
        category="ops",
        description="Triggers notifications when data quality, freshness, or runtime thresholds are breached.",
    ),
]

PHASE_4_TOTAL = len(PHASE_4_MODULES)
PHASE_4_INDEX = {item.code: item for item in PHASE_4_MODULES}


def get_phase4_modules() -> List[Dict[str, str]]:
    return [
        {
            "code": module.code,
            "name": module.name,
            "category": module.category,
            "description": module.description,
            "status": module.status,
        }
        for module in PHASE_4_MODULES
    ]


def get_phase4_module(code: str) -> Phase4Module | None:
    return PHASE_4_INDEX.get(code)


__all__ = [
    "Phase4Module",
    "PHASE_4_MODULES",
    "PHASE_4_TOTAL",
    "PHASE_4_INDEX",
    "get_phase4_modules",
    "get_phase4_module",
]
