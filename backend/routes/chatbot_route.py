from flask import Blueprint, request, jsonify
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import chatbot
from routes.auth import token_required

chatbot_bp = Blueprint('chatbot_route', __name__)

@chatbot_bp.route('/message', methods=['POST'])
@token_required
def chat(current_user):
    """
    Accepts dialogue messages, retrieves user profile metadata, and returns
    tailored AI mentor recommendations.
    """
    data = request.get_json() or {}
    message = data.get("message")
    
    if not message:
        return jsonify({"message": "Please enter a message."}), 400
        
    profile_ctx = {
        "name": current_user["name"],
        "career_goal": current_user.get("career_goal")
    }
    
    response = chatbot.generate_chatbot_response(message, profile_ctx)
    
    return jsonify({
        "sender": "mentor",
        "message": response
    }), 200
