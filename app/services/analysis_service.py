from sqlalchemy.orm import Session

from app.models import AnalysisResult, Fixture, Prediction
from app.services.prediction_engine import PredictionEngine


class AnalysisService:
    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100):
        return db.query(AnalysisResult).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_fixture(db: Session, fixture_id: str):
        return db.query(AnalysisResult).filter(AnalysisResult.fixture_id == fixture_id).first()

    @staticmethod
    def analyze_fixture(db: Session, fixture_id: str):
        """
        Analyze a fixture using the prediction engine
        """
        return PredictionEngine.analyze_fixture(db, fixture_id)

    @staticmethod
    def get_fixture_context(db: Session, fixture_id: str):
        """
        Get full context for a fixture including analysis and predictions
        """
        fixture = db.query(Fixture).filter(Fixture.id == fixture_id).first()
        if not fixture:
            raise ValueError("Fixture not found")

        predictions = db.query(Prediction).filter(Prediction.fixture_id == fixture_id).all()
        analysis = db.query(AnalysisResult).filter(AnalysisResult.fixture_id == fixture_id).first()

        return {
            "fixture": fixture,
            "predictions": predictions,
            "analysis": analysis,
            "prediction_count": len(predictions),
            "has_analysis": analysis is not None,
        }
