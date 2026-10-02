from dataclasses import dataclass, field
from typing import Dict, List

from app.book import BookCard, BookPanel


@dataclass
class SettingsOverview:
    title: str = "Settings"
    subtitle: str = "PLUTON book settings"
    panels: List[BookPanel] = field(
        default_factory=lambda: [
            BookPanel(
                "Configuration",
                "Setup and visual controls",
                cards=[
                    BookCard("Sport selector", "Switch active sport", "enabled", "primary"),
                    BookCard("Season selector", "Choose active season", "enabled", "primary"),
                    BookCard("Display mode", "Dashboard / tables / fixtures", "ready", "secondary"),
                    BookCard("Protected data", "My Tip / Agreed Tip guardrails", "enabled", "success"),
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


__all__ = ["SettingsOverview"]


