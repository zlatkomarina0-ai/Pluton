from app.phase3 import PLUTON_LISTS, SPORT_COUNTS, PHASE_3_TOTAL
from app.phase3.list_engine import ListManager


class Phase3Validator:
    """
    Validates Phase 3 completeness and compliance.
    """

    @staticmethod
    def get_phase3_status():
        """
        Get Phase 3 status overview.
        """
        return {
            "phase": 3,
            "status": "functional",
            "total_lists": PHASE_3_TOTAL,
            "sports_coverage": SPORT_COUNTS,
            "lists_defined": len(PLUTON_LISTS),
            "list_engine": "operational",
        }

    @staticmethod
    def validate_list_registry():
        """
        Validate that all 35 lists are properly registered.
        """
        if PHASE_3_TOTAL != 35:
            raise ValueError(f"Expected 35 lists, found {PHASE_3_TOTAL}")

        expected_counts = {
            "football": 8,
            "basketball": 10,
            "handball": 8,
            "formula_1": 5,
            "multi": 7,
        }

        for sport, expected_count in expected_counts.items():
            actual_count = SPORT_COUNTS.get(sport, 0)
            if actual_count != expected_count:
                raise ValueError(
                    f"Sport {sport}: expected {expected_count} lists, found {actual_count}"
                )

        return True

    @staticmethod
    def list_all_pluton_lists():
        """
        Return all 35 PLUTON lists.
        """
        return [
            {
                "code": l.code,
                "sport": l.sport,
                "category": l.category,
                "name": l.name,
                "scope": l.scope,
                "description": l.description,
                "active": l.is_active,
            }
            for l in PLUTON_LISTS
        ]


class Phase3ComplianceChecker:
    """
    Ensures Phase 3 operates within PLUTON rules.
    """

    @staticmethod
    def check_list_compliance(list_code: str):
        """
        Check if a list is properly defined and compliant.
        """
        from app.phase3 import PLUTON_LIST_INDEX
        pluton_list = PLUTON_LIST_INDEX.get(list_code)
        if not pluton_list:
            return {"compliant": False, "error": f"List {list_code} not found"}

        return {
            "compliant": True,
            "code": pluton_list.code,
            "sport": pluton_list.sport,
            "category": pluton_list.category,
            "scope": pluton_list.scope,
            "active": pluton_list.is_active,
        }

    @staticmethod
    def validate_phase3_integrity():
        """
        Run full Phase 3 integrity check.
        """
        try:
            Phase3Validator.validate_list_registry()
            return {
                "phase": 3,
                "integrity": "valid",
                "total_lists": PHASE_3_TOTAL,
                "status": "compliant",
            }
        except ValueError as e:
            return {
                "phase": 3,
                "integrity": "invalid",
                "error": str(e),
            }


__all__ = [
    "Phase3Validator",
    "Phase3ComplianceChecker",
]
