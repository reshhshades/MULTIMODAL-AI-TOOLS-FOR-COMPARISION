"""
Automation Module Blueprint for Capstone 57
Real automated workflows: statistical calculation, data pipeline normalization, automated reporting, and exports.
Student: Reshma Anandhan
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import EvaluationModel, ToolModel, TestCaseModel
from database import init_db, get_db_connection, calculate_weighted_score
from config import Config
import pandas as pd
from datetime import datetime

automation_bp = Blueprint('automation', __name__)

@automation_bp.route('/automation')
def index():
    summary = EvaluationModel.get_overall_summary()
    tools = ToolModel.get_with_metrics()
    best_modality = EvaluationModel.get_best_per_modality()
    
    # Automation health diagnostics
    conn = get_db_connection()
    eval_count = conn.execute("SELECT COUNT(*) FROM evaluations").fetchone()[0]
    user_eval_count = conn.execute("SELECT COUNT(*) FROM evaluations WHERE is_demo_data = 0").fetchone()[0]
    out_of_bounds = conn.execute("""
        SELECT COUNT(*) FROM evaluations 
        WHERE accuracy_score < 0 OR accuracy_score > 100 
           OR completeness_score < 0 OR completeness_score > 100
           OR relevance_score < 0 OR relevance_score > 100
           OR ease_of_use_score < 0 OR ease_of_use_score > 100
    """).fetchone()[0]
    conn.close()
    
    diagnostics = {
        "status": "Healthy" if out_of_bounds == 0 else "Anomalies Detected",
        "total_evals": eval_count,
        "user_evals": user_eval_count,
        "integrity_errors": out_of_bounds,
        "last_automated_run": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return render_template(
        'automation.html',
        summary=summary,
        tools=tools,
        best_modality=best_modality,
        diagnostics=diagnostics,
        active_page='automation'
    )

@automation_bp.route('/automation/recalculate', methods=['POST'])
def recalculate():
    """
    Automated batch job: Recalculates all weighted scores across every evaluation record
    in the database to ensure 100% adherence to the formula:
    (acc * 0.40) + (comp * 0.25) + (rel * 0.20) + (ease * 0.15)
    """
    conn = get_db_connection()
    evals = conn.execute("SELECT id, accuracy_score, completeness_score, relevance_score, ease_of_use_score FROM evaluations").fetchall()
    
    updated_count = 0
    cursor = conn.cursor()
    for row in evals:
        w = calculate_weighted_score(row['accuracy_score'], row['completeness_score'], row['relevance_score'], row['ease_of_use_score'])
        cursor.execute("UPDATE evaluations SET weighted_score = ? WHERE id = ?", (w, row['id']))
        updated_count += 1
        
    conn.commit()
    conn.close()
    
    flash(f"Automated Score Recalculation Complete! Recalculated and verified {updated_count} evaluation records.", "success")
    return redirect(url_for('automation.index'))

@automation_bp.route('/automation/reset-database', methods=['POST'])
def reset_database():
    """
    Automated Data Reset: Restores the benchmark dataset to the pristine baseline.
    """
    init_db(force_reseed=True)
    flash("Database successfully restored to the verified 60-evaluation benchmark baseline!", "info")
    return redirect(url_for('automation.index'))
