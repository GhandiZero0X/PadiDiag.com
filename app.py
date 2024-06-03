from flask import Flask, render_template, request
from expert_system import diagnose_symptoms

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    symptoms = request.form.getlist('symptoms')
    diagnosis = diagnose_symptoms(symptoms)
    return render_template('result.html', diagnosis=diagnosis)

if __name__ == '__main__':
    app.run(debug=True)
