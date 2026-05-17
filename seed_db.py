from app import create_app, db
from app.models import User, Student, Teacher

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
        
        # Create Student
        student_user = User(username='student1', email='student@eduai.com', role='student')
        student_user.set_password('password123')
        db.session.add(student_user)
        db.session.flush()
        
        student_profile = Student(user_id=student_user.id, department='Computer Science', batch='2026')
        db.session.add(student_profile)
        
        db.session.commit()
        print("Database seeded successfully!")
        print("Test Accounts:")
        print("Admin: admin@eduai.com / password123")
        print("Teacher: teacher@eduai.com / password123")
        print("Student: student@eduai.com / password123")

if __name__ == '__main__':
    seed_database()
