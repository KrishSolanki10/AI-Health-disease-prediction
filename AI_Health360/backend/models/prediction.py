from app import db
from datetime import datetime


class Prediction(db.Model):
    """Stores the result of every disease-prediction run for a user."""
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    disease_type = db.Column(db.String(50), nullable=False)  # diabetes/heart/liver/kidney
    input_data = db.Column(db.JSON, nullable=False)          # raw form inputs used
    risk_level = db.Column(db.String(20))                    # Low/Moderate/High
    confidence = db.Column(db.Float)                         # model confidence %
    model_used = db.Column(db.String(50))                    # e.g. RandomForest, XGBoost
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "disease_type": self.disease_type,
            "risk_level": self.risk_level,
            "confidence": self.confidence,
            "model_used": self.model_used,
            "created_at": self.created_at.isoformat(),
        }
