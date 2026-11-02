"""
Project Configuration for Capstone 57 - Multimodal AI Tools Comparison
Student: Reshma Anandhan
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    PROJECT_NAME = "Capstone 57 – Multimodal AI Tools Comparison for Students"
    STUDENT_NAME = "Reshma Anandhan"
    VERSION = "1.0.0"
    SECRET_KEY = os.environ.get("SECRET_KEY", "capstone-57-secret-key-reshma-2026")
    
    # Paths
    DATABASE_PATH = os.environ.get("DATABASE_PATH", str(BASE_DIR / "data" / "multimodal_ai.db"))
    UPLOAD_FOLDER = str(BASE_DIR / "uploads")
    REPORTS_FOLDER = str(BASE_DIR / "reports")
    STATIC_FOLDER = str(BASE_DIR / "static")
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'mp3', 'wav', 'm4a', 'ogg', 'txt'}
    
    # Weights for Evaluation Scoring System
    WEIGHT_ACCURACY = 0.40
    WEIGHT_COMPLETENESS = 0.25
    WEIGHT_RELEVANCE = 0.20
    WEIGHT_EASE_OF_USE = 0.15
    
    # Evaluation Scale
    MAX_SCORE = 100
    MIN_SCORE = 0
