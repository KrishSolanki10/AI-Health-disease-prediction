from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/status")
def health_status():
    """Placeholder route so the blueprint has at least one endpoint.
    Real routes for this module get built in its dedicated phase."""
    return jsonify({"module": "health", "status": "stub - not yet implemented"})
