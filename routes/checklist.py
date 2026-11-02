"""
Multimodal Output Checklist Blueprint for Capstone 57
Interactive verification checklist for evaluating AI output reliability and safety risks.
Student: Reshma Anandhan
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import ChecklistModel, ToolModel, TestCaseModel

checklist_bp = Blueprint('checklist', __name__)

@checklist_bp.route('/checklist', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tool_name = request.form.get('tool_name', '').strip()
        task_name = request.form.get('task_name', '').strip()
        
        has_incorrect = 'has_incorrect_info' in request.form
        has_missing = 'has_missing_info' in request.form
        has_hallucinations = 'has_hallucinations' in request.form
        has_unsafe = 'has_unsafe_advice' in request.form
        has_outdated = 'has_outdated_info' in request.form
        has_source_issues = 'has_source_reliability_issues' in request.form
        has_privacy_risks = 'has_privacy_risks' in request.form
        notes = request.form.get('notes', '').strip()
        
        if not tool_name or not task_name:
            flash("Please provide the AI Tool Name and Task/Topic Name.", "danger")
            return redirect(url_for('checklist.index'))
            
        audit_id, risk, reliability = ChecklistModel.create(
            tool_name=tool_name,
            task_name=task_name,
            has_incorrect=has_incorrect,
            has_missing=has_missing,
            has_hallucinations=has_hallucinations,
            has_unsafe=has_unsafe,
            has_outdated=has_outdated,
            has_source_issues=has_source_issues,
            has_privacy_risks=has_privacy_risks,
            notes=notes
        )
        flash(f"Checklist audit saved successfully! Risk Level: {risk} ({reliability}% Reliability).", "success")
        return redirect(url_for('checklist.index'))
        
    audits = ChecklistModel.get_all()
    tools = ToolModel.get_all()
    test_cases = TestCaseModel.get_all()
    
    return render_template(
        'checklist.html',
        audits=audits,
        tools=tools,
        test_cases=test_cases,
        active_page='checklist'
    )
