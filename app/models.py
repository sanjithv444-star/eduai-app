from datetime import datetime, timezone, date as date_type
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20)) # 'admin', 'teacher', 'student'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    department = db.Column(db.String(100))
    batch = db.Column(db.String(20))
    
    user = db.relationship('User', backref=db.backref('student_profile', uselist=False))
    enrollments = db.relationship('Enrollment', backref='student', lazy='dynamic')
    attendance_records = db.relationship('Attendance', backref='student', lazy='dynamic')
    marks_records = db.relationship('Marks', backref='student', lazy='dynamic')
    predictions = db.relationship('Prediction', backref='student', lazy='dynamic')

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    department = db.Column(db.String(100))
    
    user = db.relationship('User', backref=db.backref('teacher_profile', uselist=False))
    courses_taught = db.relationship('Course', backref='teacher', lazy='dynamic')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(100))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    
    enrollments = db.relationship('Enrollment', backref='course', lazy='dynamic')
    assessments = db.relationship('Assessment', backref='course', lazy='dynamic')
    materials = db.relationship('Material', backref='course', lazy='dynamic')

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    enrolled_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date())
    status = db.Column(db.String(20)) # 'present', 'absent', 'late'

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    title = db.Column(db.String(100))
    type = db.Column(db.String(50)) # 'assignment', 'quiz', 'exam'
    max_marks = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    marks = db.relationship('Marks', backref='assessment', lazy='dynamic')

class Marks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    marks_obtained = db.Column(db.Float)
    feedback = db.Column(db.Text)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    date_predicted = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    predicted_score = db.Column(db.Float)
    performance_category = db.Column(db.String(50)) # 'Excellent', 'Good', 'Needs Improvement'
    recommended_actions = db.Column(db.Text) # JSON string or plain text

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    title = db.Column(db.String(100))
    link = db.Column(db.String(255))
    type = db.Column(db.String(50)) # 'video', 'document', 'quiz'
    difficulty_level = db.Column(db.String(20)) # 'beginner', 'intermediate', 'advanced'
