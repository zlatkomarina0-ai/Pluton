from app.phase4 import PHASE_4_TOTAL, PHASE_4_MODULES


class Phase4Validator:
    """Validates the Phase 4 execution framework."""

    @staticmethod
    def get_phase4_status():
        return {
            "phase": 4,
            "status": "implemented",
            "total_modules": PHASE_4_TOTAL,
            "modules_defined": len(PHASE_4_MODULES),
            "runtime_ready": True,
            "focus": [
                "runtime orchestration",
                "scheduler engine",
                "source ingestion",
                "analysis pipeline",
                "monitoring and alerting",
            ],
        }

    @staticmethod
    def validate_registry():
        if PHASE_4_TOTAL != 6:
            raise ValueError(f"Expected 6 Phase 4 modules, found {PHASE_4_TOTAL}")

        expected_codes = {
            "RUNTIME_ORCHESTRATION",
            "SCHEDULER_ENGINE",
            "SOURCE_INGESTION",
            "ANALYSIS_PIPELINE",
            "MONITORING",
            "ALERTING",
        }

        actual_codes = {module.code for module in PHASE_4_MODULES}
        missing = expected_codes - actual_codes
        if missing:
            raise ValueError(f"Missing Phase 4 modules: {sorted(missing)}")

        return True

    @staticmethod
    def list_phase4_modules():
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

    @staticmethod
    def validate_integrity():
        try:
            Phase4Validator.validate_registry()
            return {
                "phase": 4,
                "integrity": "valid",
                "status": "compliant",
                "total_modules": PHASE_4_TOTAL,
            }
        except ValueError as exc:
            return {
                "phase": 4,
                "integrity": "invalid",
                "error": str(exc),
            }


__all__ = ["Phase4Validator"]
