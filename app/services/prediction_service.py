from sqlalchemy.orm import Session

from app.models import Fixture, League, Season, Team


class FixturesService:
    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Fixture).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, fixture_id: str):
        return db.query(Fixture).filter(Fixture.id == fixture_id).first()

    @staticmethod
    def create(
        db: Session,
        *,
        sport_id: str,
        league_id: str | None,
        season_id: str | None,
        home_team_id: str | None,
        away_team_id: str | None,
        status: str = "scheduled",
        venue: str | None = None,
        round_name: str | None = None,
        competition_name: str | None = None,
        external_id: str | None = None,
        kickoff_at=None,
    ):
        if league_id:
            league = db.query(League).filter(League.id == league_id).first()
            if not league:
                raise ValueError("League not found")

        if season_id:
            season = db.query(Season).filter(Season.id == season_id).first()
            if not season:
                raise ValueError("Season not found")
            if league_id and season.league_id != league_id:
                raise ValueError("Season does not belong to the supplied league")

        if home_team_id:
            home_team = db.query(Team).filter(Team.id == home_team_id).first()
            if not home_team:
                raise ValueError("Home team not found")

        if away_team_id:
            away_team = db.query(Team).filter(Team.id == away_team_id).first()
            if not away_team:
                raise ValueError("Away team not found")

        fixture = Fixture(
            sport_id=sport_id,
            league_id=league_id,
            season_id=season_id,
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            external_id=external_id,
            kickoff_at=kickoff_at,
            status=status,
            venue=venue,
            round_name=round_name,
            competition_name=competition_name,
        )
        db.add(fixture)
        db.commit()
        db.refresh(fixture)
        return fixture
