"""
Main Application Entry Point for Capstone 57
CAPSTONE 57 – MULTIMODAL AI TOOLS COMPARISON FOR STUDENTS
Author / Student: Reshma Anandhan
"""
import os
from flask import Flask, render_template
from config import Config
from database import init_db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)
    os.makedirs(os.path.dirname(app.config['DATABASE_PATH']), exist_ok=True)
    
    # Initialize DB schema & seed data if necessary
    with app.app_context():
        if not os.path.exists(app.config['DATABASE_PATH']):
            init_db(force_reseed=True)
        else:
            init_db(force_reseed=False)
            
    # Register Blueprints
    from routes.dashboard import dashboard_bp
    from routes.tools import tools_bp
    from routes.tasks import tasks_bp
    from routes.evaluations import evaluations_bp
    from routes.comparison import comparison_bp
    from routes.reports import reports_bp
    from routes.checklist import checklist_bp
    from routes.quiz import quiz_bp
    from routes.automation import automation_bp
    from routes.before_after import before_after_bp
    from routes.presentation import presentation_bp
    from routes.prompts import prompts_bp
    from routes.api import api_bp
    
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(tools_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(evaluations_bp)
    app.register_blueprint(comparison_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(checklist_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(automation_bp)
    app.register_blueprint(before_after_bp)
    app.register_blueprint(presentation_bp)
    app.register_blueprint(prompts_bp)
    app.register_blueprint(api_bp)
    
    # Context Processor for Global Template Variables
    @app.context_processor
    def inject_global_data():
        return {
            'PROJECT_TITLE': Config.PROJECT_NAME,
            'STUDENT_NAME': Config.STUDENT_NAME,
            'VERSION': Config.VERSION,
            'CURRENT_YEAR': 2026
        }

    # Custom Jinja Filters
    @app.template_filter('badge_class')
    def badge_class_filter(val):
        if not val:
            return 'secondary'
        v = str(val).upper()
        if v in ['IMAGE', 'LOW', 'BASIC', 'EASY', 'VERIFIED']:
            return 'info'
        elif v in ['DOCUMENT', 'MODERATE', 'INTERMEDIATE', 'MEDIUM']:
            return 'warning'
        elif v in ['AUDIO', 'HIGH', 'ADVANCED', 'HARD']:
            return 'danger'
        elif v in ['CRITICAL']:
            return 'danger'
        return 'primary'

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html', error=str(e)), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html', error=str(e)), 500

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"================================================================")
    print(f" CAPSTONE 57: MULTIMODAL AI TOOLS COMPARISON FOR STUDENTS")
    print(f" Lead Researcher: {Config.STUDENT_NAME}")
    print(f" Server running at: http://127.0.0.1:{port}")
    print(f"================================================================")
    app.run(host='0.0.0.0', port=port, debug=True)
