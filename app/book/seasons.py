from dataclasses import dataclass, field
from typing import Dict, List

from app.book import BookCard, BookPanel


@dataclass
class StandingsOverview:
    title: str = "Standings"
    subtitle: str = "Rankings and tables"
    panels: List[BookPanel] = field(
        default_factory=lambda: [
            BookPanel(
                "Standing groups",
                "Table-driven views",
                cards=[
                    BookCard("Big Table", "Global standings", "ready", "primary"),
                    BookCard("League Standings", "Per league table", "ready", "primary"),
                    BookCard("Champions League", "Continental table", "ready", "secondary"),
                    BookCard("Regional table", "Nations and qualifiers", "ready", "secondary"),
                ],
            )
        ]
    )

    def to_dict(self) -> Dict[str, object]:
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "panels": [panel.to_dict() for panel in self.panels],
        }


__all__ = ["StandingsOverview"]


