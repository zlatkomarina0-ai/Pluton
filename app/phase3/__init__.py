from dataclasses import dataclass
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models import Fixture, League, Season, Team


@dataclass(frozen=True)
class PlutonList:
    code: str
    sport: str
    category: str
    name: str
    scope: str
    description: str
    source: str = "internal"
    is_active: bool = True


FOOTBALL_LISTS: List[PlutonList] = [
    PlutonList(
        code="FB_BIG_TABLE",
        sport="football",
        category="league",
        name="Big Table",
        scope="global",
        description="Main standings table across all active football leagues.",
    ),
    PlutonList(
        code="FB_MATCHES_SUGGESTIONS",
        sport="football",
        category="matches",
        name="Matches with Suggestions",
        scope="global",
        description="Fixture list with prediction suggestions and context for each match.",
    ),
    PlutonList(
        code="FB_LEAGUE_STANDINGS",
        sport="football",
        category="league",
        name="League Standings",
        scope="league",
        description="Per-league table with ranking and points progression.",
    ),
    PlutonList(
        code="FB_LEAGUE_FIXTURES",
        sport="football",
        category="fixtures",
        name="League Fixtures",
        scope="league",
        description="Scheduled fixtures for each football competition.",
    ),
    PlutonList(
        code="FB_CL_TABLE",
        sport="football",
        category="continental",
        name="Champions League Table",
        scope="competition",
        description="Table for Champions League group and knockout stages.",
    ),
    PlutonList(
        code="FB_CL_MATCHES",
        sport="football",
        category="continental",
        name="Champions League Matches",
        scope="competition",
        description="List of all Champions League fixtures and match states.",
    ),
    PlutonList(
        code="FB_NATIONS_LEAGUE",
        sport="football",
        category="national",
        name="National Teams — Nations League",
        scope="nation",
        description="Nations League list for national teams and fixtures.",
    ),
    PlutonList(
        code="FB_QUALIFIERS",
        sport="football",
        category="national",
        name="National Teams — Qualifiers",
        scope="nation",
        description="National team qualifiers and qualification tables.",
    ),
]

BASKETBALL_LISTS: List[PlutonList] = [
    PlutonList(
        code="BK_BIG_TABLE",
        sport="basketball",
        category="league",
        name="Big Table",
        scope="global",
        description="Main standings table across all active basketball leagues.",
    ),
    PlutonList(
        code="BK_MATCHES_SUGGESTIONS",
        sport="basketball",
        category="matches",
        name="Matches with Suggestions",
        scope="global",
        description="Basketball fixture list enriched with suggestions and match context.",
    ),
    PlutonList(
        code="BK_LEAGUE_STANDINGS",
        sport="basketball",
        category="league",
        name="League Standings",
        scope="league",
        description="Per-league table for basketball competitions.",
    ),
    PlutonList(
        code="BK_LEAGUE_FIXTURES",
        sport="basketball",
        category="fixtures",
        name="League Fixtures",
        scope="league",
        description="Scheduled basketball fixture list per league.",
    ),
    PlutonList(
        code="BK_CL_TABLE",
        sport="basketball",
        category="continental",
        name="Champions League Table",
        scope="competition",
        description="European club competition table and positions.",
    ),
    PlutonList(
        code="BK_CL_MATCHES",
        sport="basketball",
        category="continental",
        name="Champions League Matches",
        scope="competition",
        description="European club competition match list and statuses.",
    ),
    PlutonList(
        code="BK_NATIONS_LEAGUE",
        sport="basketball",
        category="national",
        name="National Teams — Nations League",
        scope="nation",
        description="National team competition structure and fixtures.",
    ),
    PlutonList(
        code="BK_QUALIFIERS",
        sport="basketball",
        category="national",
        name="National Teams — Qualifiers",
        scope="nation",
        description="Basketball national qualifiers and qualification tables.",
    ),
    PlutonList(
        code="BK_NBA_RESULTS",
        sport="basketball",
        category="league",
        name="NBA Results",
        scope="league",
        description="NBA game results and outcomes.",
    ),
    PlutonList(
        code="BK_NBA_STANDINGS",
        sport="basketball",
        category="league",
        name="NBA Standings",
        scope="league",
        description="NBA league standings and rankings.",
    ),
]

HANDBALL_LISTS: List[PlutonList] = [
    PlutonList(
        code="HB_BIG_TABLE",
        sport="handball",
        category="league",
        name="Big Table",
        scope="global",
        description="Main standings table across active handball leagues.",
    ),
    PlutonList(
        code="HB_MATCHES_SUGGESTIONS",
        sport="handball",
        category="matches",
        name="Matches with Suggestions",
        scope="global",
        description="Handball fixture list with predicted context and suggestions.",
    ),
    PlutonList(
        code="HB_LEAGUE_STANDINGS",
        sport="handball",
        category="league",
        name="League Standings",
        scope="league",
        description="Per-league standing table for handball competitions.",
    ),
    PlutonList(
        code="HB_LEAGUE_FIXTURES",
        sport="handball",
        category="fixtures",
        name="League Fixtures",
        scope="league",
        description="Handball fixtures and scheduling list.",
    ),
    PlutonList(
        code="HB_CL_TABLE",
        sport="handball",
        category="continental",
        name="Champions League Table",
        scope="competition",
        description="Continental club table and ranking.",
    ),
    PlutonList(
        code="HB_CL_MATCHES",
        sport="handball",
        category="continental",
        name="Champions League Matches",
        scope="competition",
        description="Continental club fixtures and statuses.",
    ),
    PlutonList(
        code="HB_NATIONS_LEAGUE",
        sport="handball",
        category="national",
        name="National Teams — Nations League",
        scope="nation",
        description="National team and qualification lists for handball.",
    ),
    PlutonList(
        code="HB_QUALIFIERS",
        sport="handball",
        category="national",
        name="National Teams — Qualifiers",
        scope="nation",
        description="Handball national qualifiers and qualification tables.",
    ),
]

FORMULA_ONE_LISTS: List[PlutonList] = [
    PlutonList(
        code="F1_CALENDAR",
        sport="formula_1",
        category="calendar",
        name="Calendar / Weekend",
        scope="season",
        description="Race weekends and calendar timeline for Formula 1.",
    ),
    PlutonList(
        code="F1_PRACTICE_QUALIFYING",
        sport="formula_1",
        category="session",
        name="Practice & Qualifying",
        scope="race_weekend",
        description="Practice and qualifying sessions and results.",
    ),
    PlutonList(
        code="F1_SPRINT_RACE",
        sport="formula_1",
        category="session",
        name="Sprint & Race",
        scope="race_weekend",
        description="Sprint and race data for each Formula 1 weekend.",
    ),
    PlutonList(
        code="F1_CHAMPIONSHIPS_STATS",
        sport="formula_1",
        category="statistics",
        name="Championships & Statistics",
        scope="season",
        description="Driver and constructor standings plus statistics.",
    ),
    PlutonList(
        code="F1_TEAM_RADAR",
        sport="formula_1",
        category="performance",
        name="Team Performance Radar",
        scope="season",
        description="Team performance tracking and trend analysis.",
    ),
]

NATIONAL_CONTINENTAL_LISTS: List[PlutonList] = [
    PlutonList(
        code="NC_WORLD_CUP_QUALIFIERS",
        sport="multi",
        category="continental",
        name="World Cup Qualifiers",
        scope="region",
        description="Global qualification list for world-cup pathways.",
    ),
    PlutonList(
        code="NC_CONTINENTAL_CHAMPIONSHIPS",
        sport="multi",
        category="continental",
        name="Continental Championships",
        scope="region",
        description="Continental championship fixtures and standings.",
    ),
    PlutonList(
        code="NC_NATIONS_LEAGUE",
        sport="multi",
        category="national",
        name="Nations League / equivalent competitions",
        scope="region",
        description="Nations League style competitions across regions.",
    ),
    PlutonList(
        code="NC_ASIA",
        sport="multi",
        category="regional",
        name="Asia",
        scope="region",
        description="Asian competitions and group structures.",
    ),
    PlutonList(
        code="NC_NORTH_CENTRAL_AMERICA_CARIBBEAN",
        sport="multi",
        category="regional",
        name="North / Central America + Caribbean",
        scope="region",
        description="Regional competition lists for North, Central America and Caribbean.",
    ),
    PlutonList(
        code="NC_SOUTH_AMERICA",
        sport="multi",
        category="regional",
        name="South America",
        scope="region",
        description="South American regional and qualification competitions.",
    ),
    PlutonList(
        code="NC_AFRICA",
        sport="multi",
        category="regional",
        name="Africa",
        scope="region",
        description="African continental and qualification competitions.",
    ),
]

PLUTON_LISTS: List[PlutonList] = (
    FOOTBALL_LISTS
    + BASKETBALL_LISTS
    + HANDBALL_LISTS
    + FORMULA_ONE_LISTS
    + NATIONAL_CONTINENTAL_LISTS
)

PLUTON_LIST_INDEX: Dict[str, PlutonList] = {item.code: item for item in PLUTON_LISTS}


def get_lists_by_sport(sport: str) -> List[PlutonList]:
    """Get all PLUTON lists for a specific sport."""
    return [item for item in PLUTON_LISTS if item.sport == sport]


def get_lists_by_category(category: str) -> List[PlutonList]:
    """Get all PLUTON lists by category."""
    return [item for item in PLUTON_LISTS if item.category == category]


def get_list_by_code(code: str) -> Optional[PlutonList]:
    """Get a specific PLUTON list by code."""
    return PLUTON_LIST_INDEX.get(code)


SPORT_COUNTS: Dict[str, int] = {
    "football": len(FOOTBALL_LISTS),
    "basketball": len(BASKETBALL_LISTS),
    "handball": len(HANDBALL_LISTS),
    "formula_1": len(FORMULA_ONE_LISTS),
    "multi": len(NATIONAL_CONTINENTAL_LISTS),
}

PHASE_3_TOTAL = len(PLUTON_LISTS)


__all__ = [
    "PlutonList",
    "FOOTBALL_LISTS",
    "BASKETBALL_LISTS",
    "HANDBALL_LISTS",
    "FORMULA_ONE_LISTS",
    "NATIONAL_CONTINENTAL_LISTS",
    "PLUTON_LISTS",
    "PLUTON_LIST_INDEX",
    "get_lists_by_sport",
    "get_lists_by_category",
    "get_list_by_code",
    "SPORT_COUNTS",
    "PHASE_3_TOTAL",
]
