from flask import Blueprint, jsonify

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.get("/status")
def chatbot_status():
    """Placeholder route so the blueprint has at least one endpoint.
    Real routes for this module get built in its dedicated phase."""
    return jsonify({"module": "chatbot", "status": "stub - not yet implemented"})
