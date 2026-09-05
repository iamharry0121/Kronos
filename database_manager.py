from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    #one row is one account and usermixin gives all auth based functions so dont write auth things

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)

    def set_password(self, plain_txt_pwd):
        self.password_hash = generate_password_hash(plain_txt_pwd)

    def check_password(self, plain_txt_pwd):
        return check_password_hash(self. password_hash, plain_txt_pwd)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

#user related helpers
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_by_id(user_id):
    return User.query.get(int(user_id))

def create_user(email, plain_txt_pwd):
    new_user = User(email=email)
    new_user.set_password(plain_txt_pwd)
    db.session.add(new_user)
    db.session.commit()
    return new_user
#end of user related helpers

#task related helpers
def add_task(task_text, user_id):
    new_task = Task(task=task_text, user_id=user_id)
    db.session.add(new_task)
    db.session.commit()

def get_all_tasks(user_id):
    return Task.query.filter_by(user_id=user_id).all()

def delete_task_by_id(task_id, user_id):
    task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
    db.session.delete(task)
    db.session.commit()

def toggle_task(task_id, user_id):
    task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
    task.completed = not task.completed
    db.session.commit()
    return task.completed
#end of task related helpers

