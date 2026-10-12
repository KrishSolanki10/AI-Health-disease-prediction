from app import db
from datetime import datetime


class User(db.Model):
    """
    Represents any account in the system: patient, doctor, or admin.
    role determines dashboard access and permissions.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum("patient", "doctor", "admin", name="user_roles"),
                      default="patient", nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum("Male", "Female", "Other", name="genders"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "age": self.age,
            "gender": self.gender,
        }
