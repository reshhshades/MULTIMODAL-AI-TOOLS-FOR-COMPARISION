"""
Evaluation System Blueprint for Capstone 57
Allows students to record, edit, and evaluate multimodal AI outputs using a 0-100 weighted scoring method.
Student: Reshma Anandhan
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import EvaluationModel, ToolModel, TestCaseModel
from database import calculate_weighted_score

evaluations_bp = Blueprint('evaluations', __name__)

@evaluations_bp.route('/evaluations')
def index():
    tool_id = request.args.get('tool_id', type=int)
    modality = request.args.get('modality', '')
    data_type = request.args.get('data_type', '') # 'demo', 'user', or empty for all
    
    is_demo = None
    if data_type == 'demo':
        is_demo = True
    elif data_type == 'user':
        is_demo = False
        
    evaluations = EvaluationModel.get_all(tool_id=tool_id, modality=modality, is_demo=is_demo)
    tools = ToolModel.get_all()
    
    return render_template(
        'evaluations_list.html',
        evaluations=evaluations,
        tools=tools,
        selected_tool_id=tool_id,
        selected_modality=modality,
        selected_data_type=data_type,
        active_page='evaluations'
    )

@evaluations_bp.route('/evaluate/new', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            tool_id = int(request.form.get('tool_id'))
            test_case_id = int(request.form.get('test_case_id'))
            evaluator_name = request.form.get('evaluator_name', 'Reshma Anandhan').strip()
            response_text = request.form.get('response_text', '').strip()
            
            # Scores (0 - 100 validation)
            accuracy = float(request.form.get('accuracy_score', 0))
            completeness = float(request.form.get('completeness_score', 0))
            relevance = float(request.form.get('relevance_score', 0))
            ease_of_use = float(request.form.get('ease_of_use_score', 0))
            
            for name, val in [('Accuracy', accuracy), ('Completeness', completeness), ('Relevance', relevance), ('Ease of use', ease_of_use)]:
                if not (0 <= val <= 100):
                    flash(f"Score for {name} must be between 0 and 100.", "danger")
                    return redirect(request.url)

            hallucination_detected = 'hallucination_detected' in request.form
            hallucination_details = request.form.get('hallucination_details', '').strip()
            
            unsafe_outdated_detected = 'unsafe_outdated_detected' in request.form
            unsafe_outdated_details = request.form.get('unsafe_outdated_details', '').strip()
            
            student_notes = request.form.get('student_notes', '').strip()
            
            # User evaluations are labeled as actual live data (is_demo_data = 0)
            eval_id = EvaluationModel.create(
                tool_id=tool_id,
                test_case_id=test_case_id,
                evaluator_name=evaluator_name or "Reshma Anandhan",
                response_text=response_text,
                accuracy=accuracy,
                completeness=completeness,
                relevance=relevance,
                ease_of_use=ease_of_use,
                hallucination_detected=hallucination_detected,
                hallucination_details=hallucination_details,
                unsafe_outdated_detected=unsafe_outdated_detected,
                unsafe_outdated_details=unsafe_outdated_details,
                student_notes=student_notes,
                is_demo_data=0
            )
            
            flash("Evaluation recorded successfully! Actual student experiment data saved.", "success")
            return redirect(url_for('evaluations.index'))
            
        except ValueError as e:
            flash(f"Invalid input: Please enter valid numerical scores between 0 and 100.", "danger")
            return redirect(request.url)
        except Exception as e:
            flash(f"Error saving evaluation: {str(e)}", "danger")
            return redirect(request.url)
            
    # GET request
    tools = ToolModel.get_all()
    test_cases = TestCaseModel.get_all()
    preselect_tc = request.args.get('tc_id', type=int)
    preselect_tool = request.args.get('tool_id', type=int)
    
    return render_template(
        'evaluate.html',
        tools=tools,
        test_cases=test_cases,
        preselect_tc=preselect_tc,
        preselect_tool=preselect_tool,
        is_edit=False,
        active_page='evaluate'
    )

@evaluations_bp.route('/evaluate/edit/<int:eval_id>', methods=['GET', 'POST'])
def edit(eval_id):
    eval_item = EvaluationModel.get_by_id(eval_id)
    if not eval_item:
        flash("Evaluation not found.", "danger")
        return redirect(url_for('evaluations.index'))
        
    if request.method == 'POST':
        try:
            accuracy = float(request.form.get('accuracy_score', 0))
            completeness = float(request.form.get('completeness_score', 0))
            relevance = float(request.form.get('relevance_score', 0))
            ease_of_use = float(request.form.get('ease_of_use_score', 0))
            
            for name, val in [('Accuracy', accuracy), ('Completeness', completeness), ('Relevance', relevance), ('Ease of use', ease_of_use)]:
                if not (0 <= val <= 100):
                    flash(f"Score for {name} must be between 0 and 100.", "danger")
                    return redirect(request.url)

            response_text = request.form.get('response_text', '').strip()
            hallucination_detected = 'hallucination_detected' in request.form
            hallucination_details = request.form.get('hallucination_details', '').strip()
            
            unsafe_outdated_detected = 'unsafe_outdated_detected' in request.form
            unsafe_outdated_details = request.form.get('unsafe_outdated_details', '').strip()
            
            student_notes = request.form.get('student_notes', '').strip()
            
            EvaluationModel.update(
                eval_id=eval_id,
                accuracy=accuracy,
                completeness=completeness,
                relevance=relevance,
                ease_of_use=ease_of_use,
                response_text=response_text,
                hallucination_detected=hallucination_detected,
                hallucination_details=hallucination_details,
                unsafe_outdated_detected=unsafe_outdated_detected,
                unsafe_outdated_details=unsafe_outdated_details,
                student_notes=student_notes
            )
            flash("Evaluation updated successfully!", "success")
            return redirect(url_for('evaluations.index'))
            
        except ValueError:
            flash("Please enter valid numerical scores between 0 and 100.", "danger")
            return redirect(request.url)
            
    tools = ToolModel.get_all()
    test_cases = TestCaseModel.get_all()
    return render_template(
        'evaluate.html',
        eval_item=eval_item,
        tools=tools,
        test_cases=test_cases,
        is_edit=True,
        active_page='evaluations'
    )

@evaluations_bp.route('/evaluate/delete/<int:eval_id>', methods=['POST'])
def delete(eval_id):
    EvaluationModel.delete(eval_id)
    flash("Evaluation deleted successfully.", "info")
    return redirect(url_for('evaluations.index'))
