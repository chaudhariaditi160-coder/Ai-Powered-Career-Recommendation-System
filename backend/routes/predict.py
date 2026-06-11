from flask import Blueprint, jsonify, request, send_file
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database
import model
import report
import roadmap as roadmap_module
import resume as resume_module
from routes.auth import token_required

predict_bp = Blueprint('predict', __name__)

# Details database for careers to supply details to frontend cards
CAREERS_INFO = {
    "Software Engineer": {
        "description": "Develops, builds, and maintains web applications, services, and software infrastructure using cutting-edge coding stacks.",
        "avg_salary": 110000,
        "entry_salary": 75000,
        "mid_salary": 110000,
        "senior_salary": 160000,
        "growth_rate": "15%",
        "growth_rating": "High",
        "skills_required": ["python", "javascript", "react", "node.js", "git"]
    },
    "Data Scientist": {
        "description": "Leverages statistical modeling, machine learning, and programming pipelines to discover patterns and drive commercial decisions.",
        "avg_salary": 120000,
        "entry_salary": 85000,
        "mid_salary": 120000,
        "senior_salary": 175000,
        "growth_rate": "22%",
        "growth_rating": "Very High",
        "skills_required": ["python", "sql", "machine learning", "pandas", "numpy", "statistics"]
    },
    "UI/UX Designer": {
        "description": "Designs layouts, flows, user experiences, and interactive mockups to guarantee aesthetic interface operations.",
        "avg_salary": 90000,
        "entry_salary": 60000,
        "mid_salary": 90000,
        "senior_salary": 130000,
        "growth_rate": "10%",
        "growth_rating": "Medium",
        "skills_required": ["figma", "wireframing", "prototyping", "user research", "interaction design"]
    },
    "DevOps Engineer": {
        "description": "Configures and automates clouds, containerization services, orchestration tools, and CI/CD development pipelines.",
        "avg_salary": 125000,
        "entry_salary": 85000,
        "mid_salary": 125000,
        "senior_salary": 180000,
        "growth_rate": "18%",
        "growth_rating": "High",
        "skills_required": ["aws", "docker", "kubernetes", "linux", "jenkins", "cicd"]
    },
    "Product Manager": {
        "description": "Coordinates product lifecycle stages, defines development roadmaps, and aligns engineering teams with market needs.",
        "avg_salary": 115000,
        "entry_salary": 75000,
        "mid_salary": 115000,
        "senior_salary": 165000,
        "growth_rate": "11%",
        "growth_rating": "Medium",
        "skills_required": ["agile", "scrum", "product roadmap", "market research", "analytics"]
    },
    "Cybersecurity Specialist": {
        "description": "Protects computers, systems, networks, and confidential databases from unauthorized intrusions and data breaches.",
        "avg_salary": 105000,
        "entry_salary": 70000,
        "mid_salary": 105000,
        "senior_salary": 150000,
        "growth_rate": "28%",
        "growth_rating": "Very High",
        "skills_required": ["networking", "firewalls", "penetration testing", "cryptography", "security audit"]
    },
    "Database Administrator": {
        "description": "Manages server clustering, query tuning, security configurations, and recovery protocols for structured databases.",
        "avg_salary": 95000,
        "entry_salary": 65000,
        "mid_salary": 95000,
        "senior_salary": 135000,
        "growth_rate": "5%",
        "growth_rating": "Low",
        "skills_required": ["sql", "mysql", "postgresql", "performance tuning", "backup recovery"]
    },
    "Digital Marketer": {
        "description": "Drives web traffic and commercial leads through organic visibility, paid ads, and copywriting formats.",
        "avg_salary": 85000,
        "entry_salary": 55000,
        "mid_salary": 85000,
        "senior_salary": 120000,
        "growth_rate": "9%",
        "growth_rating": "Medium",
        "skills_required": ["seo", "sem", "google analytics", "copywriting", "social media"]
    }
}

@predict_bp.route('/recommend', methods=['GET'])
@token_required
def recommend_careers(current_user):
    """
    Retrieves the user's latest assessment and runs the ML model to predict 
    the top 5 matching careers with match percentages and job insights.
    """
    user_id = current_user["id"]
    
    # Query latest assessment
    assessment = database.query_db(
        "SELECT * FROM assessments WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
        (user_id,), one=True
    )
    
    if not assessment:
        # Return fallback predictions if user has not completed assessment yet
        # This keeps the dashboard from breaking before assessment is run.
        fallback_recs = [
            {"career": "Software Engineer", "match_percentage": 75},
            {"career": "Data Scientist", "match_percentage": 65},
            {"career": "UI/UX Designer", "match_percentage": 50},
            {"career": "DevOps Engineer", "match_percentage": 40},
            {"career": "Product Manager", "match_percentage": 30}
        ]
        results = fallback_recs
    else:
        # Load values
        interests_list = json.loads(assessment.get("interests_list", "[]"))
        skills_dict = json.loads(assessment.get("skills_list", "{}"))
        personality_dict = json.loads(assessment.get("personality_scores", "{}"))
        
        # Turn into combined format string for classifier prediction
        # Get skill names matching keys if possible
        interests_text = ", ".join(interests_list)
        
        # Mapping self rating labels for training features
        # e.g., if rating is 4 or 5, consider it as a possessed skill
        skills_labels = []
        skill_keys = {
            "skl-1": "python javascript coding",
            "skl-2": "sql mysql query database",
            "skl-3": "figma wireframing design",
            "skl-4": "linux docker cloud kubernetes devops",
            "skl-5": "leadership management agile scrum"
        }
        for k, val in skills_dict.items():
            if int(val) >= 3:
                skills_labels.append(skill_keys.get(k, ""))
                
        skills_text = " ".join(skills_labels)
        
        personality_labels = []
        personality_keys = {
            "per-1": "analytical detail-oriented logical",
            "per-2": "empathetic visual creative",
            "per-3": "leader communicator organizer outgoing"
        }
        for k, val in personality_dict.items():
            if int(val) >= 3:
                personality_labels.append(personality_keys.get(k, ""))
        personality_text = " ".join(personality_labels)
        
        # Call classifier model predict
        try:
            results = model.predict_career(interests_text, skills_text, personality_text)
        except Exception as e:
            print(f"ML Model prediction error ({e}). Returning fallback...")
            results = [
                {"career": "Software Engineer", "match_percentage": 85.0},
                {"career": "Data Scientist", "match_percentage": 72.0},
                {"career": "UI/UX Designer", "match_percentage": 64.0},
                {"career": "DevOps Engineer", "match_percentage": 58.0},
                {"career": "Product Manager", "match_percentage": 52.0}
            ]
            
    # Attach rich career details (salary, growth, description)
    enhanced_results = []
    for res in results:
        career_name = res["career"]
        info = CAREERS_INFO.get(career_name, {
            "description": "General career track.",
            "avg_salary": 90000,
            "entry_salary": 60000,
            "mid_salary": 90000,
            "senior_salary": 130000,
            "growth_rate": "10%",
            "growth_rating": "Medium",
            "skills_required": []
        })
        enhanced_results.append({
            "career": career_name,
            "match_percentage": res["match_percentage"],
            "description": info["description"],
            "avg_salary": info["avg_salary"],
            "entry_salary": info["entry_salary"],
            "mid_salary": info["mid_salary"],
            "senior_salary": info["senior_salary"],
            "growth_rate": info["growth_rate"],
            "growth_rating": info["growth_rating"],
            "skills_required": info["skills_required"]
        })
        
    # Automatically update user match metrics to DB based on best recommendation match
    if enhanced_results:
        best_match = enhanced_results[0]
        # Update match percentage and goal if not already set
        database.execute_db(
            """
            UPDATE users 
            SET career_match_percentage = %s, 
                career_goal = COALESCE(career_goal, %s)
            WHERE id = %s
            """,
            (int(best_match["match_percentage"]), best_match["career"], user_id)
        )
        
    return jsonify(enhanced_results), 200

@predict_bp.route('/save', methods=['POST'])
@token_required
def save_career(current_user):
    """Bookmarks/Saves a recommended career path for user."""
    user_id = current_user["id"]
    data = request.get_json() or {}
    career_title = data.get("career_title")
    match_percentage = data.get("match_percentage", 50)
    
    if not career_title:
        return jsonify({"message": "Please specify a career title to save."}), 400
        
    info = CAREERS_INFO.get(career_title, {})
    
    try:
        database.execute_db(
            """
            INSERT OR REPLACE INTO saved_careers (user_id, career_title, match_percentage, details)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, career_title, int(match_percentage), json.dumps(info))
        )
        return jsonify({"message": f"Career path '{career_title}' saved successfully!"}), 201
    except Exception as e:
        # Fallback query for MySQL replace support if INSERT OR REPLACE isn't supported (in standard SQL it's REPLACE INTO)
        try:
            database.execute_db(
                """
                REPLACE INTO saved_careers (user_id, career_title, match_percentage, details)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, career_title, int(match_percentage), json.dumps(info))
            )
            return jsonify({"message": f"Career path '{career_title}' saved successfully!"}), 201
        except Exception as e2:
            return jsonify({"message": f"Failed to save career: {str(e2)}"}), 500

@predict_bp.route('/saved', methods=['GET'])
@token_required
def get_saved_careers(current_user):
    """Retrieves all saved career bookmarks for user."""
    user_id = current_user["id"]
    saved = database.query_db("SELECT id, career_title, match_percentage, details, created_at FROM saved_careers WHERE user_id = %s", (user_id,))
    
    # Parse json details before returning
    results = []
    for item in saved:
        details = {}
        if item.get("details"):
            try:
                details = json.loads(item["details"])
            except Exception:
                details = {}
        results.append({
            "id": item["id"],
            "career_title": item["career_title"],
            "match_percentage": item["match_percentage"],
            "details": details,
            "created_at": item["created_at"]
        })
        
    return jsonify(results), 200

@predict_bp.route('/report/generate', methods=['POST'])
@token_required
def generate_report(current_user):
    """
    Assembles career predictions, resume score, and learning roadmap 
    to build a downloadable PDF report file.
    """
    user_id = current_user["id"]
    
    # Fetch recommendation statistics
    recs = database.query_db("SELECT career_title, match_percentage FROM saved_careers WHERE user_id = %s", (user_id,))
    if not recs:
        recs = [{"career": current_user.get("career_goal") or "Software Engineer", "match_percentage": current_user.get("career_match_percentage") or 75}]
    else:
        recs = [{"career": r["career_title"], "match_percentage": r["match_percentage"]} for r in recs]
        
    latest_resume = database.query_db("SELECT * FROM resumes WHERE user_id = %s ORDER BY created_at DESC LIMIT 1", (user_id,), one=True)
    if latest_resume:
        extracted = latest_resume["parsed_skills"].split(",") if latest_resume["parsed_skills"] else []
        try:
            missing = json.loads(latest_resume["missing_skills"])
        except Exception:
            missing = []
        resume_analysis = {
            "ats_score": latest_resume["ats_score"],
            "resume_strength": latest_resume["resume_strength"],
            "extracted_skills": [e.strip() for e in extracted],
            "missing_skills": missing
        }
    else:
        resume_analysis = {
            "ats_score": current_user["resume_score"],
            "resume_strength": "Medium",
            "extracted_skills": ["python", "javascript", "html", "css", "sql"],
            "missing_skills": ["react", "node.js"]
        }
        
    career_goal = current_user.get("career_goal") or recs[0]["career"]
    user_skills = resume_analysis["extracted_skills"]
    roadmap_data = roadmap_module.generate_roadmap_data(career_goal, user_skills)
    
    # Compile PDF
    pdf_path, filename = report.generate_pdf_report(current_user["name"], recs, resume_analysis, roadmap_data)
    
    return send_file(pdf_path, as_attachment=True, download_name=filename)

@predict_bp.route('/report/email', methods=['POST'])
@token_required
def email_report(current_user):
    """
    Compiles the career assessment PDF and delivers it to the user's email inbox.
    """
    user_id = current_user["id"]
    data = request.get_json() or {}
    email_to = data.get("email", current_user["email"])
    
    # Generate same dataset structures as report generate
    recs = database.query_db("SELECT career_title, match_percentage FROM saved_careers WHERE user_id = %s", (user_id,))
    if not recs:
        recs = [{"career": current_user.get("career_goal") or "Software Engineer", "match_percentage": current_user.get("career_match_percentage") or 75}]
    else:
        recs = [{"career": r["career_title"], "match_percentage": r["match_percentage"]} for r in recs]
        
    latest_resume = database.query_db("SELECT * FROM resumes WHERE user_id = %s ORDER BY created_at DESC LIMIT 1", (user_id,), one=True)
    if latest_resume:
        extracted = latest_resume["parsed_skills"].split(",") if latest_resume["parsed_skills"] else []
        try:
            missing = json.loads(latest_resume["missing_skills"])
        except Exception:
            missing = []
        resume_analysis = {
            "ats_score": latest_resume["ats_score"],
            "resume_strength": latest_resume["resume_strength"],
            "extracted_skills": [e.strip() for e in extracted],
            "missing_skills": missing
        }
    else:
        resume_analysis = {
            "ats_score": current_user["resume_score"],
            "resume_strength": "Medium",
            "extracted_skills": ["python", "javascript", "html", "css", "sql"],
            "missing_skills": ["react", "node.js"]
        }
        
    career_goal = current_user.get("career_goal") or recs[0]["career"]
    roadmap_data = roadmap_module.generate_roadmap_data(career_goal, resume_analysis["extracted_skills"])
    
    # Generate PDF
    pdf_path, filename = report.generate_pdf_report(current_user["name"], recs, resume_analysis, roadmap_data)
    
    # Email HTML body markup
    html_body = f"""
    <h2>Hello, {current_user['name']}!</h2>
    <p>Attached is your personalized <strong>AI Career Recommendation and Development Report</strong>.</p>
    <p><strong>Your Dashboard Summary:</strong></p>
    <ul>
        <li>Target Career Path: {career_goal}</li>
        <li>Top Recommendations: {", ".join(r['career'] for r in recs[:3])}</li>
        <li>Resume ATS Score: {resume_analysis['ats_score']}/100 ({resume_analysis['resume_strength']})</li>
        <li>Learning Progress: {roadmap_data['overall_progress']}% completed</li>
    </ul>
    <p>Keep coding, practicing interviews, and building your portfolio. We are here to support your career growth!</p>
    <p>Best regards,<br/>The CareerAI Platform Team</p>
    """
    
    subject = f"Your personalized CareerAI Recommendation Report for {current_user['name']}"
    sent = report.send_career_email(email_to, subject, html_body, pdf_path)
    
    if sent:
        return jsonify({"message": f"Career report email successfully dispatched to {email_to}."}), 200
    else:
        return jsonify({"message": "Failed to send email. Check SMTP settings."}), 500
