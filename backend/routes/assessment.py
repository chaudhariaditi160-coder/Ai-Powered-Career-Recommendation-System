from flask import Blueprint, request, jsonify
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database
from routes.auth import token_required

assessment_bp = Blueprint('assessment', __name__)

# Questions bank
ASSESSMENT_QUESTIONS = {
    "interests": [
        {"id": "int-1", "text": "Do you enjoy building interactive websites or web applications?", "career": "Software Engineer"},
        {"id": "int-2", "text": "Are you fascinated by statistics, trends, and extracting insights from database tables?", "career": "Data Scientist"},
        {"id": "int-3", "text": "Do you enjoy drawing layouts, picking colors, and focusing on user interfaces?", "career": "UI/UX Designer"},
        {"id": "int-4", "text": "Are you interested in managing cloud servers, automated scripts, and system health?", "career": "DevOps Engineer"},
        {"id": "int-5", "text": "Do you like organizing tasks, leading cross-functional teams, and creating project timelines?", "career": "Product Manager"}
    ],
    "skills": [
        {"id": "skl-1", "text": "Rate your python/javascript coding ability (1-5)"},
        {"id": "skl-2", "text": "Rate your SQL and database management understanding (1-5)"},
        {"id": "skl-3", "text": "Rate your layout prototyping and Figma design capability (1-5)"},
        {"id": "skl-4", "text": "Rate your command-line, linux, and docker understanding (1-5)"},
        {"id": "skl-5", "text": "Rate your leadership and presentation/speech capabilities (1-5)"}
    ],
    "personality": [
        {"id": "per-1", "text": "I consider myself a highly analytical, detail-oriented person.", "trait": "analytical"},
        {"id": "per-2", "text": "I am empathetic and always consider how other people feel.", "trait": "empathetic"},
        {"id": "per-3", "text": "I am natural at presenting ideas, convincing teams, and organizing events.", "trait": "leader"}
    ],
    "technical": [
        {
            "id": "tech-1",
            "question": "Which data structure operates on a First-In, First-Out (FIFO) basis?",
            "options": ["Stack", "Queue", "Binary Tree", "Hash Map"],
            "correct": "Queue"
        },
        {
            "id": "tech-2",
            "question": "What does SQL stand for?",
            "options": ["Structured Query Language", "Sequential Query Loop", "Style Query Language", "Simple Query Layout"],
            "correct": "Structured Query Language"
        },
        {
            "id": "tech-3",
            "question": "Which HTML tag is used to reference external JavaScript files?",
            "options": ["<link>", "<style>", "<script>", "<js>"],
            "correct": "<script>"
        }
    ]
}

@assessment_bp.route('/questions', methods=['GET'])
def get_questions():
    """Returns the set of personality, skill, interest, and technical questions."""
    return jsonify(ASSESSMENT_QUESTIONS), 200

@assessment_bp.route('/submit', methods=['POST'])
@token_required
def submit_assessment(current_user):
    """
    Submits user response answers, grades technical scores,
    persists in assessments table, and updates user profile score metrics.
    """
    user_id = current_user["id"]
    data = request.get_json() or {}
    
    interests = data.get("interests", []) # list of names (e.g. ['coding', 'statistics'])
    skills_ratings = data.get("skills", {}) # dict of id to rating (e.g. {'skl-1': 4})
    personality_ratings = data.get("personality", {}) # dict (e.g. {'per-1': 5})
    technical_answers = data.get("technical", {}) # dict of q_id to answer (e.g. {'tech-1': 'Queue'})
    
    # Calculate assessment score based on technical correctness and overall completions
    tech_correct = 0
    for q in ASSESSMENT_QUESTIONS["technical"]:
        q_id = q["id"]
        if technical_answers.get(q_id) == q["correct"]:
            tech_correct += 1
            
    # Max tech score = 60 (20 pts per correct answer)
    tech_score = tech_correct * 20
    
    # Self-ratings baseline score (max 40 pts)
    ratings_sum = sum(int(val) for val in skills_ratings.values()) if skills_ratings else 0
    ratings_max = len(ASSESSMENT_QUESTIONS["skills"]) * 5
    self_score = int((ratings_sum / ratings_max) * 40) if ratings_max > 0 else 0
    
    final_score = tech_score + self_score
    
    # Save to assessments table
    try:
        database.execute_db(
            """
            INSERT INTO assessments 
            (user_id, personality_scores, technical_scores, interests_list, skills_list)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                user_id,
                json.dumps(personality_ratings),
                json.dumps(technical_answers),
                json.dumps(interests),
                json.dumps(skills_ratings)
            )
        )
        
        # Update user record with score
        database.execute_db(
            "UPDATE users SET assessment_score = %s WHERE id = %s",
            (final_score, user_id)
        )
        
        # Add notifications for user dashboard
        database.execute_db(
            "INSERT INTO notifications (user_id, message, type) VALUES (%s, %s, %s)",
            (user_id, f"Assessment completed successfully! You scored {final_score}/100. Check your recommended career paths now.", "recommendation")
        )
        
        return jsonify({
            "message": "Assessment submitted and scored successfully!",
            "assessment_score": final_score,
            "correct_answers": tech_correct,
            "total_technical": len(ASSESSMENT_QUESTIONS["technical"])
        }), 201
        
    except Exception as e:
        return jsonify({"message": f"Submission failed: {str(e)}"}), 500
