from app import create_app, db
from app.models import User, Student, Teacher, Course, Enrollment, Assessment, Marks, Attendance
from datetime import datetime, timedelta
import random

app = create_app()

def seed_database():
    with app.app_context():
        # Check if users already exist
        if User.query.count() > 0:
            print("Database already seeded!")
            return
            
        print("Seeding database...")
        
        # Create Admin
        admin = User(username='admin', email='admin@eduai.com', role='admin')
        admin.set_password('password123')
        db.session.add(admin)
        
        # Create Teacher
        teacher_user = User(username='teacher1', email='teacher@eduai.com', role='teacher')
        teacher_user.set_password('password123')
        db.session.add(teacher_user)
        db.session.flush() # To get the user ID
        
        teacher_profile = Teacher(user_id=teacher_user.id, department='Computer Science')
        db.session.add(teacher_profile)
        db.session.flush()
        
        # Create Student
        student_user = User(username='student1', email='student@eduai.com', role='student')
        student_user.set_password('password123')
        db.session.add(student_user)
        db.session.flush()
        
        student_profile = Student(user_id=student_user.id, department='Computer Science', batch='2026')
        db.session.add(student_profile)
        db.session.flush()

        # Create Courses
        courses_data = [
            {'code': 'CS101', 'name': 'Introduction to Programming'},
            {'code': 'CS102', 'name': 'Data Structures'},
            {'code': 'MA101', 'name': 'Calculus I'}
        ]
        courses = []
        for c in courses_data:
            course = Course(code=c['code'], name=c['name'], teacher_id=teacher_profile.id)
            db.session.add(course)
            courses.append(course)
        db.session.flush()

        # Enroll Student
        for course in courses:
            enrollment = Enrollment(student_id=student_profile.id, course_id=course.id)
            db.session.add(enrollment)
        
        # Create Assessments and Marks
        for course in courses:
            for i in range(1, 4):
                assessment = Assessment(course_id=course.id, title=f'Quiz {i}', type='quiz', max_marks=100)
                db.session.add(assessment)
                db.session.flush()
                
                # Assign marks (slightly improving over time)
                base_mark = random.uniform(60, 80)
                mark = min(100, base_mark + (i * 5) + random.uniform(-5, 5))
                marks_record = Marks(assessment_id=assessment.id, student_id=student_profile.id, marks_obtained=mark, feedback="Good effort.")
                db.session.add(marks_record)

        # Create Attendance (Last 14 days)
        today = datetime.now().date()
        for i in range(14):
            date = today - timedelta(days=i)
            # Skip weekends
            if date.weekday() >= 5:
                continue
            
            for course in courses:
                status = 'present' if random.random() > 0.15 else 'absent' # 85% attendance rate
                attendance = Attendance(student_id=student_profile.id, course_id=course.id, date=date, status=status)
                db.session.add(attendance)
        
        db.session.commit()
        print("Database seeded successfully with rich mock data!")
        print("Test Accounts:")
        print("Admin: admin@eduai.com / password123")
        print("Teacher: teacher@eduai.com / password123")
        print("Student: student@eduai.com / password123")

if __name__ == '__main__':
    seed_database()
