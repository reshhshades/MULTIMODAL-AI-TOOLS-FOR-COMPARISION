"""
Prompt Library Blueprint for Capstone 57
Curated repository of reusable multimodal prompts for image understanding, PDF summarization, and audio analysis.
Student: Reshma Anandhan
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import PromptLibraryModel
from database import get_db_connection

prompts_bp = Blueprint('prompts', __name__)

@prompts_bp.route('/prompts')
def index():
    category = request.args.get('category', '').upper()
    if category in ['IMAGE', 'DOCUMENT', 'AUDIO']:
        prompts = PromptLibraryModel.get_all(category)
    else:
        prompts = PromptLibraryModel.get_all()
        category = 'ALL'
        
    return render_template(
        'prompts.html',
        prompts=prompts,
        selected_category=category,
        active_page='prompts'
    )

@prompts_bp.route('/prompts/new', methods=['POST'])
def create():
    try:
        category = request.form.get('category', 'IMAGE').upper()
        title = request.form.get('title', '').strip()
        prompt_text = request.form.get('prompt_text', '').strip()
        target_outcome = request.form.get('target_outcome', '').strip()
        recommended_tool = request.form.get('recommended_tool', 'Any').strip()
        difficulty = request.form.get('difficulty', 'Intermediate').strip()
        
        if not title or not prompt_text:
            flash("Title and Prompt text are required.", "danger")
            return redirect(url_for('prompts.index'))
            
        conn = get_db_connection()
        conn.execute("""
        INSERT INTO prompt_library
        (category, title, prompt_text, target_outcome, recommended_tool, difficulty)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (category, title, prompt_text, target_outcome, recommended_tool, difficulty))
        conn.commit()
        conn.close()
        
        flash("New prompt added to the library!", "success")
    except Exception as e:
        flash(f"Error adding prompt: {str(e)}", "danger")
        
    return redirect(url_for('prompts.index'))
