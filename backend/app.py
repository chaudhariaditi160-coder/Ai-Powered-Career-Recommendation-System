
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

import database

# Import Blueprints
from routes.auth import auth_bp, token_required
from routes.assessment import assessment_bp
from routes.predict import predict_bp
from routes.resume_route import resume_bp
from routes.roadmap_route import roadmap_bp
from routes.chatbot_route import chatbot_bp
from routes.interview_route import interview_bp
from routes.portfolio_route import portfolio_bp
from routes.admin_route import admin_bp

app = Flask(__name__)
# Enable CORS for all routes to support React frontend communication
CORS(app, resources={r"/*": {"origins": "*"}})

# Ensure uploads folder is created
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads'), exist_ok=True)

# Register Blueprints with prefixes
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(assessment_bp, url_prefix='/api/assessment')
app.register_blueprint(predict_bp, url_prefix='/api/predict')
app.register_blueprint(resume_bp, url_prefix='/api/resume')
app.register_blueprint(roadmap_bp, url_prefix='/api/roadmap')
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
app.register_blueprint(interview_bp, url_prefix='/api/interview')
app.register_blueprint(portfolio_bp, url_prefix='/api/portfolio')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# Core Notifications API endpoints
@app.route('/api/notifications', methods=['GET'])
@token_required
def get_notifications(current_user):
    """
    Fetches all notifications/alerts logged for the user.
    """
    user_id = current_user["id"]
    try:
        notes = database.query_db(
            "SELECT id, message, type, is_read, created_at FROM notifications WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,)
        )
        return jsonify(notes), 200
    except Exception as e:
        return jsonify({"message": f"Failed to retrieve notifications: {str(e)}"}), 500

@app.route('/api/notifications/read', methods=['POST'])
@token_required
def mark_notifications_read(current_user):
    """
    Marks all notifications for this user as read.
    """
    user_id = current_user["id"]
    try:
        database.execute_db(
            "UPDATE notifications SET is_read = 1 WHERE user_id = %s",
            (user_id,)
        )
        return jsonify({"message": "Notifications marked as read successfully."}), 200
    except Exception as e:
        return jsonify({"message": f"Failed to update notifications: {str(e)}"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Service health endpoint."""
    return jsonify({
        "status": "online",
        "service": "AI Career Recommendation API",
        "database": "connected"
    }), 200

# Initialize DB on server start
with app.app_context():
    database.init_db()

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
