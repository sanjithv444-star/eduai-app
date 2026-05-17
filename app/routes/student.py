from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ml.predictor import predictor
from app.models import Student, Course, Enrollment, Assessment, Marks, Attendance
from app import db
from ml.predictor import predictor
import random

bp = Blueprint('student', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student':
        return "Unauthorized", 403
        
    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student:
        return "Student profile not found", 404
        
    # Get Enrollments
    enrollments = student.enrollments.all()
    courses = [e.course for e in enrollments]
    
    # Get Attendance
    total_classes = student.attendance_records.count()
    present_classes = student.attendance_records.filter_by(status='present').count()
    attendance_pct = (present_classes / total_classes * 100) if total_classes > 0 else 0
    
    # Get Recent Marks
    recent_marks = student.marks_records.order_by(Marks.id.desc()).limit(5).all()
    
    # Calculate Average
    total_marks = sum([m.marks_obtained for m in student.marks_records.all()])
    num_marks = student.marks_records.count()
    avg_mark = (total_marks / num_marks) if num_marks > 0 else 0
    
    # Dummy data for AI prediction to keep it fast
    predicted_mark, category = predictor.predict(attendance_pct, len(enrollments), avg_mark, avg_mark)

    return render_template('student/dashboard.html', 
                           courses=courses,
                           attendance_pct=attendance_pct,
                           recent_marks=recent_marks,
                           avg_mark=avg_mark,
                           predicted_mark=predicted_mark,
                           category=category)

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
        
    student = Student.query.filter_by(user_id=current_user.id).first()
    
    # Calculate real data
    total_classes = student.attendance_records.count()
    present_classes = student.attendance_records.filter_by(status='present').count()
    attendance = (present_classes / total_classes * 100) if total_classes > 0 else 85.0
    
    assignments = student.marks_records.count()
    
    total_marks = sum([m.marks_obtained for m in student.marks_records.all()])
    avg_mark = (total_marks / assignments) if assignments > 0 else 75.0
    
    predicted_mark, category = predictor.predict(attendance, assignments, avg_mark, avg_mark)
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
