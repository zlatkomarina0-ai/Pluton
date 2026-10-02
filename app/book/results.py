from dataclasses import dataclass, field
from typing import List

from app.book import BookCard, BookPanel


@dataclass
class DashboardOverview:
    title: str = "PLUTON Dashboard"
    subtitle: str = "Book overview"
    panels: List[BookPanel] = field(
        default_factory=lambda: [
            BookPanel(
                "Sports",
                "Active PLUTON modules",
                cards=[
                    BookCard("Football", "Core competitions", "9 pages", "primary"),
                    BookCard("Basketball", "Core competitions", "11 pages", "primary"),
                    BookCard("Handball", "Core competitions", "9 pages", "primary"),
                    BookCard("Formula 1", "Race weekend view", "5 pages", "secondary"),
                ],
            ),
            BookPanel(
                "Core views",
                "Book interface sections",
                cards=[
                    BookCard("Dashboard", "Main overview", "ready", "success"),
                    BookCard("Results", "Results tracking", "ready", "success"),
                    BookCard("Standings", "Tables and ranking", "ready", "success"),
                    BookCard("Seasons", "Season management", "ready", "success"),
                ],
            ),
        ]
    )

    def to_dict(self):
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "panels": [panel.to_dict() for panel in self.panels],
        }


__all__ = ["DashboardOverview"]


