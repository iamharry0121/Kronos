from flask import Flask, render_template, redirect, url_for, jsonify, flash
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import SubmitField, StringField , PasswordField
from wtforms.validators import DataRequired, Email
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)
import database_manager as db_mgr

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testingtesting6767'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///tasks.db'

csrf = CSRFProtect(app)
db_mgr.init_db(app)

#flask login setup + flask forms
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db_mgr.get_user_by_id(user_id)

class EnterTask(FlaskForm):
    task = StringField('Task', [DataRequired()])
    submit = SubmitField('Submit')

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))

    form = SignupForm()
    if form.validate_on_submit():
        existing_user = db_mgr.get_user_by_email(form.email.data)
        if existing_user:
            flash('Email already exists.')
            return redirect(url_for('signup'))

        new_user = db_mgr.create_user(form.email.data, form.password.data)

        login_user(new_user)
        return redirect(url_for('main_page'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db_mgr.get_user_by_email(form.email.data)

        if user is None or not user.check_password(form.password.data):
            flash('Incorrect email or password')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('main_page'))

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('landing_page'))

@app.route('/home', methods=['GET', 'POST'])
@login_required
def main_page():
    form = EnterTask()
    if form.validate_on_submit():
        db_mgr.add_task(form.task.data, current_user.id)
        return redirect(url_for('main_page'))

    tasks = db_mgr.get_all_tasks(current_user.id)
    return render_template('main_page.html', form=form, values=tasks)

@app.route('/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    is_completed = db_mgr.toggle_task(task_id, current_user.id)
    return jsonify({'success':True, 'completed':is_completed})

@app.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    db_mgr.delete_task_by_id(task_id, current_user.id)
    return jsonify({'success':True})

if __name__ == '__main__':
    app.run(debug=True)