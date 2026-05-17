from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint('teacher', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'teacher':
        return "Unauthorized", 403
    return render_template('teacher/dashboard.html')
