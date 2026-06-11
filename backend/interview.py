QUESTIONS_DATABASE = {
    "Software Engineer": [
        {
            "id": "se-1",
            "type": "technical",
            "question": "What is the difference between synchronous and asynchronous programming, and when would you use each?",
            "keywords": ["blocking", "non-blocking", "event loop", "callbacks", "promises", "async/await", "api", "concurrency"],
            "ideal_concepts": "Synchronous tasks run sequentially, blocking further execution. Asynchronous tasks allow other tasks to proceed while waiting, usually handled via event loops, promises, or async/await. Use async for networking, I/O, or database queries."
        },
        {
            "id": "se-2",
            "type": "technical",
            "question": "Explain how REST APIs utilize HTTP methods (GET, POST, PUT, DELETE) and status codes.",
            "keywords": ["http", "get", "post", "put", "delete", "status codes", "200", "201", "404", "500", "idempotent", "stateless"],
            "ideal_concepts": "GET retrieves data, POST creates, PUT updates, and DELETE removes. 200 OK, 201 Created denote success; 404 Not Found is user error; 500 is server error."
        },
        {
            "id": "se-3",
            "type": "behavioral",
            "question": "Describe a time when you had to resolve a difficult technical conflict with a team member.",
            "keywords": ["communication", "listen", "compromise", "collaboration", "empathy", "solution", "objective", "feedback"],
            "ideal_concepts": "The answer should follow the STAR format: state the conflict, how you listened to the other viewpoint, focused on objective facts or testing, and collaborated on a shared solution."
        }
    ],
    "Data Scientist": [
        {
            "id": "ds-1",
            "type": "technical",
            "question": "What is overfitting in machine learning, and what are three common ways to prevent it?",
            "keywords": ["overfitting", "validation", "regularization", "dropout", "cross-validation", "early stopping", "complexity", "noise"],
            "ideal_concepts": "Overfitting happens when a model learns noise instead of patterns. Prevent it by: 1) Cross-validation, 2) Regularization (L1/L2, dropout), 3) Simplification (pruning, reducing parameters), or 4) Adding more data."
        },
        {
            "id": "ds-2",
            "type": "technical",
            "question": "What is the difference between supervised and unsupervised learning? Provide examples of each.",
            "keywords": ["labeled", "unlabeled", "regression", "classification", "clustering", "k-means", "random forest", "target"],
            "ideal_concepts": "Supervised learning uses labeled training data to predict a target (e.g. classification, regression). Unsupervised learning finds patterns in unlabeled data (e.g. clustering like K-Means, dimensionality reduction like PCA)."
        },
        {
            "id": "ds-3",
            "type": "behavioral",
            "question": "Explain a complex technical data model or finding to a non-technical business stakeholder.",
            "keywords": ["simplify", "jargon", "analogy", "business value", "visualization", "metrics", "revenue", "impact"],
            "ideal_concepts": "Detail how you avoided technical jargon, utilized charts or simple analogies, and focused on business metrics (costs, conversion rate, time saved) rather than model details."
        }
    ],
    "UI/UX Designer": [
        {
            "id": "ui-1",
            "type": "technical",
            "question": "Describe your UX design process from receiving a problem statement to shipping a final mockup.",
            "keywords": ["research", "wireframes", "prototyping", "testing", "user stories", "figma", "feedback", "iteration"],
            "ideal_concepts": "Process: 1) Discover/Research, 2) Define user personas, 3) Ideate/Sketch, 4) Prototype in Figma, 5) Test with users, 6) Iterate and Hand off."
        },
        {
            "id": "ui-2",
            "type": "technical",
            "question": "What is a design system, and why is it important for scaling a product interface?",
            "keywords": ["consistency", "components", "colors", "typography", "reusable", "scale", "standards", "efficiency"],
            "ideal_concepts": "A design system is a collection of reusable components, guidelines, colors, and typography that ensures visual consistency, speeds up design/development, and simplifies scaling."
        }
    ]
}

def get_questions_for_role(role):
    """
    Retrieves mock interview questions matching a career role.
    """
    matched_role = None
    for k in QUESTIONS_DATABASE:
        if k.lower() in role.lower() or role.lower() in k.lower():
            matched_role = k
            break
            
    if not matched_role:
        # Fallback to Software Engineer questions
        matched_role = "Software Engineer"
        
    return QUESTIONS_DATABASE[matched_role]

def evaluate_interview_answer(question_id, user_answer, role):
    """
    Grades user answers against keyword parameters and length.
    Returns score out of 100 and evaluation comments.
    """
    questions = get_questions_for_role(role)
    q_item = next((q for q in questions if q["id"] == question_id), None)
    
    if not q_item:
        # Default fallback evaluator if question id not matched
        q_item = {
            "question": "General interview question",
            "keywords": ["communication", "experience", "learning", "teamwork", "solve"],
            "ideal_concepts": "Clear delivery, structured layout, and real-world examples."
        }
        
    ans_lower = user_answer.lower()
    
    # 1. Evaluate keyword coverage
    matched_keywords = []
    for kw in q_item.get("keywords", []):
        if re.search(rf"\b{re.escape(kw)}\b", ans_lower):
            matched_keywords.append(kw)
            
    keyword_score = 0
    total_keywords = len(q_item.get("keywords", []))
    if total_keywords > 0:
        keyword_score = int((len(matched_keywords) / total_keywords) * 60)
        
    # 2. Evaluate answer length/substance
    words = user_answer.split()
    length_score = 0
    if len(words) >= 50:
        length_score = 40
    elif 20 <= len(words) < 50:
        length_score = 25
    elif 5 <= len(words) < 20:
        length_score = 10
    else:
        length_score = 5
        
    total_score = keyword_score + length_score
    total_score = min(max(5, total_score), 100)
    
    # Feedback generation
    feedback_notes = []
    if total_score >= 80:
        feedback_notes.append("Excellent! Your answer is descriptive, structured, and covers core technical terminology.")
    elif total_score >= 50:
        feedback_notes.append("Good start, but you could elaborate. Try to provide concrete examples or detail the steps you'd take.")
    else:
        feedback_notes.append("Your response is brief. Try structuring your response more thoroughly and explain the 'why' behind your approach.")
        
    # Add tip about missing key terms
    missing_keywords = [kw for kw in q_item.get("keywords", []) if kw not in matched_keywords]
    if missing_keywords and total_score < 90:
        feedback_notes.append(f"Consider discussing concepts like: {', '.join(missing_keywords[:3])}.")
        
    # Add ideal answer snippet
    feedback_notes.append(f"Key concepts to address: {q_item.get('ideal_concepts', '')}")
    
    return {
        "score": total_score,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "feedback": "\n\n".join(feedback_notes)
    }
