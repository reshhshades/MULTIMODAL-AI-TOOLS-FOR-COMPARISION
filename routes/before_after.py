"""
Before and After Analysis Blueprint for Capstone 57
Displays pre-audit vs post-audit evaluation scores, fact-checked corrections, identified errors, and delta improvements.
Student: Reshma Anandhan
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import BeforeAfterModel, ToolModel, TestCaseModel
from database import get_db_connection

before_after_bp = Blueprint('before_after', __name__)

@before_after_bp.route('/before-after')
def index():
    records = BeforeAfterModel.get_all()
    tools = ToolModel.get_all()
    test_cases = TestCaseModel.get_all()
    
    # Calculate summary metrics
    total_audited = len(records)
    avg_delta = round(sum(r['score_delta'] for r in records) / total_audited, 2) if total_audited > 0 else 0
    positive_adjustments = sum(1 for r in records if r['score_delta'] > 0)
    penalties_applied = sum(1 for r in records if r['score_delta'] < 0)
    
    return render_template(
        'before_after.html',
        records=records,
        tools=tools,
        test_cases=test_cases,
        total_audited=total_audited,
        avg_delta=avg_delta,
        positive_adjustments=positive_adjustments,
        penalties_applied=penalties_applied,
        active_page='before_after'
    )

@before_after_bp.route('/before-after/new', methods=['POST'])
def create():
    try:
        tool_id = int(request.form.get('tool_id'))
        test_case_id = int(request.form.get('test_case_id'))
        initial_score = float(request.form.get('initial_score'))
        verified_score = float(request.form.get('verified_score'))
        errors_identified = request.form.get('errors_identified', '').strip()
        fact_check_notes = request.form.get('fact_check_notes', '').strip()
        improvement_strategy = request.form.get('improvement_strategy', '').strip()
        
        score_delta = round(verified_score - initial_score, 2)
        
        conn = get_db_connection()
        conn.execute("""
        INSERT INTO before_after_records
        (tool_id, test_case_id, initial_score, verified_score, score_delta, errors_identified, fact_check_notes, improvement_strategy, verification_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Verified')
        """, (tool_id, test_case_id, initial_score, verified_score, score_delta, errors_identified, fact_check_notes, improvement_strategy))
        conn.commit()
        conn.close()
        
        flash("New Before & After audit verification record added successfully!", "success")
    except Exception as e:
        flash(f"Error adding verification record: {str(e)}", "danger")
        
    return redirect(url_for('before_after.index'))
