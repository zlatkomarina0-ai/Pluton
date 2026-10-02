from dataclasses import dataclass, field
from typing import Dict, List

from app.book.navigation import BOOK_NAVIGATION, NavigationItem


@dataclass
class BookShell:
    active_sport: str = "football"
    active_page: str = "dashboard"
    navigation: List[NavigationItem] = field(default_factory=lambda: BOOK_NAVIGATION)

    def to_dict(self) -> Dict[str, object]:
        return {
            "active_sport": self.active_sport,
            "active_page": self.active_page,
            "navigation": [
                {
                    "id": nav.id,
                    "label": nav.label,
                    "group": nav.group,
                    "sport": nav.sport,
                    "page": nav.page,
                    "order": nav.order,
                }
                for nav in self.navigation
            ],
        }


__all__ = ["BookShell"]


