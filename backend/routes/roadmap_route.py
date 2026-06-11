from flask import Blueprint, jsonify, request
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database
import roadmap
from routes.auth import token_required

roadmap_bp = Blueprint('roadmap_route', __name__)

@roadmap_bp.route('/generate', methods=['GET'])
@token_required
def get_roadmap(current_user):
    """
    Generates dynamic step-by-step roadmap and recommendations based on 
    the user's career goal and parsed skills from their resume.
    """
    user_id = current_user["id"]
    career_goal = current_user.get("career_goal")
    
    if not career_goal:
        # Load saved career path
        saved = database.query_db("SELECT career_title FROM saved_careers WHERE user_id = %s LIMIT 1", (user_id,), one=True)
        career_goal = saved["career_title"] if saved else "Software Engineer"
        
    # Get user skills from latest resume
    latest_resume = database.query_db(
        "SELECT parsed_skills FROM resumes WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
        (user_id,), one=True
    )
    
    user_skills = []
    if latest_resume and latest_resume.get("parsed_skills"):
        user_skills = [s.strip() for s in latest_resume["parsed_skills"].split(",")]
        
    # Generate roadmap details
    roadmap_data = roadmap.generate_roadmap_data(career_goal, user_skills)
    
    # Enrich steps with the user's DB course progress
    # Check what courses are in database
    db_progress = database.query_db("SELECT course_name, completion_percentage, status FROM user_progress WHERE user_id = %s", (user_id,))
    progress_map = {p["course_name"]: p for p in db_progress}
    
    for step in roadmap_data["steps"]:
        for course in step["recommended_courses"]:
            c_name = course["title"]
            if c_name in progress_map:
                course["progress"] = progress_map[c_name]["completion_percentage"]
                course["status"] = progress_map[c_name]["status"]
            else:
                course["progress"] = 0
                course["status"] = "Not Started"
                
    return jsonify(roadmap_data), 200

@roadmap_bp.route('/progress/update', methods=['POST'])
@token_required
def update_course_progress(current_user):
    """
    Saves or updates course tracking metrics.
    """
    user_id = current_user["id"]
    data = request.get_json() or {}
    course_name = data.get("course_name")
    progress = data.get("progress", 0) # 0 to 100
    status = data.get("status", "In Progress") # 'Not Started', 'In Progress', 'Completed'
    
    if not course_name:
        return jsonify({"message": "course_name is required"}), 400
        
    try:
        # Check if course exists in SQLite / MySQL using insert or replace
        # We will query and insert/update manually to remain database-agnostic
        existing = database.query_db(
            "SELECT id FROM user_progress WHERE user_id = %s AND course_name = %s",
            (user_id, course_name), one=True
        )
        
        if existing:
            database.execute_db(
                "UPDATE user_progress SET completion_percentage = %s, status = %s WHERE id = %s",
                (int(progress), status, existing["id"])
            )
        else:
            database.execute_db(
                "INSERT INTO user_progress (user_id, course_name, completion_percentage, status) VALUES (%s, %s, %s, %s)",
                (user_id, course_name, int(progress), status)
            )
            
        # Update user notifications when a course is completed
        if status == "Completed" or int(progress) == 100:
            database.execute_db(
                "INSERT INTO notifications (user_id, message, type) VALUES (%s, %s, %s)",
                (user_id, f"Congratulations! You completed the course: {course_name}.", "learning")
            )
            
        return jsonify({"message": "Progress recorded successfully!", "course_name": course_name, "progress": progress, "status": status}), 200
        
    except Exception as e:
        return jsonify({"message": f"Failed to record progress: {str(e)}"}), 500

@roadmap_bp.route('/progress', methods=['GET'])
@token_required
def get_all_progress(current_user):
    """
    Retrieves all course progress logs to plot charts in the frontend tracker.
    """
    user_id = current_user["id"]
    logs = database.query_db("SELECT id, course_name, completion_percentage, status, last_updated FROM user_progress WHERE user_id = %s", (user_id,))
    
    return jsonify(logs), 200
