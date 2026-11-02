"""
Quiz Module Blueprint for Capstone 57
10-question multiple-choice quiz testing student knowledge on multimodal AI evaluation.
Student: Reshma Anandhan
"""
from flask import Blueprint, render_template, request
from models import QuizModel

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/quiz', methods=['GET', 'POST'])
def index():
    questions = QuizModel.get_all()
    results = None
    
    if request.method == 'POST':
        user_answers = {}
        for q in questions:
            field_name = f"question_{q['id']}"
            user_answers[str(q['id'])] = request.form.get(field_name, "")
            
        results = QuizModel.grade(user_answers)
        
    return render_template(
        'quiz.html',
        questions=questions,
        results=results,
        active_page='quiz'
    )
