from flask import Blueprint, jsonify, request
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database
from routes.auth import token_required

admin_bp = Blueprint('admin_route', __name__)

@admin_bp.route('/stats', methods=['GET'])
@token_required
def get_admin_stats(current_user):
    """
    Retrieves system statistics for the Admin Dashboard.
    Enforces admin-only permissions.
    """
    if current_user.get("role") != "admin":
        return jsonify({"message": "Forbidden. Admin privileges required."}), 403
        
    try:
        # Aggregations
        total_users = database.query_db("SELECT COUNT(*) as count FROM users", one=True)["count"]
        total_assessments = database.query_db("SELECT COUNT(*) as count FROM assessments", one=True)["count"]
        total_resumes = database.query_db("SELECT COUNT(*) as count FROM resumes", one=True)["count"]
        
        # Most recommended careers (count from saved_careers or query stats)
        most_saved_careers = database.query_db(
            "SELECT career_title, COUNT(*) as count FROM saved_careers GROUP BY career_title ORDER BY count DESC LIMIT 3"
        )
        
        career_leaderboard = [{"career": item["career_title"], "count": item["count"]} for item in most_saved_careers]
        if not career_leaderboard:
            # Seed mock ranking for UI visuals
            career_leaderboard = [
                {"career": "Software Engineer", "count": 14},
                {"career": "Data Scientist", "count": 10},
                {"career": "UI/UX Designer", "count": 6}
            ]
            
        # Get users list with their status/scores
        users_list = database.query_db(
            "SELECT id, name, email, career_goal, assessment_score, resume_score, career_match_percentage, role, created_at FROM users"
        )
        
        return jsonify({
            "total_users": total_users,
            "total_assessments": total_assessments,
            "total_resumes": total_resumes,
            "career_leaderboard": career_leaderboard,
            "users": users_list
        }), 200
        
    except Exception as e:
        return jsonify({"message": f"Failed to retrieve admin statistics: {str(e)}"}), 500
