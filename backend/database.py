import os
import sqlite3
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_TYPE = os.getenv("DB_TYPE", "sqlite") # 'mysql' or 'sqlite'
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "career_ai_db")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))

SQLITE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "career_ai.db")

def get_db_connection():
    if DB_TYPE == "mysql":
        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE,
                port=MYSQL_PORT
            )
            return conn
        except ImportError:
            print("WARNING: mysql-connector-python not installed. Falling back to SQLite.")
        except Exception as e:
            print(f"WARNING: MySQL connection failed ({e}). Falling back to SQLite.")
            
    # SQLite fallback
    conn = sqlite3.connect(SQLITE_FILE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def execute_db(query, args=()):
    """Executes a command (INSERT, UPDATE, DELETE). Returns lastrowid or affected row count."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if isinstance(conn, sqlite3.Connection):
            # SQLite uses ? placeholder instead of %s
            query_formatted = query.replace("%s", "?")
            cursor.execute(query_formatted, args)
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        else:
            # MySQL
            cursor.execute(query, args)
            conn.commit()
            last_id = cursor.lastrowid
            return last_id or cursor.rowcount
    except Exception as e:
        conn.rollback()
        print(f"Database error: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()

def query_db(query, args=(), one=False):
    """Executes a query and returns results as lists of dicts."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if isinstance(conn, sqlite3.Connection):
            query_formatted = query.replace("%s", "?")
            cursor.execute(query_formatted, args)
            rows = cursor.fetchall()
            results = [dict(row) for row in rows]
        else:
            # MySQL
            cursor.execute(query, args)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            results = [dict(zip(columns, row)) for row in rows]
        
        return (results[0] if results else None) if one else results
    except Exception as e:
        print(f"Database error: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()

def init_db():
    """Initializes tables in database."""
    print(f"Initializing Database... Type: {DB_TYPE}")
    
    # Simple table structures corresponding to schema.sql
    queries = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            career_goal TEXT DEFAULT NULL,
            assessment_score INTEGER DEFAULT 0,
            resume_score INTEGER DEFAULT 0,
            career_match_percentage INTEGER DEFAULT 0,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            personality_scores TEXT,
            technical_scores TEXT,
            interests_list TEXT,
            skills_list TEXT,
            recommended_careers TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            parsed_skills TEXT,
            ats_score INTEGER DEFAULT 0,
            resume_strength TEXT DEFAULT 'Weak',
            missing_skills TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS saved_careers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            career_title TEXT NOT NULL,
            match_percentage INTEGER NOT NULL,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, career_title),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            course_name TEXT NOT NULL,
            completion_percentage INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Not Started',
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            type TEXT NOT NULL,
            is_read BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    ]
    
    # If using MySQL, adjust AUTOINCREMENT to AUTO_INCREMENT, INTEGER to INT
    if DB_TYPE == "mysql":
        # Let's import mysql.connector to check if database exists or create it
        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                port=MYSQL_PORT
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}")
            cursor.execute(f"USE {MYSQL_DATABASE}")
            
            mysql_queries = [
                """
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
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS assessments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    personality_scores TEXT,
                    technical_scores TEXT,
                    interests_list TEXT,
                    skills_list TEXT,
                    recommended_careers TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS resumes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    filename VARCHAR(255) NOT NULL,
                    filepath VARCHAR(255) NOT NULL,
                    parsed_skills TEXT,
                    ats_score INT DEFAULT 0,
                    resume_strength VARCHAR(100) DEFAULT 'Weak',
                    missing_skills TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS saved_careers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    career_title VARCHAR(255) NOT NULL,
                    match_percentage INT NOT NULL,
                    details TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE KEY user_career (user_id, career_title),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS user_progress (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    course_name VARCHAR(255) NOT NULL,
                    completion_percentage INT DEFAULT 0,
                    status VARCHAR(50) DEFAULT 'Not Started',
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS notifications (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    message VARCHAR(500) NOT NULL,
                    type VARCHAR(100) NOT NULL,
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """
            ]
            for q in mysql_queries:
                cursor.execute(q)
            conn.commit()
            cursor.close()
            conn.close()
            print("Successfully initialized MySQL database tables.")
            return
        except Exception as e:
            print(f"Failed to initialize MySQL ({e}). Defaulting initialization to SQLite.")
            
    # SQLite Setup
    conn = sqlite3.connect(SQLITE_FILE)
    cursor = conn.cursor()
    for q in queries:
        cursor.execute(q)
    conn.commit()
    cursor.close()
    conn.close()
    print("Successfully initialized SQLite database tables.")

if __name__ == "__main__":
    init_db()
