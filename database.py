"""
Database Management Module for Capstone 57
SQLite Database connection, schema creation, and initialization.
Student: Reshma Anandhan
"""
import sqlite3
import os
from pathlib import Path
from config import Config

def get_db_connection():
    """Returns a connection to the SQLite database with row_factory set to sqlite3.Row."""
    db_path = Config.DATABASE_PATH
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db(force_reseed=False):
    """Initializes tables and seeds initial benchmark and reference data."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create AI Tools Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        developer TEXT NOT NULL,
        model_version TEXT NOT NULL,
        description TEXT NOT NULL,
        features TEXT NOT NULL,
        image_support TEXT NOT NULL,
        document_support TEXT NOT NULL,
        audio_support TEXT NOT NULL,
        free_tier_limits TEXT NOT NULL,
        official_url TEXT NOT NULL,
        verified_date TEXT NOT NULL,
        badge_color TEXT NOT NULL DEFAULT 'primary',
        is_verified INTEGER NOT NULL DEFAULT 1,
        assumptions_notes TEXT
    )
    """)
    
    # Create Multimodal Test Cases Table (15 Test Cases: 5 Image, 5 Document, 5 Audio)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_code TEXT UNIQUE NOT NULL,
        modality TEXT NOT NULL, -- 'IMAGE', 'DOCUMENT', 'AUDIO'
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        test_prompt TEXT NOT NULL,
        sample_file_name TEXT,
        ground_truth_rubric TEXT NOT NULL,
        difficulty TEXT NOT NULL DEFAULT 'Intermediate'
    )
    """)
    
    # Create Evaluations Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tool_id INTEGER NOT NULL,
        test_case_id INTEGER NOT NULL,
        evaluator_name TEXT NOT NULL DEFAULT 'Reshma Anandhan',
        response_text TEXT NOT NULL,
        accuracy_score REAL NOT NULL CHECK(accuracy_score >= 0 AND accuracy_score <= 100),
        completeness_score REAL NOT NULL CHECK(completeness_score >= 0 AND completeness_score <= 100),
        relevance_score REAL NOT NULL CHECK(relevance_score >= 0 AND relevance_score <= 100),
        ease_of_use_score REAL NOT NULL CHECK(ease_of_use_score >= 0 AND ease_of_use_score <= 100),
        weighted_score REAL NOT NULL CHECK(weighted_score >= 0 AND weighted_score <= 100),
        hallucination_detected INTEGER NOT NULL DEFAULT 0,
        hallucination_details TEXT,
        unsafe_outdated_detected INTEGER NOT NULL DEFAULT 0,
        unsafe_outdated_details TEXT,
        student_notes TEXT,
        is_demo_data INTEGER NOT NULL DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (tool_id) REFERENCES tools(id) ON DELETE CASCADE,
        FOREIGN KEY (test_case_id) REFERENCES test_cases(id) ON DELETE CASCADE
    )
    """)
    
    # Create Before and After Analysis Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS before_after_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tool_id INTEGER NOT NULL,
        test_case_id INTEGER NOT NULL,
        initial_score REAL NOT NULL,
        verified_score REAL NOT NULL,
        score_delta REAL NOT NULL,
        errors_identified TEXT NOT NULL,
        fact_check_notes TEXT NOT NULL,
        improvement_strategy TEXT NOT NULL,
        verification_status TEXT NOT NULL DEFAULT 'Verified',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (tool_id) REFERENCES tools(id) ON DELETE CASCADE,
        FOREIGN KEY (test_case_id) REFERENCES test_cases(id) ON DELETE CASCADE
    )
    """)
    
    # Create Quiz Questions Table (10 Questions)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_number INTEGER UNIQUE NOT NULL,
        question TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        correct_option TEXT NOT NULL CHECK(correct_option IN ('A', 'B', 'C', 'D')),
        explanation TEXT NOT NULL,
        category TEXT NOT NULL
    )
    """)
    
    # Create Multimodal Checklist Audit Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS checklist_audits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tool_name TEXT NOT NULL,
        task_name TEXT NOT NULL,
        has_incorrect_info INTEGER NOT NULL DEFAULT 0,
        has_missing_info INTEGER NOT NULL DEFAULT 0,
        has_hallucinations INTEGER NOT NULL DEFAULT 0,
        has_unsafe_advice INTEGER NOT NULL DEFAULT 0,
        has_outdated_info INTEGER NOT NULL DEFAULT 0,
        has_source_reliability_issues INTEGER NOT NULL DEFAULT 0,
        has_privacy_risks INTEGER NOT NULL DEFAULT 0,
        risk_level TEXT NOT NULL, -- 'Low', 'Moderate', 'High', 'Critical'
        reliability_score REAL NOT NULL,
        notes TEXT,
        audit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create Reusable Prompt Library Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prompt_library (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL, -- 'IMAGE', 'DOCUMENT', 'AUDIO'
        title TEXT NOT NULL,
        prompt_text TEXT NOT NULL,
        target_outcome TEXT NOT NULL,
        recommended_tool TEXT NOT NULL,
        difficulty TEXT NOT NULL DEFAULT 'Intermediate'
    )
    """)
    
    conn.commit()
    
    # Check if tools exist; if not or if forced, seed default benchmark datasets
    cursor.execute("SELECT COUNT(*) as count FROM tools")
    tool_count = cursor.fetchone()['count']
    
    if tool_count == 0 or force_reseed:
        from data.seed_data import seed_all
        seed_all(conn, force_reseed)
    
    conn.close()

def calculate_weighted_score(accuracy, completeness, relevance, ease_of_use):
    """
    Calculates weighted score based on Capstone 57 specifications:
    Accuracy: 40%
    Completeness: 25%
    Relevance: 20%
    Ease of Use: 15%
    """
    score = (
        (float(accuracy) * Config.WEIGHT_ACCURACY) +
        (float(completeness) * Config.WEIGHT_COMPLETENESS) +
        (float(relevance) * Config.WEIGHT_RELEVANCE) +
        (float(ease_of_use) * Config.WEIGHT_EASE_OF_USE)
    )
    return round(score, 2)
