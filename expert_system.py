import logging
from operator import itemgetter

logging.basicConfig(level=logging.DEBUG)

def forward_chaining(selected_symptoms, bagian_tanaman, kondisi_iklim, intensitas_serangan, hama_terlihat, tanda_penyakit):
    logging.debug(f"Selected symptoms: {selected_symptoms}")
    logging.debug(f"Bagian tanaman: {bagian_tanaman}")
    logging.debug(f"Kondisi iklim: {kondisi_iklim}")
    logging.debug(f"Intensitas serangan: {intensitas_serangan}")
    logging.debug(f"Hama terlihat: {hama_terlihat}")
    logging.debug(f"Tanda penyakit: {tanda_penyakit}")
    
    # Define the symptoms and diseases
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
    
    # Define the weights for each symptom
    symptom_weights = {
        "Bulir padi mengering dan berubah warna menjadi putih": 5,
        "Produksi biji padi berkurang": 4,
        "Bulir padi menjadi keriput": 3,
        "Tanaman padi yang terserang menjadi kerdil": 2,
        "Terdapat bau menyengat pada tanaman padi yang terserang": 1,
        "Terdapat tanda bekas hisapan pada bulir padi": 1,
        "Daun padi mengalami kerusakan berat dengan adanya lubang-lubang besar": 5,
        "Daun padi menjadi compang-camping dan terkoyak": 4,
        "Tanaman padi yang terserang terlihat meranggas": 3,
        "Kehadira,n ulat pada tanaman padi terutama di malam hari": 2,
        "Penurunan fotosintesis akibat kerusakan daun yang parah": 1,
        "Tanaman layu meski kondisi tanah tidak kekurangan air": 5,
        "Akar tanaman berubah warna menjadi coklat hingga hitam": 4,
        "Tanaman mati secara tiba-tiba tanpa gejala awal yang jelas": 3,
        "Akar terlihat busuk dan rapuh saat dicabut": 2,
        "Pertumbuhan tanaman terhambat dan tidak normal": 1,
        "Bercak kecil berwarna oranye muncul pada daun": 5,
        "Bercak berkembang menjadi pustula berkarat": 4,
        "Daun padi mengering dan mati dari ujung": 3,
        "Tanaman padi menjadi kerdil dan pertumbuhannya terhambat": 2,
        "Produktivitas tanaman padi menurun akibat daun yang rusak": 1,
        "Muncul garis-garis coklat panjang pada daun padi.": 5,
        "Daun padi mengering dan terlihat seperti terbakar.": 4,
        "Lesi nekrotik berkembang pada daun.": 3,
        "Daun padi menguning dan mati dari ujung daun.": 2,
        "Tanaman padi yang terserang menunjukkan pertumbuhan terhambat.": 1,
        "Lesi menyebar dan menyebabkan daun mengering.": 5,
        "Batang padi patah dan terpotong": 5,
        "Terdapat jejak gigitan pada batang padi": 4,
        "Biji padi dimakan sehingga hasil panen berkurang": 3,
        "Lubang dan sarang tikus terlihat di area sawah": 2,
        "Terdapat bercak hitam pada biji padi yang terserang.": 1,
        "Daun padi yang terserang menunjukkan perubahan warna.": 5,
        "Penurunan hasil panen akibat biji padi yang rusak.": 4,
        "Bulir padi yang berkembang menjadi kering dan hampa": 3,
        "Terdapat tanda bekas hisapan pada bulir padi": 2,
        "Daun padi yang terserang terlihat meranggas": 1,
        "Kehadira,n ulat pada tanaman padi terutama di malam hari": 5,
        "Penurunan fotosintesis akibat kerusakan daun yang parah": 4,
        "Tanaman layu meski kondisi tanah tidak kekurangan air": 3,
        "Akar tanaman berubah warna menjadi coklat hingga hitam": 2,
        "Tanaman mati secara tiba-tiba tanpa gejala awal yang jelas": 1,
        "Akar terlihat busuk dan rapuh saat dicabut": 5,
        "Pertumbuhan tanaman terhambat dan tidak normal": 2,
        "Bercak kecil berwarna oranye muncul pada daun": 5,
        "Bercak berkembang menjadi pustula berkarat": 4,
        "Daun padi mengering dan mati dari ujung": 3,
    }

    bagian_tanaman_weight = {"Daun": 2, "Batang": 2, "Bulir Padi": 2}  # Ubah bobot sesuai kebutuhan
    kondisi_iklim_weight = {"Panas dan Lebat": 3, "Hangat dan Basah": 2, "Dingin dan Kering": 1}  # Ubah bobot sesuai kebutuhan
    intensitas_serangan_weight = {"Rendah": 1, "Sedang": 2, "Tinggi": 3}  # Ubah bobot sesuai kebutuhan
    hama_terlihat_weight = 1  # Ubah bobot sesuai kebutuhan
    tanda_penyakit_weight = 1  # Ubah bobot sesuai kebutuhan

    diagnosis_results = {}
    for disease, symptoms in diseases.items():
        logging.debug(f"Evaluating disease: {disease} with symptoms: {symptoms}")
        matching_symptoms = [symptom for symptom in symptoms if symptom in selected_symptoms]
        match_percentage = len(matching_symptoms) / len(symptoms) * 100

        # Calculate the total weight for the matching symptoms
        total_weight = sum(symptom_weights.get(symptom, 0) for symptom in matching_symptoms)

        # Consider plant part, climate condition, attack intensity, visible pests, and signs of disease
        total_weight += bagian_tanaman_weight.get(bagian_tanaman, 0)
        total_weight += kondisi_iklim_weight.get(kondisi_iklim, 0)
        total_weight += intensitas_serangan_weight.get(intensitas_serangan, 0)
        total_weight += hama_terlihat_weight if hama_terlihat == "Yes" else 0
        total_weight += tanda_penyakit_weight if tanda_penyakit == "Yes" else 0

        diagnosis_results[disease] = (match_percentage, total_weight)
    
    # Sort the results by match percentage and total weight
    sorted_results = sorted(diagnosis_results.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)
    
    # Check if all match percentages are below 80%
    if all(result[1][0] < 80 for result in sorted_results):
        # If so, return the top 2 results
        top_two_results = sorted_results[:2]
        logging.debug(f"Top two diagnosis results: {top_two_results}")
        return top_two_results
    else:
        # Otherwise, return all results with match percentage >= 80%
        high_match_results = [result for result in sorted_results if result[1][0] >= 80]
        logging.debug(f"Diagnosis results with match percentage >= 80%: {high_match_results}")
        return high_match_results