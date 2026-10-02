from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.models import Fixture, League, Season, Team, Prediction, AnalysisResult
from app.phase3 import PlutonList, PLUTON_LIST_INDEX


class ListDataEngine:
    """
    Core engine for building and retrieving PLUTON list data.
    Handles fixture aggregation, filtering, and ranking for all 35 PLUTON lists.
    """

    @staticmethod
    def get_big_table_data(db: Session, sport_id: str, season_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Aggregate standings across all leagues for a sport (Big Table).
        """
        query = db.query(League).filter(League.sport_id == sport_id, League.active == True)
        leagues = query.all()

        standings = []
        for league in leagues:
            league_fixtures = db.query(Fixture).filter(
                Fixture.league_id == league.id,
                Fixture.sport_id == sport_id,
            )
            if season_id:
                league_fixtures = league_fixtures.filter(Fixture.season_id == season_id)

            standings.append({
                "league_id": str(league.id),
                "league_name": league.name,
                "fixture_count": league_fixtures.count(),
            })

        return {
            "sport_id": sport_id,
            "list_code": "*_BIG_TABLE",
            "total_leagues": len(leagues),
            "standings": standings,
            "timestamp": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def get_league_standings_data(db: Session, league_id: str, season_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve standings for a specific league.
        """
        league = db.query(League).filter(League.id == league_id).first()
        if not league:
            raise ValueError(f"League {league_id} not found")

        fixtures = db.query(Fixture).filter(
            Fixture.league_id == league_id,
            Fixture.sport_id == league.sport_id,
        )
        if season_id:
            fixtures = fixtures.filter(Fixture.season_id == season_id)

        return {
            "league_id": str(league.id),
            "league_name": league.name,
            "sport_id": str(league.sport_id),
            "season_id": season_id,
            "fixture_count": fixtures.count(),
            "list_code": "*_LEAGUE_STANDINGS",
            "timestamp": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def get_league_fixtures_data(db: Session, league_id: str, season_id: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """
        Retrieve fixtures for a specific league.
        """
        league = db.query(League).filter(League.id == league_id).first()
        if not league:
            raise ValueError(f"League {league_id} not found")

        fixtures = db.query(Fixture).filter(
            Fixture.league_id == league_id,
            Fixture.sport_id == league.sport_id,
        ).order_by(Fixture.kickoff_at.desc()).limit(limit).all()

        if season_id:
            fixtures = [f for f in fixtures if str(f.season_id) == season_id]

        fixture_list = [
            {
                "fixture_id": str(f.id),
                "event_id": f.event_id,
                "home_team_id": str(f.home_team_id) if f.home_team_id else None,
                "away_team_id": str(f.away_team_id) if f.away_team_id else None,
                "kickoff_at": f.kickoff_at.isoformat() if f.kickoff_at else None,
                "status": f.status,
            }
            for f in fixtures
        ]

        return {
            "league_id": str(league.id),
            "league_name": league.name,
            "sport_id": str(league.sport_id),
            "season_id": season_id,
            "fixture_count": len(fixture_list),
            "fixtures": fixture_list,
            "list_code": "*_LEAGUE_FIXTURES",
            "timestamp": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def get_matches_with_suggestions_data(db: Session, sport_id: str, season_id: Optional[str] = None, limit: int = 50) -> Dict[str, Any]:
        """
        Retrieve fixtures with associated predictions/suggestions.
        """
        fixtures = db.query(Fixture).filter(
            Fixture.sport_id == sport_id,
            Fixture.status == "scheduled",
        ).order_by(Fixture.kickoff_at.asc()).limit(limit).all()

        if season_id:
            fixtures = [f for f in fixtures if str(f.season_id) == season_id]

        matches_with_suggestions = []
        for fixture in fixtures:
            predictions = db.query(Prediction).filter(Prediction.fixture_id == fixture.id).all()
            analysis = db.query(AnalysisResult).filter(AnalysisResult.fixture_id == fixture.id).first()

            matches_with_suggestions.append({
                "fixture_id": str(fixture.id),
                "event_id": fixture.event_id,
                "home_team_id": str(fixture.home_team_id) if fixture.home_team_id else None,
                "away_team_id": str(fixture.away_team_id) if fixture.away_team_id else None,
                "kickoff_at": fixture.kickoff_at.isoformat() if fixture.kickoff_at else None,
                "status": fixture.status,
                "prediction_count": len(predictions),
                "has_analysis": analysis is not None,
                "analysis_score": float(analysis.pluton_score) if analysis and analysis.pluton_score else None,
            })

        return {
            "sport_id": sport_id,
            "season_id": season_id,
            "match_count": len(matches_with_suggestions),
            "matches": matches_with_suggestions,
            "list_code": "*_MATCHES_SUGGESTIONS",
            "timestamp": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def get_regional_list_data(db: Session, sport: str, region: str) -> Dict[str, Any]:
        """
        Retrieve regional/national competition data.
        """
        leagues = db.query(League).filter(
            League.is_international == True,
            League.country.ilike(f"%{region}%") if region else True,
        ).all()

        return {
            "sport": sport,
            "region": region,
            "league_count": len(leagues),
            "leagues": [
                {
                    "league_id": str(l.id),
                    "league_name": l.name,
                    "country": l.country,
                }
                for l in leagues
            ],
            "list_code": f"*_{region.upper().replace(' ', '_')}",
            "timestamp": datetime.utcnow().isoformat(),
        }


class ListRenderer:
    """
    Renders PLUTON list data in appropriate format for display.
    """

    @staticmethod
    def render_list(list_code: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format list data for rendering.
        """
        pluton_list = PLUTON_LIST_INDEX.get(list_code)
        if not pluton_list:
            raise ValueError(f"List code {list_code} not found")

        return {
            "list_code": list_code,
            "list_name": pluton_list.name,
            "sport": pluton_list.sport,
            "category": pluton_list.category,
            "scope": pluton_list.scope,
            "description": pluton_list.description,
            "data": data,
            "rendered_at": datetime.utcnow().isoformat(),
        }


class ListManager:
    """
    High-level manager for PLUTON list operations.
    """

    @staticmethod
    def build_list(db: Session, list_code: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Build a PLUTON list with data.
        """
        pluton_list = PLUTON_LIST_INDEX.get(list_code)
        if not pluton_list:
            raise ValueError(f"List code {list_code} not found")

        filters = filters or {}
        sport_id = filters.get("sport_id")
        league_id = filters.get("league_id")
        season_id = filters.get("season_id")

        # Route to appropriate data engine based on list code
        if "BIG_TABLE" in list_code:
            data = ListDataEngine.get_big_table_data(db, sport_id, season_id)
        elif "LEAGUE_STANDINGS" in list_code:
            data = ListDataEngine.get_league_standings_data(db, league_id, season_id)
        elif "LEAGUE_FIXTURES" in list_code:
            data = ListDataEngine.get_league_fixtures_data(db, league_id, season_id)
        elif "MATCHES_SUGGESTIONS" in list_code:
            data = ListDataEngine.get_matches_with_suggestions_data(db, sport_id, season_id)
        else:
            data = {"message": "List data not yet implemented", "list_code": list_code}

        return ListRenderer.render_list(list_code, data)

    @staticmethod
    def get_sport_lists(sport: str) -> List[Dict[str, Any]]:
        """
        Get all PLUTON lists for a sport.
        """
        from app.phase3 import get_lists_by_sport
        lists = get_lists_by_sport(sport)
        return [
            {
                "code": l.code,
                "name": l.name,
                "category": l.category,
                "scope": l.scope,
            }
            for l in lists
        ]


__all__ = [
    "ListDataEngine",
    "ListRenderer",
    "ListManager",
]
