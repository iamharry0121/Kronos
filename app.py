from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import SubmitField, StringField 
from wtforms.validators import DataRequired
import database_manager as db_mgr

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testingtesting6767'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///tasks.db'

db_mgr.init_db(app)

class EnterTask(FlaskForm):
    task = StringField('Task', [DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def main_page():
    form = EnterTask()
    if form.validate_on_submit():
        db_mgr.add_task(form.task.data)
        return redirect(url_for('main_page'))

    tasks = db_mgr.get_all_tasks()
    return render_template('main_page.html', form=form, values=tasks)

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    db_mgr.delete_task_by_id(task_id)
    return redirect(url_for('main_page'))

if __name__ == '__main__':
    app.run(debug=True)
