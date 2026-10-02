from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class NavigationItem:
    id: str
    label: str
    group: str
    sport: str | None = None
    page: str | None = None
    order: int = 0


BOOK_NAVIGATION: List[NavigationItem] = [
    NavigationItem("dashboard", "Dashboard", "main", order=1),
    NavigationItem("results", "Results", "main", order=2),
    NavigationItem("standings", "Standings", "main", order=3),
    NavigationItem("seasons", "Seasons", "main", order=4),
    NavigationItem("settings", "Settings", "main", order=5),
    NavigationItem("football", "Football", "sports", sport="football", page="football_dashboard", order=10),
    NavigationItem("basketball", "Basketball", "sports", sport="basketball", page="basketball_dashboard", order=11),
    NavigationItem("handball", "Handball", "sports", sport="handball", page="handball_dashboard", order=12),
    NavigationItem("formula_1", "Formula 1", "sports", sport="formula_1", page="f1_calendar", order=13),
    NavigationItem("regional", "National / Continental", "sports", sport="multi", page="regional_world_cup_qualifiers", order=14),
]


__all__ = ["NavigationItem", "BOOK_NAVIGATION"]


