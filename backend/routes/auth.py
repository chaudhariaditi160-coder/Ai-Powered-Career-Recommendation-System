import os
import datetime
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt

# Make absolute reference imports workable
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database

auth_bp = Blueprint('auth', __name__)
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-career-ai-key")

def token_required(f):
    """
    Decorator to protect API routes with JWT verification
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                
        if not token:
            return jsonify({"message": "Access token is missing!"}), 401
            
        try:
            # Decode JWT
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            current_user = database.query_db("SELECT id, name, email, career_goal, role FROM users WHERE id = %s", (data["user_id"],), one=True)
            if not current_user:
                return jsonify({"message": "User not found!"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except Exception:
            return jsonify({"message": "Token is invalid!"}), 401
            
        return f(current_user, *args, **kwargs)
        
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    if not name or not email or not password:
        return jsonify({"message": "Missing required details (name, email, password)."}), 400
        
    # Check if email exists
    existing = database.query_db("SELECT id FROM users WHERE email = %s", (email,), one=True)
    if existing:
        return jsonify({"message": "Email is already registered!"}), 409
        
    # Create user
    pw_hash = generate_password_hash(password)
    role = 'admin' if email.lower().endswith('@careerai.admin') or email.lower() == 'admin@careerai.com' else 'user'
    
    try:
        user_id = database.execute_db(
            "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
            (name, email, pw_hash, role)
        )
        
        # Seed an assessment recommendation notification to help user get started
        database.execute_db(
            "INSERT INTO notifications (user_id, message, type) VALUES (%s, %s, %s)",
            (user_id, "Welcome to CareerAI! Complete the Career Assessment to discover your matching career paths.", "assessment")
        )
        
        return jsonify({"message": "User registered successfully!", "user_id": user_id}), 201
    except Exception as e:
        return jsonify({"message": f"Registration failed: {str(e)}"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"message": "Please provide email and password."}), 400
        
    user = database.query_db("SELECT * FROM users WHERE email = %s", (email,), one=True)
    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({"message": "Invalid email or password!"}), 401
        
    # Create JWT Token (valid for 24 hours)
    payload = {
        "user_id": user["id"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    
    # Return user details + token
    return jsonify({
        "message": "Login successful!",
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "career_goal": user["career_goal"],
            "assessment_score": user["assessment_score"],
            "resume_score": user["resume_score"],
            "career_match_percentage": user["career_match_percentage"],
            "role": user["role"]
        }
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    user_id = current_user["id"]
    
    # Get total assessment count, resume score details
    user_details = database.query_db("SELECT name, email, career_goal, assessment_score, resume_score, career_match_percentage, role, created_at FROM users WHERE id = %s", (user_id,), one=True)
    
    return jsonify(user_details), 200

@auth_bp.route('/profile/update', methods=['PUT'])
@token_required
def update_profile(current_user):
    data = request.get_json() or {}
    career_goal = data.get('career_goal')
    
    if not career_goal:
        return jsonify({"message": "Please specify a career goal."}), 400
        
    database.execute_db(
        "UPDATE users SET career_goal = %s WHERE id = %s",
        (career_goal, current_user["id"])
    )
    
    return jsonify({"message": "Profile updated successfully!", "career_goal": career_goal}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Stateless JWT logout is handled on client by discarding token.
    # Expose success status code.
    return jsonify({"message": "Logged out successfully!"}), 200
