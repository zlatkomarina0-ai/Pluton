from app.book.sports.football import FOOTBALL_VIEW_SET
from app.book.sports.basketball import BASKETBALL_VIEW_SET
from app.book.sports.handball import HANDBALL_VIEW_SET
from app.book.sports.formula1 import FORMULA1_VIEW_SET
from app.book.sports.regional import REGIONAL_VIEW_SET

SPORT_VIEW_SETS = {
    "football": FOOTBALL_VIEW_SET,
    "basketball": BASKETBALL_VIEW_SET,
    "handball": HANDBALL_VIEW_SET,
    "formula_1": FORMULA1_VIEW_SET,
    "multi": REGIONAL_VIEW_SET,
}

__all__ = [
    "FOOTBALL_VIEW_SET",
    "BASKETBALL_VIEW_SET",
    "HANDBALL_VIEW_SET",
    "FORMULA1_VIEW_SET",
    "REGIONAL_VIEW_SET",
    "SPORT_VIEW_SETS",
]


