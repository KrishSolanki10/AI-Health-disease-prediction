from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from config import Config

# --- Extensions (initialized here, imported by models/routes) ---
db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, origins=app.config["CORS_ORIGINS"], supports_credentials=True)

    # --- Register blueprints ---
    # Each route module is registered here. Files exist as stubs for now
    # and will be filled in during their respective phases.
    from routes.auth import auth_bp
    from routes.prediction import prediction_bp
    from routes.chatbot import chatbot_bp
    from routes.health import health_bp
    from routes.reports import reports_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(prediction_bp, url_prefix="/api/predict")
    app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")
    app.register_blueprint(health_bp, url_prefix="/api/health")
    app.register_blueprint(reports_bp, url_prefix="/api/reports")

    @app.get("/api/ping")
    def ping():
        """Simple health-check endpoint to confirm the server + DB config loaded."""
        return jsonify({"status": "ok", "service": "AI-Health360 backend"})

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  # creates tables from models if they don't exist yet
    app.run(debug=Config.DEBUG, port=5000)
