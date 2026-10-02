from dataclasses import dataclass, field
from typing import Dict, List

from app.book import BookCard, BookPanel


@dataclass
class SeasonsOverview:
    title: str = "Seasons"
    subtitle: str = "Season and competition context"
    panels: List[BookPanel] = field(
        default_factory=lambda: [
            BookPanel(
                "Season controls",
                "Competition state management",
                cards=[
                    BookCard("Current season", "Active season view", "ready", "primary"),
                    BookCard("Archive", "Historical seasons", "protected", "secondary"),
                    BookCard("Lock state", "Protected from auto update", "enabled", "success"),
                    BookCard("Versioning", "Season version tracking", "ready", "neutral"),
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


__all__ = ["SeasonsOverview"]


