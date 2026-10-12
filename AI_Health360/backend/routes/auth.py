from flask import Blueprint, jsonify

auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/status")
def auth_status():
    """Placeholder route so the blueprint has at least one endpoint.
    Real routes for this module get built in its dedicated phase."""
    return jsonify({"module": "auth", "status": "stub - not yet implemented"})
