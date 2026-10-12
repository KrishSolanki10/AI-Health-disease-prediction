import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Central configuration for AI-Health360 backend.
    All values are pulled from environment variables (.env file)
    so no secrets are hardcoded in the codebase.
    """

    # --- Flask ---
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
    DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"

    # --- MySQL Database ---
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "ai_health360")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- JWT Auth ---
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_EXPIRES_SECONDS", 3600))  # 1 hour

    # --- CORS ---
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

    # --- Trained ML model paths ---
    MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "trained_models")
