from app import db
from datetime import datetime


class HealthRecord(db.Model):
    """
    Time-series health metrics per user, used to build trend charts
    (weight, BP, glucose, cholesterol) and the Health Risk Score.
    """
    __tablename__ = "health_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    bmi = db.Column(db.Float)
    blood_pressure_systolic = db.Column(db.Integer)
    blood_pressure_diastolic = db.Column(db.Integer)
    glucose = db.Column(db.Float)
    cholesterol = db.Column(db.Float)
    weight = db.Column(db.Float)
    health_risk_score = db.Column(db.Integer)  # 0-100
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "bmi": self.bmi,
            "blood_pressure": f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic}",
            "glucose": self.glucose,
            "cholesterol": self.cholesterol,
            "weight": self.weight,
            "health_risk_score": self.health_risk_score,
            "recorded_at": self.recorded_at.isoformat(),
        }
