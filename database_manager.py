from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def add_task(task_text):
    new_task = Task(task=task_text)
    db.session.add(new_task)
    db.session.commit()

def get_all_tasks():
    return Task.query.all() 

def delete_task_by_id(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()

def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return task.completed

