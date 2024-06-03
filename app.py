from flask import Flask, render_template, request
from expert_system import forward_chaining

app = Flask(__name__)

# Rute untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form_diagnosa')
def form_diagnosa():
    return render_template('form.html')

@app.route('/diagnose', methods=['POST'])
def diagnose():
    nama = request.form['nama']
    kabupaten = request.form['kabupaten']
    hektar = request.form['hektar']
    selected_symptoms = request.form.getlist('gejala')
    bagian_tanaman = request.form['bagian_tanaman']
    kondisi_iklim = request.form['kondisi_iklim']
    intensitas_serangan = request.form['intensitas_serangan']
    hama_terlihat = request.form['hama_terlihat']
    tanda_penyakit = request.form['tanda_penyakit']

    diagnosis_results = forward_chaining(selected_symptoms)  # Kirim gejala sebagai string ke fungsi forward_chaining
    return render_template('result.html', nama=nama, kabupaten=kabupaten, hektar=hektar, gejala=selected_symptoms,
                           bagian_tanaman=bagian_tanaman, kondisi_iklim=kondisi_iklim,
                           intensitas_serangan=intensitas_serangan, hama_terlihat=hama_terlihat,
                           tanda_penyakit=tanda_penyakit, results=diagnosis_results)


if __name__ == '__main__':
    app.run(debug=True)