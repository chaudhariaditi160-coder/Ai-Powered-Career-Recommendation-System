import random

# Predefined conversational items for wow factor
KNOWLEDGE_BASE = {
    "resume": [
        "To increase your ATS score, format your resume with standard sections: 'Experience', 'Education', 'Projects', and 'Skills'. Avoid tables, shapes, and complex layouts which parser engines struggle with.",
        "Always tailor your resume for the specific job description by directly incorporating keyword skills mentioned in the listing.",
        "Ensure your experience bullet points use action verbs and follow the XYZ formula: 'Accomplished [X] as measured by [Y], by doing [Z]'."
    ],
    "interview": [
        "In behavioral interviews, frame your answers with the STAR technique: Situation, Task, Action, and Result. Make sure the Result includes quantitative metrics if possible.",
        "For technical sessions, explain your thought process out loud. Interviewers care as much about how you think as they do about finding the correct final code.",
        "Research the company's tech stack, culture, and core values prior to the interview. Prepare 2-3 thoughtful questions to ask them at the end."
    ],
    "skills": [
        "Start learning new technical skills by building mini-projects rather than just watching lectures. Code active projects, save them on GitHub, and document your learnings.",
        "Do not ignore soft skills like communication, empathy, and active listening. These are crucial for career progression and team leading roles.",
        "Try to build a T-shaped profile: have broad knowledge across multiple areas, and deep, specialized expertise in one specific domain."
    ],
    "greetings": [
        "Hello! I am your AI Career Mentor. I'm here to help you analyze career paths, find roadmaps, improve your resume, and practice for interviews. What's on your mind today?",
        "Hi there! Ready to take the next step in your professional journey? Tell me what field or challenge you are working on.",
        "Welcome! How can I assist with your career development today? You can ask about resumes, mock interviews, or transitions."
    ]
}

def generate_chatbot_response(user_message, user_profile=None):
    """
    Analyzes user message keywords and returns custom career advisor replies,
    embedding profile data (like name, career goals) if available.
    """
    msg = user_message.lower().strip()
    
    # Context gathering
    user_name = user_profile.get('name', 'there') if user_profile else 'there'
    career_goal = user_profile.get('career_goal', '') if user_profile else ''
    
    # Greetings
    if any(greet in msg for greet in ["hello", "hi", "hey", "greetings", "yo"]):
        resp = random.choice(KNOWLEDGE_BASE["greetings"])
        return resp.replace("there", user_name)
        
    # Resume queries
    if any(k in msg for k in ["resume", "ats", "cv", "portfolio"]):
        advice = random.choice(KNOWLEDGE_BASE["resume"])
        return f"Hi {user_name}, here is some advice regarding your resume/portfolio:\n\n{advice}\n\nFeel free to upload your resume PDF to our 'Resume Analyzer' tab for a complete ATS review!"
        
    # Interview queries
    if any(k in msg for k in ["interview", "mock", "question", "hired", "recruiter"]):
        advice = random.choice(KNOWLEDGE_BASE["interview"])
        return f"Great question! Preparation is key. {advice}\n\nYou can head over to our 'Mock Interview' tab to test your skills in real-time and get scored feedback!"
        
    # Skills queries
    if any(k in msg for k in ["skill", "learn", "course", "study", "bootcamp"]):
        advice = random.choice(KNOWLEDGE_BASE["skills"])
        return f"Regarding skill development: {advice}\n\nOur 'Roadmap' and 'Courses' sections can automatically outline step-by-step tracks based on your missing skills!"
        
    # Career transition or match queries
    if any(k in msg for k in ["path", "job", "career", "role", "recommend"]):
        if career_goal:
            return f"I see your current career goal is set to **{career_goal}**. That's a great field with strong growth! I suggest completing the 'Assessment' and uploading a resume. I can then analyze your skill gap and suggest specific courses to fast-track your progress."
        else:
            return "Finding the right career path starts with matching your core interests and technical skills. Try taking our 5-part assessment! Our ML engine will evaluate your responses and recommend the top 5 fields with growth predictions."
            
    # Default fallback response
    return f"Thanks for sharing that, {user_name}! In my experience, the best way to advance is by mapping your target role's skills against your current profile, and working on 1 specific project per month. What specific role or skill are you looking to master next?"
