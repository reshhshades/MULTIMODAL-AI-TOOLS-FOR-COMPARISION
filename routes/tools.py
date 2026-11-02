"""
AI Tools Information Blueprint for Capstone 57
Displays detailed technical profiles, multimodal capabilities, free tier limits, and verified dates.
Student: Reshma Anandhan
"""
from flask import Blueprint, render_template
from models import ToolModel

tools_bp = Blueprint('tools', __name__)

@tools_bp.route('/tools')
def index():
    tools = ToolModel.get_with_metrics()
    return render_template(
        'tools.html',
        tools=tools,
        active_page='tools'
    )
