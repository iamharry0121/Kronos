from flask import Flask, render_template
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import SubmitField, StringField 
from wtforms.validators import DataRequired
import secrets

class EnterTask(FlaskForm):
    task = StringField('Task', [DataRequired()])
    submit = SubmitField('Submit')

app = Flask(__name__)
foo = secrets.token_urlsafe(16) #URL in urlsafe meaning it only uses characters found in a web url
app.secret_key = foo
csrf = CSRFProtect(app)
etls = []


@app.route('/', methods=['GET', 'POST'])
def main_page():
    form = EnterTask()
    if form.validate_on_submit():
        task = form.task.data
        etls.append(task)
        return render_template('main_page.html', form=form, values=etls)

    return render_template('main_page.html', form=form)
        
if __name__ == '__main__':
    app.run(debug=True)