from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ml.predictor import predictor
import random

bp = Blueprint('student', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student':
        return "Unauthorized", 403
    return render_template('student/dashboard.html')

@bp.route('/profile')
@login_required
def profile():
    if current_user.role != 'student':
        return "Unauthorized", 403
    return render_template('student/profile.html')

@bp.route('/analytics')
@login_required
def analytics():
    if current_user.role != 'student':
        return "Unauthorized", 403
        
    # Generate some dummy data for the demonstration
    attendance = random.uniform(60, 100)
    assignments = random.randint(5, 10)
    quiz = random.uniform(50, 95)
    prev_term = random.uniform(55, 90)
    
    predicted_mark, category = predictor.predict(attendance, assignments, quiz, prev_term)
    recommendation = predictor.get_recommendations(category, predicted_mark)
    
    return render_template('student/analytics.html', 
                          attendance=attendance, 
                          predicted_mark=predicted_mark,
                          category=category,
                          recommendation=recommendation)

@bp.route('/recommendations')
@login_required
def recommendations():
    if current_user.role != 'student':
        return "Unauthorized", 403
    return render_template('student/recommendations.html')
