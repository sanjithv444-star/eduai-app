from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('main/index.html')

@bp.route('/seed-db-secret')
def seed_db_secret():
    # Only for demonstration/setup purposes.
    from seed_db import seed_database
    import sys
    try:
        from app import db
        db.drop_all()
        db.create_all()
        seed_database()
        return "Database successfully cleared and re-seeded with mock data!"
    except Exception as e:
        return f"Error: {str(e)}", 500
