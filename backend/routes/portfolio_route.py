from flask import Blueprint, request, jsonify
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import portfolio
from routes.auth import token_required

portfolio_bp = Blueprint('portfolio_route', __name__)

@portfolio_bp.route('/analyze', methods=['POST'])
@token_required
def analyze_portfolio(current_user):
    """
    Accepts a GitHub handle, runs analytics on the repositories, and returns 
    strengths, scores, and developer recommendations.
    """
    data = request.get_json() or {}
    username = data.get("username")
    
    if not username:
        return jsonify({"message": "Please enter a valid GitHub username."}), 400
        
    analysis = portfolio.analyze_github_profile(username)
    return jsonify(analysis), 200
