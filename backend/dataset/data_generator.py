import csv
import os
import random

# Ensure directory exists
os.makedirs(os.path.dirname(__file__), exist_ok=True)

# 1. Careers Dataset (for Recommendation ML Model)
def generate_careers_csv():
    careers_path = os.path.join(os.path.dirname(__file__), 'careers.csv')
    
    # Templates for synthetic generation
    roles = [
        "Software Engineer", 
        "Data Scientist", 
        "UI/UX Designer", 
        "DevOps Engineer", 
        "Product Manager",
        "Cybersecurity Specialist",
        "Database Administrator",
        "Digital Marketer"
    ]
    
    skills_map = {
        "Software Engineer": ["python", "javascript", "react", "node.js", "git", "data structures", "algorithms"],
        "Data Scientist": ["python", "sql", "machine learning", "pandas", "numpy", "statistics", "data visualization"],
        "UI/UX Designer": ["figma", "sketch", "wireframing", "prototyping", "user research", "interaction design"],
        "DevOps Engineer": ["aws", "docker", "kubernetes", "linux", "jenkins", "cicd", "bash"],
        "Product Manager": ["agile", "scrum", "product roadmap", "market research", "analytics", "communication"],
        "Cybersecurity Specialist": ["networking", "firewalls", "penetration testing", "cryptography", "security audit", "linux"],
        "Database Administrator": ["sql", "mysql", "postgresql", "performance tuning", "backup recovery", "database design"],
        "Digital Marketer": ["seo", "sem", "google analytics", "copywriting", "social media", "content marketing"]
    }
    
    interests_map = {
        "Software Engineer": ["coding", "problem solving", "web apps", "open source", "technology"],
        "Data Scientist": ["math", "data analysis", "statistics", "puzzles", "research"],
        "UI/UX Designer": ["drawing", "design", "human behavior", "art", "psychology"],
        "DevOps Engineer": ["automation", "cloud computing", "system administration", "networking"],
        "Product Manager": ["leadership", "business strategy", "user feedback", "organizing", "collaboration"],
        "Cybersecurity Specialist": ["hacking", "security", "privacy", "investigation", "networking"],
        "Database Administrator": ["organization", "data structure", "optimization", "system performance"],
        "Digital Marketer": ["writing", "socializing", "trends", "advertising", "behavioral psychology"]
    }
    
    personalities_map = {
        "Software Engineer": ["analytical", "logical", "problem solver", "detail-oriented"],
        "Data Scientist": ["curious", "analytical", "researcher", "logical"],
        "UI/UX Designer": ["creative", "empathetic", "observant", "visual"],
        "DevOps Engineer": ["systematic", "logical", "pragmatic", "organized"],
        "Product Manager": ["leader", "communicative", "decisive", "adaptable"],
        "Cybersecurity Specialist": ["skeptical", "detail-oriented", "analytical", "vigilant"],
        "Database Administrator": ["meticulous", "organized", "logical", "patient"],
        "Digital Marketer": ["outgoing", "creative", "persuasive", "dynamic"]
    }

    with open(careers_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["interests", "skills", "personality", "career_path"])
        
        # Generate 1500 samples
        for _ in range(1500):
            role = random.choice(roles)
            
            # Select random elements from templates to introduce variation
            skills_sample = random.sample(skills_map[role], k=random.randint(3, 5))
            # Occasionally add some random noise (skills from other roles) to simulate real-world noise
            if random.random() < 0.15:
                other_role = random.choice([r for r in roles if r != role])
                skills_sample.append(random.choice(skills_map[other_role]))
                
            interests_sample = random.sample(interests_map[role], k=random.randint(2, 4))
            personality_sample = random.sample(personalities_map[role], k=random.randint(2, 3))
            
            writer.writerow([
                ", ".join(interests_sample),
                ", ".join(skills_sample),
                ", ".join(personality_sample),
                role
            ])
    print(f"Generated careers.csv with 1500 rows at {careers_path}")

# 2. Resumes Dataset
def generate_resumes_csv():
    resumes_path = os.path.join(os.path.dirname(__file__), 'resumes.csv')
    
    roles = [
        "Software Engineer", 
        "Data Scientist", 
        "UI/UX Designer", 
        "DevOps Engineer", 
        "Product Manager",
        "Cybersecurity Specialist",
        "Database Administrator",
        "Digital Marketer"
    ]
    
    sample_templates = {
        "Software Engineer": "Experienced Software Developer with a strong background in building web applications. Highly skilled in Python, JavaScript, React, Node.js, and git. Passionate about algorithms and designing scalable backend architectures.",
        "Data Scientist": "Detail-oriented Data Scientist with expertise in statistical analysis, machine learning, and data mining. Proficient in Python, SQL, Pandas, NumPy, and Scikit-learn. Adept at turning complex datasets into actionable business insights.",
        "UI/UX Designer": "Creative UI/UX Designer specializing in user research, wireframing, and interactive prototyping. Proficient in Figma, Sketch, and Adobe Creative Suite. Dedicated to designing user-centric, aesthetically pleasing interfaces.",
        "DevOps Engineer": "Reliable DevOps Engineer with extensive experience in cloud automation and infrastructure management. Hands-on with AWS, Docker, Kubernetes, CI/CD pipelines, and Linux administration. Focuses on automation and reliability.",
        "Product Manager": "Strategic Product Manager with a track record of delivering user-friendly products. Experienced in agile methodologies, product roadmapping, customer research, and cross-functional team leadership.",
        "Cybersecurity Specialist": "Dedicated Security Specialist with focus on information security, risk mitigation, and threat analysis. Skilled in network firewalls, penetration testing, cryptography, and server hardening.",
        "Database Administrator": "Meticulous Database Administrator with deep knowledge of database architecture, clustering, backup, and performance optimization. Expert in MySQL, PostgreSQL, and SQL scripting.",
        "Digital Marketer": "Results-driven Digital Marketer specialized in driving user growth through organic and paid media. Proficient in SEO, SEM, content strategy, Google Analytics, and running campaign structures."
    }
    
    with open(resumes_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["resume_text", "category"])
        
        # Generate 100 sample resumes for reference/mock comparisons
        for _ in range(200):
            role = random.choice(roles)
            text = sample_templates[role]
            # Introduce variations in skills
            writer.writerow([text, role])
    print(f"Generated resumes.csv with 200 rows at {resumes_path}")

# 3. Jobs Dataset
def generate_jobs_csv():
    jobs_path = os.path.join(os.path.dirname(__file__), 'jobs.csv')
    
    jobs_data = [
        # Job Title, Company, Growth Rate (%), Avg Salary, Entry Salary, Mid Salary, Senior Salary, Required Skills, Industry
        ["Software Engineer", "TechCorp Solutions", "15", "110000", "75000", "110000", "160000", "python, javascript, react, git", "Technology"],
        ["Senior Software Engineer", "Innovate Labs", "12", "145000", "115000", "145000", "195000", "javascript, react, node.js, system architecture", "Technology"],
        ["Data Scientist", "DataMetrics LLC", "22", "120000", "85000", "120000", "175000", "python, sql, machine learning, statistics", "Data & Analytics"],
        ["Machine Learning Engineer", "NeuralNet Labs", "25", "135000", "95000", "135000", "190000", "python, machine learning, pytorch, pandas", "Technology"],
        ["UI/UX Designer", "Creative Studio", "10", "90000", "60000", "90000", "130000", "figma, wireframing, prototyping, user research", "Design & Media"],
        ["Lead Designer", "Apex Brands", "8", "120000", "85000", "120000", "160000", "figma, design systems, interaction design, leadership", "Design & Media"],
        ["DevOps Engineer", "CloudScale Networks", "18", "125000", "85000", "125000", "180000", "aws, docker, kubernetes, linux, cicd", "Technology / Cloud"],
        ["Site Reliability Engineer", "ScaleOps Inc", "16", "135000", "90000", "135000", "190000", "kubernetes, linux, network protocols, automation", "Technology"],
        ["Product Manager", "Alpha Products", "11", "115000", "75000", "115000", "165000", "agile, product roadmap, market research", "Business & Product"],
        ["Cybersecurity Analyst", "SecureNet Security", "28", "105000", "70000", "105000", "150000", "networking, firewalls, threat detection, security audit", "Cybersecurity"],
        ["Database Administrator", "InfoVault Systems", "5", "95000", "65000", "95000", "135000", "sql, mysql, postgresql, performance tuning", "Database Services"],
        ["Digital Marketing Manager", "GrowthFlow Media", "9", "85000", "55000", "85000", "120000", "seo, sem, google analytics, content marketing", "Marketing & Growth"]
    ]
    
    with open(jobs_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["job_title", "company", "growth_rate", "average_salary", "entry_salary", "mid_salary", "senior_salary", "skills_required", "industry"])
        
        for job in jobs_data:
            writer.writerow(job)
            
        # Add random variations to get 50 job listings
        for i in range(40):
            base_job = random.choice(jobs_data)
            company_suffixes = ["Inc", "Corp", "Partners", "Global", "Systems"]
            company_name = f"{base_job[1].split()[0]} {random.choice(company_suffixes)}"
            
            # Slightly perturb values
            growth = int(base_job[2]) + random.randint(-3, 3)
            avg_sal = int(base_job[3]) + random.randint(-5000, 5000)
            entry_sal = int(base_job[4]) + random.randint(-3000, 3000)
            mid_sal = avg_sal
            senior_sal = int(base_job[6]) + random.randint(-8000, 8000)
            
            writer.writerow([
                base_job[0],
                company_name,
                str(max(1, growth)),
                str(avg_sal),
                str(entry_sal),
                str(mid_sal),
                str(senior_sal),
                base_job[7],
                base_job[8]
            ])
            
    print(f"Generated jobs.csv with {12 + 40} rows at {jobs_path}")

if __name__ == '__main__':
    generate_careers_csv()
    generate_resumes_csv()
    generate_jobs_csv()
