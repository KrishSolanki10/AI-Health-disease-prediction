from flask import Blueprint, jsonify

reports_bp = Blueprint("reports", __name__)


@reports_bp.get("/status")
def reports_status():
    """Placeholder route so the blueprint has at least one endpoint.
    Real routes for this module get built in its dedicated phase."""
    return jsonify({"module": "reports", "status": "stub - not yet implemented"})
