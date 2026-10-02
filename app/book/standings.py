from dataclasses import dataclass, field
from typing import Dict, List

from app.book import BookCard, BookPanel


@dataclass
class ResultsOverview:
    title: str = "Results"
    subtitle: str = "PLUTON results tracking"
    panels: List[BookPanel] = field(
        default_factory=lambda: [
            BookPanel(
                "Result streams",
                "Main result groups",
                cards=[
                    BookCard("Football", "League and CL outcomes", "active", "primary"),
                    BookCard("Basketball", "League and CL outcomes", "active", "primary"),
                    BookCard("Handball", "League and CL outcomes", "active", "primary"),
                    BookCard("Formula 1", "Race weekend results", "active", "secondary"),
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


__all__ = ["ResultsOverview"]


