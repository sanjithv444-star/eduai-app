from app import create_app, db
from app.models import User, Student, Teacher, Course

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Student': Student, 'Teacher': Teacher, 'Course': Course}

if __name__ == '__main__':
    app.run(debug=True)
