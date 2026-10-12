from flask import Blueprint, jsonify

prediction_bp = Blueprint("prediction", __name__)


@prediction_bp.get("/status")
def prediction_status():
    """Placeholder route so the blueprint has at least one endpoint.
    Real routes for this module get built in its dedicated phase."""
    return jsonify({"module": "prediction", "status": "stub - not yet implemented"})
