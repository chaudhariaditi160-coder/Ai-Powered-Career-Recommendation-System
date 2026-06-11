ROADMAP_TEMPLATES = {
    "Software Engineer": {
        "steps": [
            {
                "stage": "Beginner",
                "title": "Programming Core & Fundamentals",
                "description": "Master coding basics, flow control, object-oriented concepts, and source control.",
                "skills": ["python", "javascript", "git", "html", "css"]
            },
            {
                "stage": "Intermediate",
                "title": "Data Structures & Advanced Coding",
                "description": "Understand complex algorithms, data structures (stacks, queues, trees), and API building.",
                "skills": ["react", "node.js", "data structures", "algorithms", "rest api"]
            },
            {
                "stage": "Advanced",
                "title": "System Architecture & Scalability",
                "description": "Learn cloud integration, database scaling, microservices, and performance tuning.",
                "skills": ["aws", "docker", "kubernetes", "system design", "mongodb"]
            }
        ]
    },
    "Data Scientist": {
        "steps": [
            {
                "stage": "Beginner",
                "title": "Statistical Foundations & Querying",
                "description": "Establish basic statistics, linear algebra, and data retrieval structures using SQL.",
                "skills": ["python", "sql", "statistics"]
            },
            {
                "stage": "Intermediate",
                "title": "Data Wrangling & Machine Learning",
                "description": "Learn to load, clean, analyze data, and build standard predictive machine learning models.",
                "skills": ["pandas", "numpy", "machine learning", "scikit-learn", "data visualization"]
            },
            {
                "stage": "Advanced",
                "title": "Deep Learning & Production Deployments",
                "description": "Build neural networks, utilize large language models, and scale pipeline deployments on cloud systems.",
                "skills": ["deep learning", "nlp", "tableau", "model deployment"]
            }
        ]
    },
    "UI/UX Designer": {
        "steps": [
            {
                "stage": "Beginner",
                "title": "Design Principles & Fundamentals",
                "description": "Understand typography, layouts, colors, and human-computer interactions.",
                "skills": ["design principles", "figma", "sketch"]
            },
            {
                "stage": "Intermediate",
                "title": "Wireframing & Prototyping",
                "description": "Build high-fidelity layouts, prototypes, and conduct initial user testing iterations.",
                "skills": ["wireframing", "prototyping", "user research", "interaction design"]
            },
            {
                "stage": "Advanced",
                "title": "Design Systems & High-Fidelity Hand-offs",
                "description": "Organize large-scale components, reusable styling libraries, and work closely with developers.",
                "skills": ["design systems", "adobe xd", "usability testing"]
            }
        ]
    },
    "DevOps Engineer": {
        "steps": [
            {
                "stage": "Beginner",
                "title": "Operating Systems & Networking Basics",
                "description": "Establish a strong command over Linux shells, scripting, and basic IP networking.",
                "skills": ["linux", "bash", "git", "networking"]
            },
            {
                "stage": "Intermediate",
                "title": "Containers & Integration Pipelines",
                "description": "Containerize software and build automation frameworks for build/test processes.",
                "skills": ["aws", "docker", "jenkins", "cicd"]
            },
            {
                "stage": "Advanced",
                "title": "Orchestration & Infrastructure-as-Code",
                "description": "Manage multi-container deployments and write code representing cloud environments.",
                "skills": ["kubernetes", "terraform", "ansible", "cloud security"]
            }
        ]
    },
    "Product Manager": {
        "steps": [
            {
                "stage": "Beginner",
                "title": "Fundamentals of Product Management",
                "description": "Learn standard frameworks, lifecycle steps, and working within agile environments.",
                "skills": ["agile", "scrum", "communication"]
            },
            {
                "stage": "Intermediate",
                "title": "Data Insights & Roadmap Planning",
                "description": "Collect user feedback, analyze target markets, and format timelines for release tasks.",
                "skills": ["product roadmap", "market research", "analytics", "jira"]
            },
            {
                "stage": "Advanced",
                "title": "Strategy & Leadership",
                "description": "Define product positioning, establish financial viability, and coordinate across business domains.",
                "skills": ["product strategy", "business strategy", "stakeholder management"]
            }
        ]
    },
    "Cybersecurity Specialist": {
        "steps": [
            {
                "stage": "Beginner",
                "title": "Core Networking & Systems",
                "description": "Study network configurations, routing protocols, and operate command line shells.",
                "skills": ["networking", "linux", "security basics"]
            },
            {
                "stage": "Intermediate",
                "title": "Vulnerability Analysis & Firewalls",
                "description": "Configure rules to restrict access, capture traffic, and run network security audits.",
                "skills": ["firewalls", "penetration testing", "wireshark", "cryptography"]
            },
            {
                "stage": "Advanced",
                "title": "Threat Intelligence & Security Operations",
                "description": "Build systems for security event monitoring, investigate incidents, and handle responses.",
                "skills": ["security audit", "siem", "incident response", "malware analysis"]
            }
        ]
    },
    "Database Administrator": {
        "steps": [
            {
                "stage": "Beginner",
                "title": "SQL Querying & DB Design",
                "description": "Understand structured schemas, writing statements, and relations normalization.",
                "skills": ["sql", "mysql", "database design"]
            },
            {
                "stage": "Intermediate",
                "title": "Database Optimization",
                "description": "Write indices, tune queries, and manage transactional safety configurations.",
                "skills": ["postgresql", "performance tuning", "backup recovery", "nosql"]
            },
            {
                "stage": "Advanced",
                "title": "Clustering & Data High-Availability",
                "description": "Manage database servers across server clusters and setup mirroring/replication backups.",
                "skills": ["oracle", "replication", "database clustering", "cloud storage"]
            }
        ]
    },
    "Digital Marketer": {
        "steps": [
            {
                "stage": "Beginner",
                "title": "Marketing Channels & Foundations",
                "description": "Study target demographics, outline copy guidelines, and run organic social posts.",
                "skills": ["copywriting", "social media", "marketing basics"]
            },
            {
                "stage": "Intermediate",
                "title": "Search Visibility & Web Analytics",
                "description": "Optimize content to search engines and read metrics tools to gauge visitor traffic.",
                "skills": ["seo", "sem", "google analytics", "content marketing"]
            },
            {
                "stage": "Advanced",
                "title": "Growth Campaigns & Email Automations",
                "description": "Configure complex email drips, target ads based on retargeting pixels, and manage budgets.",
                "skills": ["email marketing", "adwords", "brand strategy", "conversion rates"]
            }
        ]
    }
}

COURSES_DATABASE = [
    # Software Engineering
    {"id": "c1", "title": "Programming for Everybody (Getting Started with Python)", "provider": "Coursera - University of Michigan", "skill": "python", "level": "Beginner", "rating": 4.8, "duration": "12 hours"},
    {"id": "c2", "title": "Modern JavaScript From The Beginning", "provider": "Udemy", "skill": "javascript", "level": "Beginner", "rating": 4.7, "duration": "21 hours"},
    {"id": "c3", "title": "Front-End Web Development with React", "provider": "Coursera - HKUST", "skill": "react", "level": "Intermediate", "rating": 4.6, "duration": "30 hours"},
    {"id": "c4", "title": "Node.js, Express, MongoDB & More", "provider": "Udemy", "skill": "node.js", "level": "Intermediate", "rating": 4.8, "duration": "42 hours"},
    {"id": "c5", "title": "Version Control with Git", "provider": "Coursera - Atlassian", "skill": "git", "level": "Beginner", "rating": 4.7, "duration": "5 hours"},
    {"id": "c6", "title": "Data Structures and Algorithms Specialization", "provider": "Coursera - UC San Diego", "skill": "data structures", "level": "Intermediate", "rating": 4.6, "duration": "80 hours"},
    
    # Data Science
    {"id": "c7", "title": "SQL for Data Science", "provider": "Coursera - UC Davis", "skill": "sql", "level": "Beginner", "rating": 4.6, "duration": "14 hours"},
    {"id": "c8", "title": "Applied Data Science with Python Specialization", "provider": "Coursera - University of Michigan", "skill": "pandas", "level": "Intermediate", "rating": 4.5, "duration": "60 hours"},
    {"id": "c9", "title": "Machine Learning with Python", "provider": "Coursera - IBM", "skill": "machine learning", "level": "Intermediate", "rating": 4.7, "duration": "22 hours"},
    {"id": "c10", "title": "Deep Learning Specialization", "provider": "Coursera - DeepLearning.AI", "skill": "deep learning", "level": "Advanced", "rating": 4.9, "duration": "90 hours"},
    {"id": "c11", "title": "Introduction to Probability and Statistics", "provider": "edX - MIT", "skill": "statistics", "level": "Beginner", "rating": 4.8, "duration": "48 hours"},
    
    # UI/UX
    {"id": "c12", "title": "Google UX Design Professional Certificate", "provider": "Coursera - Google", "skill": "figma", "level": "Beginner", "rating": 4.8, "duration": "120 hours"},
    {"id": "c13", "title": "User Experience Research & Design", "provider": "Coursera - University of Michigan", "skill": "user research", "level": "Intermediate", "rating": 4.7, "duration": "40 hours"},
    {"id": "c14", "title": "Figma UI/UX Design Essentials", "provider": "Udemy", "skill": "prototyping", "level": "Beginner", "rating": 4.8, "duration": "15 hours"},
    
    # DevOps
    {"id": "c15", "title": "AWS Certified Cloud Practitioner Ultimate Exam Prep", "provider": "Udemy", "skill": "aws", "level": "Beginner", "rating": 4.7, "duration": "18 hours"},
    {"id": "c16", "title": "Docker Technologies for DevOps and Developers", "provider": "Udemy", "skill": "docker", "level": "Intermediate", "rating": 4.6, "duration": "8 hours"},
    {"id": "c17", "title": "Certified Kubernetes Administrator (CKA)", "provider": "Udemy", "skill": "kubernetes", "level": "Advanced", "rating": 4.8, "duration": "22 hours"},
    
    # General fallback courses for unlisted skills
    {"id": "c18", "title": "Agile PM Specialization", "provider": "Coursera", "skill": "agile", "level": "Beginner", "rating": 4.7, "duration": "30 hours"},
    {"id": "c19", "title": "Google SEO Fundamentals", "provider": "Coursera - UC Davis", "skill": "seo", "level": "Intermediate", "rating": 4.6, "duration": "15 hours"},
    {"id": "c20", "title": "Complete Cyber Security Course", "provider": "Udemy", "skill": "penetration testing", "level": "Intermediate", "rating": 4.7, "duration": "25 hours"}
]

def generate_roadmap_data(career_path, user_skills=[]):
    """
    Returns a customized learning roadmap structure for a career path,
    flagging skills the user already possesses and recommending courses for the ones they lack.
    """
    # Normalize career path name
    career_key = None
    for key in ROADMAP_TEMPLATES:
        if key.lower() in career_path.lower() or career_path.lower() in key.lower():
            career_key = key
            break
            
    if not career_key:
        career_key = "Software Engineer" # Default
        
    template = ROADMAP_TEMPLATES[career_key]
    user_skills_normalized = [s.lower() for s in user_skills]
    
    roadmap_steps = []
    
    for step in template["steps"]:
        step_completed_skills = []
        step_missing_skills = []
        
        for skill in step["skills"]:
            if skill.lower() in user_skills_normalized:
                step_completed_skills.append(skill)
            else:
                step_missing_skills.append(skill)
                
        # Calculate completion rate of this stage
        total_skills = len(step["skills"])
        completion = round((len(step_completed_skills) / total_skills) * 100) if total_skills > 0 else 0
        
        # Recommendations of courses for missing skills in this stage
        course_recs = []
        for missing_skill in step_missing_skills:
            # Find a course that teaches this skill
            for c in COURSES_DATABASE:
                if c["skill"] == missing_skill:
                    course_recs.append(c)
                    break
                    
        # If no courses found, provide a mock course
        if not course_recs and step_missing_skills:
            for skill in step_missing_skills:
                course_recs.append({
                    "id": f"mock-{skill}",
                    "title": f"Mastering {skill.capitalize()} for Industry",
                    "provider": "CareerAI Academy",
                    "skill": skill,
                    "level": step["stage"],
                    "rating": 4.5,
                    "duration": "10 hours"
                })
                
        roadmap_steps.append({
            "stage": step["stage"],
            "title": step["title"],
            "description": step["description"],
            "skills": step["skills"],
            "completed_skills": step_completed_skills,
            "missing_skills": step_missing_skills,
            "completion_percentage": completion,
            "recommended_courses": course_recs[:3] # Limit to 3 recommendations
        })
        
    return {
        "career_path": career_key,
        "overall_progress": round(sum(s["completion_percentage"] for s in roadmap_steps) / len(roadmap_steps)),
        "steps": roadmap_steps
    }
