"""
REST API Blueprint for Capstone 57
JSON endpoints for dynamic Chart.js visualizations, real-time score calculation, and stats.
Student: Reshma Anandhan
"""
from flask import Blueprint, jsonify, request
from models import ToolModel, EvaluationModel, TestCaseModel
from database import calculate_weighted_score

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/chart-data')
def chart_data():
    tools = ToolModel.get_with_metrics()
    category_matrix = EvaluationModel.get_category_modality_matrix()
    
    # 1. Bar Chart Data (Overall Weighted & Accuracy per Tool)
    tool_names = [t['name'] for t in tools]
    weighted_scores = [t['avg_weighted_score'] for t in tools]
    accuracy_scores = [t['avg_accuracy'] for t in tools]
    
    # 2. Modality Breakdown
    # Group by tool and modality
    modality_breakdown = {}
    for row in category_matrix:
        tool = row['tool_name']
        mod = row['modality']
        if tool not in modality_breakdown:
            modality_breakdown[tool] = {'IMAGE': 0, 'DOCUMENT': 0, 'AUDIO': 0}
        modality_breakdown[tool][mod] = row['avg_weighted']
        
    # 3. Radar Chart Data (Accuracy, Completeness, Relevance, Ease of Use, Low-Hallucination)
    radar_datasets = []
    colors_map = {
        'ChatGPT': {'border': '#10b981', 'bg': 'rgba(16, 185, 129, 0.2)'},
        'Google Gemini': {'border': '#06b6d4', 'bg': 'rgba(6, 182, 212, 0.2)'},
        'Claude': {'border': '#f59e0b', 'bg': 'rgba(245, 158, 11, 0.2)'},
        'Microsoft Copilot': {'border': '#3b82f6', 'bg': 'rgba(59, 130, 246, 0.2)'}
    }
    
    for t in tools:
        tname = t['name']
        c = colors_map.get(tname, {'border': '#94a3b8', 'bg': 'rgba(148, 163, 184, 0.2)'})
        # Calculate a low-hallucination score (100 - (hallucinations * 20))
        halluc_penalty = max(0, 100 - ((t['total_hallucinations'] or 0) * 20))
        radar_datasets.append({
            'label': tname,
            'data': [
                t['avg_accuracy'] or 0,
                t['avg_completeness'] or 0,
                t['avg_relevance'] or 0,
                t['avg_ease_of_use'] or 0,
                halluc_penalty
            ],
            'borderColor': c['border'],
            'backgroundColor': c['bg'],
            'pointBackgroundColor': c['border'],
            'pointBorderColor': '#fff'
        })
        
    # 4. Failure breakdown
    failure_data = {
        'labels': tool_names,
        'hallucinations': [t['total_hallucinations'] or 0 for t in tools],
        'unsafe_outdated': [t['total_unsafe_outdated'] or 0 for t in tools]
    }
    
    return jsonify({
        'tools': tool_names,
        'weighted_scores': weighted_scores,
        'accuracy_scores': accuracy_scores,
        'modality_breakdown': modality_breakdown,
        'radar_labels': ['Accuracy (40%)', 'Completeness (25%)', 'Relevance (20%)', 'Ease of Use (15%)', 'Truthfulness (Low Hallucination)'],
        'radar_datasets': radar_datasets,
        'failure_data': failure_data
    })

@api_bp.route('/api/calculate-score', methods=['POST'])
def calculate_score_api():
    data = request.get_json() or {}
    try:
        acc = float(data.get('accuracy', 0))
        comp = float(data.get('completeness', 0))
        rel = float(data.get('relevance', 0))
        ease = float(data.get('ease_of_use', 0))
        
        weighted = calculate_weighted_score(acc, comp, rel, ease)
        return jsonify({
            'success': True,
            'weighted_score': weighted,
            'formula': f"({acc}*0.40) + ({comp}*0.25) + ({rel}*0.20) + ({ease}*0.15) = {weighted}"
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
