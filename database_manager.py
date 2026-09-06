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

    # the date and time this task is due. Required (nullable=False) since
    # every task needs one for the reminder-email feature to work.
    due_date = db.Column(db.DateTime, nullable=False)

    # tracks whether we've already sent the reminder email for this task,
    # so the scheduler (added later) doesn't email the user twice.
    reminder_sent = db.Column(db.Boolean, default=False)

    # how many minutes before due_date the reminder email should go out.
    # Stored as minutes so the scheduler math is just simple subtraction:
    # remind_at = due_date - timedelta(minutes=remind_minutes_before)
    remind_minutes_before = db.Column(db.Integer, nullable=False, default=60)

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
def add_task(task_text, due_date, remind_minutes_before, user_id):
    new_task = Task(
        task=task_text,
        due_date=due_date,
        remind_minutes_before=remind_minutes_before,
        user_id=user_id
    )
    db.session.add(new_task)
    db.session.commit()

def get_all_tasks(user_id):
    # Ordering by due_date means the soonest-due task always shows first.
    return Task.query.filter_by(user_id=user_id).order_by(Task.due_date.asc()).all()

def get_tasks_needing_reminders(now):
    from datetime import timedelta
    candidates = Task.query.filter_by(reminder_sent=False, completed=False).all()
    due_for_reminder = []
    for task in candidates:
        remind_at = task.due_date - timedelta(minutes=task.remind_minutes_before)
        if remind_at <= now:
            due_for_reminder.append(task)
    return due_for_reminder

def mark_reminder_sent(task_id):
    task = Task.query.get(task_id)
    if task:
        task.reminder_sent = True
        db.session.commit()

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