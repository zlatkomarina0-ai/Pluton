from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class BookPage:
    page_id: str
    label: str
    section: str
    sport: Optional[str] = None
    category: Optional[str] = None
    scope: Optional[str] = None
    enabled: bool = True


@dataclass(frozen=True)
class BookModule:
    module_id: str
    label: str
    sport: Optional[str] = None
    pages: List[BookPage] = field(default_factory=list)


NAVIGATION_PAGES: List[BookPage] = [
    BookPage("dashboard", "Dashboard", "main", scope="global"),
    BookPage("results", "Results", "results", scope="global"),
    BookPage("standings", "Standings", "standings", scope="global"),
    BookPage("seasons", "Seasons", "seasons", scope="global"),
    BookPage("settings", "Settings", "settings", scope="global"),
]

FOOTBALL_PAGES: List[BookPage] = [
    BookPage("football_dashboard", "Football Dashboard", "sport", sport="football", category="dashboard"),
    BookPage("football_big_table", "Big Table", "sport", sport="football", category="league", scope="global"),
    BookPage("football_league_standings", "League Standings", "sport", sport="football", category="league", scope="league"),
    BookPage("football_league_fixtures", "League Fixtures", "sport", sport="football", category="fixtures", scope="league"),
    BookPage("football_matches_suggestions", "Matches with Suggestions", "sport", sport="football", category="matches", scope="global"),
    BookPage("football_cl_table", "Champions League Table", "sport", sport="football", category="continental", scope="competition"),
    BookPage("football_cl_matches", "Champions League Matches", "sport", sport="football", category="continental", scope="competition"),
    BookPage("football_nations_league", "Nations League", "sport", sport="football", category="national", scope="nation"),
    BookPage("football_qualifiers", "Qualifiers", "sport", sport="football", category="national", scope="nation"),
]

BASKETBALL_PAGES: List[BookPage] = [
    BookPage("basketball_dashboard", "Basketball Dashboard", "sport", sport="basketball", category="dashboard"),
    BookPage("basketball_big_table", "Big Table", "sport", sport="basketball", category="league", scope="global"),
    BookPage("basketball_league_standings", "League Standings", "sport", sport="basketball", category="league", scope="league"),
    BookPage("basketball_league_fixtures", "League Fixtures", "sport", sport="basketball", category="fixtures", scope="league"),
    BookPage("basketball_matches_suggestions", "Matches with Suggestions", "sport", sport="basketball", category="matches", scope="global"),
    BookPage("basketball_cl_table", "Champions League Table", "sport", sport="basketball", category="continental", scope="competition"),
    BookPage("basketball_cl_matches", "Champions League Matches", "sport", sport="basketball", category="continental", scope="competition"),
    BookPage("basketball_nations_league", "Nations League", "sport", sport="basketball", category="national", scope="nation"),
    BookPage("basketball_qualifiers", "Qualifiers", "sport", sport="basketball", category="national", scope="nation"),
    BookPage("basketball_nba_results", "NBA Results", "sport", sport="basketball", category="results", scope="league"),
    BookPage("basketball_nba_standings", "NBA Standings", "sport", sport="basketball", category="standings", scope="league"),
]

HANDBALL_PAGES: List[BookPage] = [
    BookPage("handball_dashboard", "Handball Dashboard", "sport", sport="handball", category="dashboard"),
    BookPage("handball_big_table", "Big Table", "sport", sport="handball", category="league", scope="global"),
    BookPage("handball_league_standings", "League Standings", "sport", sport="handball", category="league", scope="league"),
    BookPage("handball_league_fixtures", "League Fixtures", "sport", sport="handball", category="fixtures", scope="league"),
    BookPage("handball_matches_suggestions", "Matches with Suggestions", "sport", sport="handball", category="matches", scope="global"),
    BookPage("handball_cl_table", "Champions League Table", "sport", sport="handball", category="continental", scope="competition"),
    BookPage("handball_cl_matches", "Champions League Matches", "sport", sport="handball", category="continental", scope="competition"),
    BookPage("handball_nations_league", "Nations League", "sport", sport="handball", category="national", scope="nation"),
    BookPage("handball_qualifiers", "Qualifiers", "sport", sport="handball", category="national", scope="nation"),
]

FORMULA1_PAGES: List[BookPage] = [
    BookPage("f1_calendar", "Calendar / Weekend", "sport", sport="formula_1", category="calendar", scope="season"),
    BookPage("f1_practice_qualifying", "Practice & Qualifying", "sport", sport="formula_1", category="session", scope="race_weekend"),
    BookPage("f1_sprint_race", "Sprint & Race", "sport", sport="formula_1", category="session", scope="race_weekend"),
    BookPage("f1_championships_stats", "Championships & Statistics", "sport", sport="formula_1", category="statistics", scope="season"),
    BookPage("f1_team_radar", "Team Performance Radar", "sport", sport="formula_1", category="performance", scope="season"),
]

REGIONAL_PAGES: List[BookPage] = [
    BookPage("regional_world_cup_qualifiers", "World Cup Qualifiers", "sport", sport="multi", category="continental", scope="region"),
    BookPage("regional_continental_championships", "Continental Championships", "sport", sport="multi", category="continental", scope="region"),
    BookPage("regional_nations_league", "Nations League / equivalent competitions", "sport", sport="multi", category="national", scope="region"),
    BookPage("regional_asia", "Asia", "sport", sport="multi", category="regional", scope="region"),
    BookPage("regional_ncca", "North / Central America + Caribbean", "sport", sport="multi", category="regional", scope="region"),
    BookPage("regional_south_america", "South America", "sport", sport="multi", category="regional", scope="region"),
    BookPage("regional_africa", "Africa", "sport", sport="multi", category="regional", scope="region"),
]

BOOK_MODULES: List[BookModule] = [
    BookModule("main", "Main", pages=NAVIGATION_PAGES),
    BookModule("football", "Football", sport="football", pages=FOOTBALL_PAGES),
    BookModule("basketball", "Basketball", sport="basketball", pages=BASKETBALL_PAGES),
    BookModule("handball", "Handball", sport="handball", pages=HANDBALL_PAGES),
    BookModule("formula_1", "Formula 1", sport="formula_1", pages=FORMULA1_PAGES),
    BookModule("regional", "National / Continental", sport="multi", pages=REGIONAL_PAGES),
]

BOOK_PAGE_INDEX: Dict[str, BookPage] = {
    page.page_id: page for module in BOOK_MODULES for page in module.pages
}


def get_book_module(module_id: str) -> Optional[BookModule]:
    for module in BOOK_MODULES:
        if module.module_id == module_id:
            return module
    return None


def get_book_page(page_id: str) -> Optional[BookPage]:
    return BOOK_PAGE_INDEX.get(page_id)


def get_book_modules_for_sport(sport: str) -> List[BookModule]:
    return [module for module in BOOK_MODULES if module.sport == sport]


__all__ = [
    "BookPage",
    "BookModule",
    "NAVIGATION_PAGES",
    "FOOTBALL_PAGES",
    "BASKETBALL_PAGES",
    "HANDBALL_PAGES",
    "FORMULA1_PAGES",
    "REGIONAL_PAGES",
    "BOOK_MODULES",
    "BOOK_PAGE_INDEX",
    "get_book_module",
    "get_book_page",
    "get_book_modules_for_sport",
]


if __name__ == "__main__":
    print(f"BOOK_MODULES={len(BOOK_MODULES)}")
    print(f"TOTAL_PAGES={len(BOOK_PAGE_INDEX)}")
    print([module.module_id for module in BOOK_MODULES])




