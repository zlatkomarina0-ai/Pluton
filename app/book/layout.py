from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class BookStatus:
    label: str
    state: str = "ready"


@dataclass
class BookLayout:
    active_sport: str = "football"
    active_section: str = "dashboard"
    show_sidebar: bool = True
    show_topbar: bool = True
    status: BookStatus = field(default_factory=lambda: BookStatus("PLUTON Book Ready"))

    def to_dict(self) -> Dict[str, object]:
        return {
            "active_sport": self.active_sport,
            "active_section": self.active_section,
            "show_sidebar": self.show_sidebar,
            "show_topbar": self.show_topbar,
            "status": {"label": self.status.label, "state": self.status.state},
        }


@dataclass
class BookCard:
    title: str
    subtitle: str
    value: Optional[str] = None
    tone: str = "neutral"


@dataclass
class BookPanel:
    title: str
    subtitle: str = ""
    cards: List[BookCard] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "cards": [
                {
                    "title": card.title,
                    "subtitle": card.subtitle,
                    "value": card.value,
                    "tone": card.tone,
                }
                for card in self.cards
            ],
        }


__all__ = ["BookStatus", "BookLayout", "BookCard", "BookPanel"]


