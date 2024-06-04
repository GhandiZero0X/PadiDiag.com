from flask import Flask, render_template, request
from expert_system import forward_chaining

app = Flask(__name__)

diseases = {
        #hama padi
        "Hama Walang Sangit": ["Bulir padi mengering dan berubah warna menjadi putih", 
                                "Produksi biji padi berkurang", 
                                "Bulir padi menjadi keriput", 
                                "Tanaman padi yang terserang menjadi kerdil", 
                                "Terdapat bau menyengat pada tanaman padi yang terserang"],
        "Hama Ganjur": ["Bulir padi mengering dan berubah warna menjadi putih", 
                        "Produksi biji padi berkurang", 
                        "Bulir padi menjadi keriput", 
                        "Tanaman padi yang terserang menjadi kerdil", 
                        "Terdapat tanda bekas hisapan pada bulir padi"],
        "Hama Tikus Sawah": ["Batang padi patah dan terpotong",
                                "Terdapat jejak gigitan pada batang padi",
                                "Biji padi dimakan sehingga hasil panen berkurang",
                                "Lubang dan sarang tikus terlihat di area sawah",
                                "Daun dan batang tanaman padi terlihat rusak dan terpotong"],
        "Hama Ulat Grayak": ["Daun padi mengalami kerusakan berat dengan adanya lubang-lubang besar",
                                "Daun padi menjadi compang-camping dan terkoyak",
                                "Tanaman padi yang terserang terlihat meranggas",
                                "Kehadira,n ulat pada tanaman padi terutama di malam hari",
                                "Penurunan fotosintesis akibat kerusakan daun yang parah"],
        "Hama Hama Kepik Hijau": ["Bulir padi yang berkembang menjadi kering dan hampa", 
                                    "Terdapat bercak hitam pada biji padi yang terserang.", 
                                    "Biji padi menjadi keriput dan tidak berkembang.", 
                                    "Daun padi yang terserang menunjukkan perubahan warna.", 
                                    "Penurunan hasil panen akibat biji padi yang rusak."],
        #penyakit padi
        "Busuk Akar": ["Tanaman layu meski kondisi tanah tidak kekurangan air",
                        "Akar tanaman berubah warna menjadi coklat hingga hitam",
                        "Tanaman mati secara tiba-tiba tanpa gejala awal yang jelas",
                        "Akar terlihat busuk dan rapuh saat dicabut",
                        "Pertumbuhan tanaman terhambat dan tidak normal"],
        "Penyakit Kresek": ["Muncul garis-garis coklat panjang pada daun padi.", 
                        "Daun padi mengering dan terlihat seperti terbakar.", 
                        "Lesi nekrotik berkembang pada daun.", 
                        "Daun padi menguning dan mati dari ujung daun.", 
                        "Tanaman padi yang terserang menunjukkan pertumbuhan terhambat."],
        "Karat Daun": ["Bercak kecil berwarna oranye muncul pada daun",
                        "Bercak berkembang menjadi pustula berkarat",
                        "Daun padi mengering dan mati dari ujung",
                        "Tanaman padi menjadi kerdil dan pertumbuhannya terhambat",
                        "Produktivitas tanaman padi menurun akibat daun yang rusak"],
        "Penyakit Blas (Blast)": ["Lesi berbentuk berlian muncul pada daun.", 
                        "Lesi menyebar dan menyebabkan daun mengering.", 
                        "Batang padi yang terserang menunjukkan lesi berwarna coklat kehitaman.", 
                        "Tanaman padi yang terserang mengalami kematian jika tidak diobati.", 
                        " Pertumbuhan tanaman terhambat dan produksi biji padi menurun."],
        "Tungro": ["Tanaman menunjukkan pertumbuhan yang terhambat",
                    "Daun padi menjadi kuning dengan garis-garis hijau",
                    "Biji padi tidak berkembang dan kering",
                    "Daun padi menggulung dan mengering",
                    "Tanaman padi yang terserang memiliki anakan yang lebih sedikit"],
}

# Rute untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form_diagnosa')
def form_diagnosa():
    # Create a set of unique symptoms
    unique_symptoms = set(symptom for symptoms in diseases.values() for symptom in symptoms)
    return render_template('form.html', symptoms=unique_symptoms)

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