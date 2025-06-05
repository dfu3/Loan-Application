from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('loan_app.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    return f'Hello, {name}!'

