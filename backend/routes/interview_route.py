from flask import Blueprint, jsonify, request
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import interview
from routes.auth import token_required

interview_bp = Blueprint('interview_route', __name__)

@interview_bp.route('/questions', methods=['GET'])
@token_required
def get_interview_questions(current_user):
    """
    Fetches mock interview questions relevant to the user's career path.
    """
    career = current_user.get("career_goal") or "Software Engineer"
    questions = interview.get_questions_for_role(career)
    
    # Strip keywords and ideal answers so the user cannot cheat in the UI!
    client_questions = []
    for q in questions:
        client_questions.append({
            "id": q["id"],
            "type": q["type"],
            "question": q["question"]
        })
        
    return jsonify(client_questions), 200

@interview_bp.route('/evaluate', methods=['POST'])
@token_required
def evaluate_answer(current_user):
    """
    Processes a submitted mock interview response and returns score + coaching feedback.
    """
    data = request.get_json() or {}
    question_id = data.get("question_id")
    answer = data.get("answer")
    
    if not question_id or not answer:
        return jsonify({"message": "question_id and answer are required"}), 400
        
    career = current_user.get("career_goal") or "Software Engineer"
    evaluation = interview.evaluate_interview_answer(question_id, answer, career)
    
    return jsonify(evaluation), 200
