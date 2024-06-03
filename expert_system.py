import logging
from pyDatalog import pyDatalog

logging.basicConfig(level=logging.DEBUG)

def forward_chaining(selected_symptoms):
    logging.debug(f"Selected symptoms: {selected_symptoms}")
    
    # Inisialisasi pyDatalog di sini
    pyDatalog.clear()
    pyDatalog.create_terms('gejala, penyakit, diagnosa, G, P')
    
    # Definisikan predikat diagnosa
    def diagnosa(penyakit, gejala):
        return pyDatalog.Variable(penyakit, gejala)
    
    # Fakta tentang gejala dan penyakit
    rules = [
    {"if": ["Bulir padi mengering dan berubah warna menjadi putih", 
            "Produksi biji padi berkurang", 
            "Bulir padi menjadi keriput", 
            "Tanaman padi yang terserang menjadi kerdil", 
            "Terdapat bau menyengat pada tanaman padi yang terserang"], 
        "then": "Hama Walang Sangit"},
    {"if": ["Bulir padi mengering dan berubah warna menjadi putih", 
            "Produksi biji padi berkurang", 
            "Bulir padi menjadi keriput", 
            "Tanaman padi yang terserang menjadi kerdil", 
            "Terdapat tanda bekas hisapan pada bulir padi"], 
        "then": "Hama Ganjur"},
    {"if": ["Batang padi patah dan terpotong", 
            "Terdapat jejak gigitan pada batang padi", 
            "Biji padi dimakan sehingga hasil panen berkurang", 
            "Lubang dan sarang tikus terlihat di area sawah", 
            "Daun dan batang tanaman padi terlihat rusak dan terpotong"], 
        "then": "Hama Tikus Sawah"},
    {"if": ["Daun padi mengalami kerusakan berat dengan adanya lubang-lubang besar", 
            "Daun padi menjadi compang-camping dan terkoyak", 
            "Tanaman padi yang terserang terlihat meranggas", 
            "Kehadiran ulat pada tanaman padi terutama di malam hari", 
            "Penurunan fotosintesis akibat kerusakan daun yang parah"], 
        "then": "Hama Ulat Grayak"},
    {"if": ["Bulir padi yang berkembang menjadi kering dan hampa", 
            "Terdapat bercak hitam pada biji padi yang terserang", 
            "Biji padi menjadi keriput dan tidak berkembang", 
            "Daun padi yang terserang menunjukkan perubahan warna", 
            "Penurunan hasil panen akibat biji padi yang rusak"], 
        "then": "Hama Kepik Hijau"},
    {"if": ["Tanaman layu meski kondisi tanah tidak kekurangan air", 
            "Akar tanaman berubah warna menjadi coklat hingga hitam", 
            "Tanaman mati secara tiba-tiba tanpa gejala awal yang jelas", 
            "Akar terlihat busuk dan rapuh saat dicabut", 
            "Pertumbuhan tanaman terhambat dan tidak normal"], 
        "then": "Busuk Akar"},
    {"if": ["Muncul garis-garis coklat panjang pada daun padi", 
            "Daun padi mengering dan terlihat seperti terbakar", 
            "Lesi nekrotik berkembang pada daun", 
            "Daun padi menguning dan mati dari ujung daun", 
            "Tanaman padi yang terserang menunjukkan pertumbuhan terhambat"], 
        "then": "Penyakit Kresek"},
    {"if": ["Bercak kecil berwarna oranye muncul pada daun", 
            "Bercak berkembang menjadi pustula berkarat", 
            "Daun padi mengering dan mati dari ujung", 
            "Tanaman padi menjadi kerdil dan pertumbuhannya terhambat", 
            "Produktivitas tanaman padi menurun akibat daun yang rusak"], 
        "then": "Karat Daun (Leaf Rust)"},
    {"if": ["Lesi berbentuk berlian muncul pada daun", 
            "Lesi menyebar dan menyebabkan daun mengering", 
            "Batang padi yang terserang menunjukkan lesi berwarna coklat kehitaman", 
            "Tanaman padi yang terserang mengalami kematian jika tidak diobati", 
            "Pertumbuhan tanaman terhambat dan produksi biji padi menurun"], 
        "then": "Penyakit Blas (Blast)"},
    {"if": ["Tanaman menunjukkan pertumbuhan yang terhambat", 
            "Daun padi menjadi kuning dengan garis-garis hijau", 
            "Biji padi tidak berkembang dan kering", 
            "Daun padi menggulung dan mengering", 
            "Tanaman padi yang terserang memiliki anakan yang lebih sedikit"], 
        "then": "Tungro"}
]

    # Aturan untuk diagnosa berdasarkan gejala
    for rule in rules:
        for gejala in rule["if"]:
            pyDatalog.assert_fact('diagnosa', rule["then"], gejala)

    diagnosis_results = set()
    for penyakit in pyDatalog.ask('diagnosa(P, G)').answers:
        logging.debug(f"Evaluating disease: {penyakit[0]} with symptoms: {penyakit[1]}")
        if all(gejala in selected_symptoms for gejala in penyakit[1]):
            diagnosis_results.add(penyakit[0])
    
    logging.debug(f"Diagnosis results: {diagnosis_results}")
    return list(diagnosis_results)