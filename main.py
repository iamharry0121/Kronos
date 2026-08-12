from flask import Flask, render_template, request
from markupsafe import Markup

app = Flask(__name__)
tsk_ls = []

@app.template_filter('nl2br')
def nl2br_filter(s):
    return Markup(s.replace('\n', '<br>'))

@app.route('/', methods=['GET', 'POST'])
def main_page():
    nls = []
    if request.method == 'POST':
        ui = request.form.get('task')
        tsk_ls.append(ui)
        for i,v in enumerate(tsk_ls):
            ni = i+1
            nls.append(f'{ni}. {v}')
        print(nls)
        return render_template('main_page.html', task='\n'.join(nls))
        
        
    return render_template('main_page.html')
    
if __name__ == '__main__':
    app.run(debug=True)