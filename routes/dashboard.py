"""
Dashboard Blueprint for Capstone 57
Home Dashboard displaying overall metrics, quick insights, charts, and summary statistics.
Student: Reshma Anandhan
"""
from flask import Blueprint, render_template
from models import EvaluationModel, ToolModel, TestCaseModel

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
def index():
    summary = EvaluationModel.get_overall_summary()
    tools = ToolModel.get_with_metrics()
    best_modality = EvaluationModel.get_best_per_modality()
    total_test_cases = len(TestCaseModel.get_all())
    
    return render_template(
        'dashboard.html',
        summary=summary,
        tools=tools,
        best_modality=best_modality,
        total_test_cases=total_test_cases,
        active_page='dashboard'
    )
