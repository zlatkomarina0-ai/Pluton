from sqlalchemy.orm import Session

from app.models import AnalysisResult, Fixture, Prediction


class AnalysisService:
    @staticmethod
    def analyze_fixture(db: Session, fixture_id: str):
        fixture = db.query(Fixture).filter(Fixture.id == fixture_id).first()
        if not fixture:
            raise ValueError("Fixture not found")

        predictions = db.query(Prediction).filter(Prediction.fixture_id == fixture_id).all()
        if not predictions:
            raise ValueError("No predictions found for this fixture")

        scores = [float(p.confidence) for p in predictions if p.confidence is not None]
        average_confidence = sum(scores) / len(scores) if scores else 0.0

        home_total = sum(float(p.home_score) for p in predictions if p.home_score is not None)
        away_total = sum(float(p.away_score) for p in predictions if p.away_score is not None)
        weighted_score = (home_total - away_total) / max(len(predictions), 1)

        result = AnalysisResult(
            fixture_id=fixture_id,
            source_summary={
                "fixture_id": fixture_id,
                "prediction_count": len(predictions),
                "average_confidence": round(average_confidence, 2),
            },
            consensus_score=round(average_confidence, 2),
            weighted_score=round(weighted_score, 2),
            pluton_score=round(average_confidence + weighted_score, 2),
            confidence_score=round(average_confidence, 2),
            result_label="pending",
            notes="Computed from current predictions for fixture",
        )
        db.add(result)
        db.commit()
        db.refresh(result)
        return result

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100):
        return db.query(AnalysisResult).offset(skip).limit(limit).all()
