from sqlalchemy.orm import Session
from decimal import Decimal
from app.models import Fixture, Prediction, AnalysisResult


class PredictionEngine:
    """
    PLUTON Prediction Engine
    Analyzes predictions for fixtures and generates consensus/confidence/pluton scores
    """

    CONFIDENCE_WEIGHT = 0.4
    STRENGTH_WEIGHT = 0.3
    AGREEMENT_WEIGHT = 0.3

    @staticmethod
    def calculate_consensus_score(predictions: list) -> float:
        """
        Calculate consensus score from multiple predictions
        - Average confidence across all predictions
        - Range: 0.0 - 100.0
        """
        if not predictions:
            return 0.0

        confidences = [float(p.confidence) for p in predictions if p.confidence is not None]
        if not confidences:
            return 0.0

        return round(sum(confidences) / len(confidences), 2)

    @staticmethod
    def calculate_weighted_score(predictions: list) -> float:
        """
        Calculate weighted score based on prediction agreement
        - Measures how close predictions agree on home/away outcome
        - Range: -100.0 to 100.0 (negative = away, positive = home)
        """
        if not predictions:
            return 0.0

        home_scores = []
        away_scores = []

        for p in predictions:
            if p.home_score is not None:
                home_scores.append(float(p.home_score))
            if p.away_score is not None:
                away_scores.append(float(p.away_score))

        if not home_scores or not away_scores:
            return 0.0

        avg_home = sum(home_scores) / len(home_scores)
        avg_away = sum(away_scores) / len(away_scores)
        difference = avg_home - avg_away

        return round(difference, 2)

    @staticmethod
    def calculate_strength_score(predictions: list) -> float:
        """
        Calculate average strength across predictions
        - Measures conviction level of predictions
        - Range: 0.0 - 100.0
        """
        if not predictions:
            return 0.0

        strengths = [float(p.strength) for p in predictions if p.strength is not None]
        if not strengths:
            return 0.0

        return round(sum(strengths) / len(strengths), 2)

    @staticmethod
    def calculate_pluton_score(consensus: float, weighted: float, strength: float) -> float:
        """
        Calculate PLUTON score - proprietary algorithm combining:
        - Consensus: how much experts agree (40%)
        - Weighted: directional bias (30%)
        - Strength: conviction level (30%)
        """
        # Normalize weighted score to 0-100 range
        normalized_weighted = ((weighted + 100) / 2) if weighted >= -100 and weighted <= 100 else 50

        pluton = (
            (consensus * PredictionEngine.CONFIDENCE_WEIGHT)
            + (normalized_weighted * PredictionEngine.AGREEMENT_WEIGHT)
            + (strength * PredictionEngine.STRENGTH_WEIGHT)
        )

        return round(min(100.0, max(0.0, pluton)), 2)

    @staticmethod
    def determine_result_label(consensus: float, pluton: float) -> str:
        """
        Determine result label based on scores
        - "high_confidence": consensus >= 75 and pluton >= 70
        - "moderate_confidence": consensus >= 60 and pluton >= 55
        - "low_confidence": consensus >= 40 and pluton >= 40
        - "uncertain": otherwise
        """
        if consensus >= 75 and pluton >= 70:
            return "high_confidence"
        elif consensus >= 60 and pluton >= 55:
            return "moderate_confidence"
        elif consensus >= 40 and pluton >= 40:
            return "low_confidence"
        else:
            return "uncertain"

    @staticmethod
    def analyze_fixture(db: Session, fixture_id: str) -> AnalysisResult:
        """
        Full analysis pipeline for a fixture
        1. Load fixture and predictions
        2. Calculate all scores
        3. Create analysis result
        4. Save to database
        """
        fixture = db.query(Fixture).filter(Fixture.id == fixture_id).first()
        if not fixture:
            raise ValueError(f"Fixture {fixture_id} not found")

        predictions = db.query(Prediction).filter(Prediction.fixture_id == fixture_id).all()
        if not predictions:
            raise ValueError(f"No predictions found for fixture {fixture_id}")

        # Calculate scores
        consensus_score = PredictionEngine.calculate_consensus_score(predictions)
        weighted_score = PredictionEngine.calculate_weighted_score(predictions)
        strength_score = PredictionEngine.calculate_strength_score(predictions)
        pluton_score = PredictionEngine.calculate_pluton_score(consensus_score, weighted_score, strength_score)
        result_label = PredictionEngine.determine_result_label(consensus_score, pluton_score)

        # Check if analysis already exists
        existing = db.query(AnalysisResult).filter(AnalysisResult.fixture_id == fixture_id).first()
        if existing:
            # Update existing
            existing.consensus_score = Decimal(str(consensus_score))
            existing.weighted_score = Decimal(str(weighted_score))
            existing.pluton_score = Decimal(str(pluton_score))
            existing.confidence_score = Decimal(str(consensus_score))
            existing.result_label = result_label
            existing.source_summary = {
                "fixture_id": fixture_id,
                "prediction_count": len(predictions),
                "consensus_score": consensus_score,
                "strength_score": strength_score,
                "agreed_predictions": sum(1 for p in predictions if p.is_agreed_tip),
            }
            existing.notes = f"Updated from {len(predictions)} predictions"
            db.commit()
            db.refresh(existing)
            return existing
        else:
            # Create new
            result = AnalysisResult(
                fixture_id=fixture_id,
                consensus_score=Decimal(str(consensus_score)),
                weighted_score=Decimal(str(weighted_score)),
                pluton_score=Decimal(str(pluton_score)),
                confidence_score=Decimal(str(consensus_score)),
                result_label=result_label,
                source_summary={
                    "fixture_id": fixture_id,
                    "prediction_count": len(predictions),
                    "consensus_score": consensus_score,
                    "strength_score": strength_score,
                    "agreed_predictions": sum(1 for p in predictions if p.is_agreed_tip),
                },
                notes=f"Generated from {len(predictions)} predictions",
            )
            db.add(result)
            db.commit()
            db.refresh(result)
            return result
