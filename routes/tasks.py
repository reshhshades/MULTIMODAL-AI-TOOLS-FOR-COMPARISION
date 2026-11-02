"""
Multimodal Task Testing Blueprint for Capstone 57
Displays the 15 standardized test cases (5 Image, 5 Document, 5 Audio), rubrics, and downloadable sample test files.
Student: Reshma Anandhan
"""
import os
from pathlib import Path
from flask import Blueprint, render_template, request, send_from_directory, abort, current_app
from models import TestCaseModel
from config import BASE_DIR

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks')
def index():
    modality_filter = request.args.get('modality', '').upper()
    if modality_filter in ['IMAGE', 'DOCUMENT', 'AUDIO']:
        test_cases = TestCaseModel.get_by_modality(modality_filter)
    else:
        test_cases = TestCaseModel.get_all()
        modality_filter = 'ALL'
        
    return render_template(
        'tasks.html',
        test_cases=test_cases,
        modality_filter=modality_filter,
        active_page='tasks'
    )

@tasks_bp.route('/tasks/download/<filename>')
def download_asset(filename):
    assets_dir = BASE_DIR / "data" / "sample_assets"
    file_path = assets_dir / filename
    if not file_path.exists():
        abort(404, description=f"Asset {filename} not found.")
    return send_from_directory(assets_dir, filename, as_attachment=True)
