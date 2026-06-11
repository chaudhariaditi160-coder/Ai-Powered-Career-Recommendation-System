-- Career AI System Database Schema

CREATE DATABASE IF NOT EXISTS career_ai_db;
USE career_ai_db;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    career_goal VARCHAR(255) DEFAULT NULL,
    assessment_score INT DEFAULT 0,
    resume_score INT DEFAULT 0,
    career_match_percentage INT DEFAULT 0,
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Assessments Table
CREATE TABLE IF NOT EXISTS assessments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    personality_scores TEXT, -- JSON structure of personality ratings
    technical_scores TEXT,   -- JSON structure of tech rating
    interests_list TEXT,     -- JSON array of selected interests
    skills_list TEXT,        -- JSON array of selected skills
    recommended_careers TEXT, -- JSON array of top recommendations
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Resumes Table
CREATE TABLE IF NOT EXISTS resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(255) NOT NULL,
    parsed_skills TEXT,      -- Comma-separated or JSON list
    ats_score INT DEFAULT 0,
    resume_strength VARCHAR(100) DEFAULT 'Weak',
    missing_skills TEXT,     -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. Saved Careers Table
CREATE TABLE IF NOT EXISTS saved_careers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    career_title VARCHAR(255) NOT NULL,
    match_percentage INT NOT NULL,
    details TEXT,            -- Description and key metrics in JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY user_career (user_id, career_title),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 5. User Progress Table
CREATE TABLE IF NOT EXISTS user_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_name VARCHAR(255) NOT NULL,
    completion_percentage INT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'Not Started', -- 'In Progress', 'Completed'
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 6. Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message VARCHAR(500) NOT NULL,
    type VARCHAR(100) NOT NULL, -- 'assessment', 'recommendation', 'learning'
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Seed an Admin User (password is 'admin123')
-- password hash here corresponds to sha256_crypt or scrypt hash. Since we will use Werkzeug security,
-- we'll seed or handle register inside code, but having this file is a key requirements item.
