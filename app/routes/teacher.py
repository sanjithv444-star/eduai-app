from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Teacher, Student, Course, Enrollment, Assessment, Marks, Attendance
from app import db
from datetime import datetime, timezone

bp = Blueprint('teacher', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'teacher':
        return "Unauthorized", 403
        
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        return "Teacher profile not found", 404
        
    courses = teacher.courses_taught.all()
    
    # Get all unique students enrolled in these courses
    students = set()
    for course in courses:
        for enrollment in course.enrollments:
            students.add(enrollment.student)
            
    # Convert to list for template iteration
    students = list(students)
    
    return render_template('teacher/dashboard.html', teacher=teacher, courses=courses, students=students)

@bp.route('/add_mark', methods=['POST'])
@login_required
def add_mark():
    if current_user.role != 'teacher':
        return "Unauthorized", 403
        
    student_id = request.form.get('student_id')
    course_id = request.form.get('course_id')
    assessment_title = request.form.get('assessment_title')
    marks_obtained = request.form.get('marks_obtained')
    max_marks = request.form.get('max_marks', 100)
    feedback = request.form.get('feedback', '')
    
    if not all([student_id, course_id, assessment_title, marks_obtained]):
        flash('All required fields must be filled.', 'danger')
        return redirect(url_for('teacher.dashboard'))
        
    try:
        # Create Assessment if it doesn't exist for this specific instance
        assessment = Assessment(
            course_id=course_id,
            title=assessment_title,
            type='quiz',
            max_marks=float(max_marks)
        )
        db.session.add(assessment)
        db.session.flush() # Get ID
        
        # Add Mark
        mark = Marks(
            assessment_id=assessment.id,
            student_id=student_id,
            marks_obtained=float(marks_obtained),
            feedback=feedback
        )
        db.session.add(mark)
        db.session.commit()
        
        flash(f'Successfully added mark for {assessment_title}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error saving mark: {str(e)}', 'danger')
        
    return redirect(url_for('teacher.dashboard'))

@bp.route('/add_attendance', methods=['POST'])
@login_required
def add_attendance():
    if current_user.role != 'teacher':
        return "Unauthorized", 403
        
    student_id = request.form.get('student_id')
    course_id = request.form.get('course_id')
    status = request.form.get('status')
    
    if not all([student_id, course_id, status]):
        flash('All required fields must be filled.', 'danger')
        return redirect(url_for('teacher.dashboard'))
        
    try:
        attendance = Attendance(
            student_id=student_id,
            course_id=course_id,
            date=datetime.now(timezone.utc).date(),
            status=status
        )
        db.session.add(attendance)
        db.session.commit()
        
        flash(f'Successfully marked attendance as {status}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error saving attendance: {str(e)}', 'danger')
        
    return redirect(url_for('teacher.dashboard'))
