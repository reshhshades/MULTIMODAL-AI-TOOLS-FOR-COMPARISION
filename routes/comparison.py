"""
Comparison Dashboard Blueprint for Capstone 57
Comprehensive comparative analysis of ChatGPT, Google Gemini, Claude, and Copilot.
Student: Reshma Anandhan
"""
from flask import Blueprint, render_template, request
from models import ToolModel, EvaluationModel, TestCaseModel

comparison_bp = Blueprint('comparison', __name__)

@comparison_bp.route('/comparison')
def index():
    selected_modality = request.args.get('modality', 'ALL').upper()
    
    tools = ToolModel.get_with_metrics()
    best_per_modality = EvaluationModel.get_best_per_modality()
    category_matrix = EvaluationModel.get_category_modality_matrix()
    
    # Filter category matrix if specific modality is chosen
    if selected_modality in ['IMAGE', 'DOCUMENT', 'AUDIO']:
        filtered_matrix = [row for row in category_matrix if row['modality'] == selected_modality]
    else:
        filtered_matrix = category_matrix
        selected_modality = 'ALL'
        
    # Strengths and weaknesses knowledge matrix for college students
    strengths_weaknesses = {
        "ChatGPT": {
            "strengths": [
                "Superior natural language clarity and pedagogical explanations.",
                "Robust OCR and mathematical equation parsing in images.",
                "Highly responsive desktop and mobile interface.",
                "Clean LaTeX formatting for student study guides."
            ],
            "weaknesses": [
                "Free web tier lacks native direct audio (.mp3/.wav) upload.",
                "Frequent dynamic rate limits on GPT-4o, downgrading to mini.",
                "Occasional overconfidence when interpreting ambiguous diagrams."
            ],
            "student_verdict": "Best overall for conceptual explanation, math problem solving, and diagram deconstruction."
        },
        "Google Gemini": {
            "strengths": [
                "Only major free tool offering direct native audio file upload (.mp3, .wav).",
                "Expansive 1,000,000 token context window processes 100+ page PDFs effortlessly.",
                "Superior multimodal temporal and spatial reasoning.",
                "Generous rate limits on Gemini 1.5 Flash."
            ],
            "weaknesses": [
                "Occasionally hallucinates subtle timestamps on audio files.",
                "Formatting can be less strictly structured compared to Claude.",
                "Requires careful prompt constraints to avoid unsolicited extra commentary."
            ],
            "student_verdict": "Undisputed champion for lecture audio transcription, large PDF summarization, and high-speed workflow."
        },
        "Claude": {
            "strengths": [
                "Lowest hallucination rate among all tested models in document tasks.",
                "Exceptional depth in academic summarization and fact-checking.",
                "Impeccable adherence to negative constraints ('do not assume...').",
                "High precision in logic circuit analysis and code synthesis."
            ],
            "weaknesses": [
                "No native audio file upload on free web tier (claude.ai).",
                "Most restrictive free tier message limit (resets every 5 hours).",
                "Refuses to answer if documents trigger overzealous safety filters."
            ],
            "student_verdict": "Highest reliability and academic rigor for research paper synthesis and critical fact-checking."
        },
        "Microsoft Copilot": {
            "strengths": [
                "Native integration into Microsoft Edge browser reads any PDF without upload.",
                "Real-time web search grounding brings up-to-date context and citations.",
                "Free to use with standard Microsoft account (no subscription required).",
                "Good printed text recognition."
            ],
            "weaknesses": [
                "Web search grounding occasionally pulls irrelevant blogs into PDF answers.",
                "No direct audio file upload (only microphone live dictation).",
                "Lower accuracy on complex multi-variable physics and economics charts."
            ],
            "student_verdict": "Convenient student assistant for quick PDF reading in Edge and web-grounded fact lookup."
        }
    }
    
    return render_template(
        'comparison.html',
        tools=tools,
        best_per_modality=best_per_modality,
        category_matrix=filtered_matrix,
        selected_modality=selected_modality,
        strengths_weaknesses=strengths_weaknesses,
        active_page='comparison'
    )
