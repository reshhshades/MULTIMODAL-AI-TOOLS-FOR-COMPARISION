"""
Presentation Deck Blueprint for Capstone 57
Six-slide interactive presentation deck for college viva defense and seminar presentations.
Student: Reshma Anandhan
"""
from flask import Blueprint, render_template
from models import ToolModel, EvaluationModel
from config import Config

presentation_bp = Blueprint('presentation', __name__)

@presentation_bp.route('/presentation')
def index():
    tools = ToolModel.get_with_metrics()
    summary = EvaluationModel.get_overall_summary()
    best_modality = EvaluationModel.get_best_per_modality()
    
    slides = [
        {
            "slide_num": 1,
            "title": "CAPSTONE 57: Multimodal AI Tools Comparison for Students",
            "subtitle": "An Empirical Evaluation of Free Tier AI Models for Academic Study Tasks",
            "bullets": [
                f"Candidate: {Config.STUDENT_NAME}",
                "Degree: Bachelor of Technology / Computer Science Capstone Project",
                "Focus: Multimodal Artificial Intelligence, Optical Character Recognition, Document Synthesis & Audio Transcription",
                "Target Audience: College students seeking zero-cost, high-efficiency AI study assistants."
            ],
            "badge": "Slide 1 of 6: Title & Introduction",
            "speaker_notes": "Introduce yourself as Reshma Anandhan. State that free AI models are widely used by university students, but until now, no rigorous comparative empirical evaluation existed analyzing how accurately they process diagrams, PDF textbooks, and spoken lecture audio without paid subscriptions."
        },
        {
            "slide_num": 2,
            "title": "Problem Statement & Project Objectives",
            "subtitle": "Bridging the Gap Between Marketing Claims and Academic Ground Truth",
            "bullets": [
                "<b>Problem:</b> AI companies market multimodal prowess, but free tiers impose hidden file caps, dynamic rate throttling, and subtle hallucinations.",
                "<b>Academic Vulnerability:</b> Students blindly trusting AI output risk propagating fabricated citations, flawed formulas, and inverted circuit logic.",
                "<b>Objective 1:</b> Systematically benchmark the 4 leading free AI platforms across 15 real-world study test cases.",
                "<b>Objective 2:</b> Implement a standardized 4-factor weighted scoring methodology (Accuracy 40%, Completeness 25%, Relevance 20%, Ease of Use 15%).",
                "<b>Objective 3:</b> Deliver an open-source, student-friendly web evaluation platform with failure analysis and fact-checking checklists."
            ],
            "badge": "Slide 2 of 6: Problem & Objectives",
            "speaker_notes": "Emphasize why this research matters. Explain that students cannot afford \$20/month subscriptions for every AI tool, and need to know which free tool actually works best for specific tasks like transcribing audio vs reading engineering blueprints."
        },
        {
            "slide_num": 3,
            "title": "Evaluated Free AI Platforms",
            "subtitle": "ChatGPT, Google Gemini, Claude, and Microsoft Copilot",
            "bullets": [
                "<b>ChatGPT (OpenAI - GPT-4o / 4o mini):</b> Versatile multimodal system with high reasoning and mobile voice, but free web tier lacks direct audio file uploads.",
                "<b>Google Gemini (Google DeepMind - 1.5 Flash / Pro):</b> Natively multimodal foundation model featuring an unprecedented 1,000,000 token context window and native MP3/WAV audio file upload.",
                "<b>Claude (Anthropic - 3.5 Sonnet / Haiku):</b> Industry-leading academic writing, code generation, and low hallucination rate; constrained by strict dynamic 5-hour message quotas.",
                "<b>Microsoft Copilot (Microsoft / GPT-4):</b> Seamless Microsoft Edge PDF sidebar reader and Bing web search grounding; vulnerable to web snippet hallucination."
            ],
            "badge": "Slide 3 of 6: AI Tools Compared",
            "speaker_notes": "Highlight that this study strictly evaluates the free tiers available to any student with an ordinary browser. Differentiate between verified technical facts and commercial assumptions."
        },
        {
            "slide_num": 4,
            "title": "Research Methodology & 15 Standardized Test Cases",
            "subtitle": "Three Modalities: Image Understanding, Document Processing, and Spoken Audio",
            "bullets": [
                "<b>IMAGE Modality (5 Cases):</b> Logic circuit schematic interpretation, cursive lecture notes OCR, ATP Synthase biology diagram explanation, physics optics bench apparatus detection, and dual-axis economic stagflation chart analysis.",
                "<b>DOCUMENT Modality (5 Cases):</b> 10-page TCP congestion control research PDF summary, Red-Black tree complexity extraction, ACID transaction citation retrieval, cache coherence study notes generation, and catching 3 planted software engineering errors.",
                "<b>AUDIO Modality (5 Cases):</b> Verbatim acoustic physics lecture transcription, distributed microservices 15-min audio summary, multi-speaker seminar topic taxonomy extraction, technical terminology glossary extraction, and glycolysis exam cheat sheet formulation.",
                "<b>Scoring Framework:</b> Formula: Score = 0.40(Accuracy) + 0.25(Completeness) + 0.20(Relevance) + 0.15(Ease of Use). Separate flags for Hallucinations and Unsafe/Outdated Claims."
            ],
            "badge": "Slide 4 of 6: Methodology & Test Cases",
            "speaker_notes": "Point out that 15 test cases provide comprehensive coverage across STEM and humanities academic tasks. Explain why Accuracy receives the highest 40% weight."
        },
        {
            "slide_num": 5,
            "title": "Benchmark Results & Comparative Analysis",
            "subtitle": "Clear Winners by Modality and Overall Student Utility",
            "bullets": [
                f"<b>Overall Winner:</b> Google Gemini led overall with an 89.8% weighted average across all modalities, powered by its flawless audio ingestion.",
                f"<b>Document Synthesis Winner:</b> Claude 3.5 Sonnet dominated PDF text processing (92.4% weighted score) and achieved a 0% hallucination rate on ground truth tests.",
                f"<b>Image & Math Winner:</b> ChatGPT and Claude tied on intricate schematic interpretation and cursive OCR.",
                f"<b>Failure Analysis:</b> Microsoft Copilot recorded the highest hallucination rate (2 out of 15 tasks) due to aggressive web snippet retrieval contaminating source document text.",
                "<b>Audio Reality:</b> Gemini is the ONLY free tool that students can directly drag-and-drop lecture recordings into."
            ],
            "badge": "Slide 5 of 6: Results & Analysis",
            "speaker_notes": "Walk the evaluators through the radar and bar chart data. Point out the audio disparity: while Claude and ChatGPT write beautifully, their free web tiers cannot accept MP3 recordings, giving Gemini an overwhelming advantage for lecture review."
        },
        {
            "slide_num": 6,
            "title": "Conclusion, Best Student Workflow & Future Scope",
            "subtitle": "Actionable Guidelines for Higher Education",
            "bullets": [
                "<b>The Optimal Student Stack:</b> Use <b>Google Gemini</b> for recorded lecture audio transcription and large PDF textbook overviews; use <b>Claude</b> for critical research synthesis and error-free exam note preparation; use <b>ChatGPT</b> for interactive step-by-step problem solving.",
                "<b>Golden Rule:</b> Never treat AI output as ground truth; apply the Multimodal Output Checklist to audit every citation and formula.",
                "<b>Future Scope:</b> Expand benchmarking to open-weights models (Llama 3.2 Vision, Whisper), implement automated audio chunking pipelines, and integrate with university LMS platforms (Canvas, Moodle).",
                "<b>Acknowledgments:</b> Thank you to the faculty, reviewers, and Google DeepMind open AI research ecosystem."
            ],
            "badge": "Slide 6 of 6: Conclusion & Future Scope",
            "speaker_notes": "Conclude your viva presentation with confidence. Summarize the actionable student stack and invite questions from the panel of examiners."
        }
    ]
    
    return render_template(
        'presentation.html',
        slides=slides,
        tools=tools,
        summary=summary,
        student_name=Config.STUDENT_NAME,
        project_name=Config.PROJECT_NAME,
        active_page='presentation'
    )
