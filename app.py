from flask import Flask, render_template

app = Flask(__name__)

# Rute untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Rute untuk halaman form diagnosa
@app.route('/form_diagnosa')
def form_diagnosa():
    return render_template('form.html')

@app.route('/hasil_diagnosa')
def hasil_diagnosa():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
