from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        ui = request.form.get('task')
        return render_template('main_page.html', task=ui)
    return render_template('main_page.html')
    
if __name__ == '__main__':
    app.run(debug=True)