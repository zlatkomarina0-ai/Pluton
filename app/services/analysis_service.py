from sqlalchemy.orm import Session

from app.models import Fixture, Prediction, User


class PredictionService:
    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Prediction).offset(skip).limit(limit).all()

    @staticmethod
    def list_for_user(db: Session, user_id: str, skip: int = 0, limit: int = 100):
        return (
            db.query(Prediction)
            .filter(Prediction.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create(
        db: Session,
        *,
        fixture_id: str,
        user_id: str,
        prediction_type: str,
        home_score: int | None = None,
        away_score: int | None = None,
        market_type: str | None = None,
        confidence: float | None = None,
        strength: float | None = None,
    ):
        fixture = db.query(Fixture).filter(Fixture.id == fixture_id).first()
        if not fixture:
            raise ValueError("Fixture not found")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        prediction = Prediction(
            fixture_id=fixture_id,
            user_id=user_id,
            prediction_type=prediction_type,
            home_score=home_score,
            away_score=away_score,
            market_type=market_type,
            confidence=confidence,
            strength=strength,
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        return prediction
