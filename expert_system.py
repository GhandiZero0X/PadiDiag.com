from flask import request, render_template
from flask import Flask
import logging
from operator import itemgetter

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

def forward_chaining(selected_symptoms, bagian_tanaman, kondisi_iklim):
    logging.debug(f"Selected symptoms: {selected_symptoms}, Bagian Tanaman: {bagian_tanaman}, Kondisi Iklim: {kondisi_iklim}")
    
    # Define the diseases and their related plant parts
    diseases = {
        "Hama Walang Sangit": {"gejala": ["Bulir padi mengering dan berubah warna menjadi putih", 
                                            "Produksi biji padi berkurang", 
                                            "Bulir padi menjadi keriput", 
                                            "Tanaman padi yang terserang menjadi kerdil", 
                                            "Terdapat bau menyengat pada tanaman padi yang terserang"],
                                            "bagian_tanaman": "Bulir Padi", "kondisi_iklim": "panas"},
        "Hama Ganjur": {"gejala": ["Bulir padi mengering dan berubah warna menjadi putih", 
                                    "Produksi biji padi berkurang", 
                                    "Bulir padi menjadi keriput", 
                                    "Tanaman padi yang terserang menjadi kerdil", 
                                    "Terdapat tanda bekas hisapan pada bulir padi"],
                                    "bagian_tanaman": "Batang", "kondisi_iklim": "hujan"},
        "Hama Tikus Sawah": {"gejala": ["Batang padi patah dan terpotong",
                                            "Terdapat jejak gigitan pada batang padi",
                                            "Biji padi dimakan sehingga hasil panen berkurang",
                                            "Lubang dan sarang tikus terlihat di area sawah",
                                            "Daun dan batang tanaman padi terlihat rusak dan terpotong"],
                                            "bagian_tanaman": "Semua Bagian Tumbuhan", "kondisi_iklim": "hujan"},
        "Hama Ulat Grayak": {"gejala": ["Daun padi mengalami kerusakan berat dengan adanya lubang-lubang besar",
                                            "Daun padi menjadi compang-camping dan terkoyak",
                                            "Tanaman padi yang terserang terlihat meranggas",
                                            "Kehadiran ulat pada tanaman padi terutama di malam hari",
                                            "Penurunan fotosintesis akibat kerusakan daun yang parah"],
                                            "bagian_tanaman": "Daun", "kondisi_iklim": "lembab"},
        "Hama Hama Kepik Hijau": {"gejala": ["Bulir padi yang berkembang menjadi kering dan hampa", 
                                                "Terdapat bercak hitam pada biji padi yang terserang.", 
                                                "Biji padi menjadi keriput dan tidak berkembang.", 
                                                "Daun padi yang terserang menunjukkan perubahan warna.", 
                                                "Penurunan hasil panen akibat biji padi yang rusak."],
                                                "bagian_tanaman": "Bulir Padi", "kondisi_iklim": "lembab"},
        "Busuk Akar": {"gejala": ["Tanaman layu meski kondisi tanah tidak kekurangan air",
                                    "Akar tanaman berubah warna menjadi coklat hingga hitam",
                                    "Tanaman mati secara tiba-tiba tanpa gejala awal yang jelas",
                                    "Akar terlihat busuk dan rapuh saat dicabut",
                                    "Pertumbuhan tanaman terhambat dan tidak normal"],
                                    "bagian_tanaman": "Akar", "kondisi_iklim": "hujan"},
        "Penyakit Kresek": {"gejala": ["Muncul garis-garis coklat panjang pada daun padi.", 
                                        "Daun padi mengering dan terlihat seperti terbakar.", 
                                        "Lesi nekrotik berkembang pada daun.", 
                                        "Daun padi menguning dan mati dari ujung daun.", 
                                        "Tanaman padi yang terserang menunjukkan pertumbuhan terhambat."],
                                        "bagian_tanaman": "Daun", "kondisi_iklim": "hujan"},
        "Karat Daun": {"gejala": ["Bercak kecil berwarna oranye muncul pada daun",
                                    "Bercak berkembang menjadi pustula berkarat",
                                    "Daun padi mengering dan mati dari ujung",
                                    "Tanaman padi menjadi kerdil dan pertumbuhannya terhambat",
                                    "Produktivitas tanaman padi menurun akibat daun yang rusak"],
                                    "bagian_tanaman": "Daun", "kondisi_iklim": "hujan"},
        "Penyakit Blas (Blast)": {"gejala": ["Lesi berbentuk berlian muncul pada daun.", 
                                                "Lesi menyebar dan menyebabkan daun mengering.", 
                                                "Batang padi yang terserang menunjukkan lesi berwarna coklat kehitaman.", 
                                                "Tanaman padi yang terserang mengalami kematian jika tidak diobati.", 
                                                "Pertumbuhan tanaman terhambat dan produksi biji padi menurun."],
                                                "bagian_tanaman": "Daun", "kondisi_iklim": "hujan"},
        "Tungro": {"gejala": ["Tanaman menunjukkan pertumbuhan yang terhambat",
                                "Daun padi menjadi kuning dengan garis-garis hijau",
                                "Biji padi tidak berkembang dan kering",
                                "Daun padi menggulung dan mengering",
                                "Tanaman padi yang terserang memiliki anakan yang lebih sedikit"],
                                "bagian_tanaman": "Batang", "kondisi_iklim": "hujan"},
    }
    
    # Define the weights for each symptom
    symptom_weights = {
        # Weight based on the part of the plant affected
        "Bulir padi mengering dan berubah warna menjadi putih": 5 if bagian_tanaman == "Bulir Padi" else 0,
        "Produksi biji padi berkurang": 4 if bagian_tanaman == "Bulir Padi" else 0,
        "Bulir padi menjadi keriput": 3 if bagian_tanaman == "Bulir Padi" else   0,
        "Tanaman padi yang terserang menjadi kerdil": 2 if bagian_tanaman == "Bulir Padi" else 0,
        "Terdapat bau menyengat pada tanaman padi yang terserang": 1 if bagian_tanaman == "Bulir Padi" else 0,
        "Terdapat tanda bekas hisapan pada bulir padi": 1 if bagian_tanaman == "Bulir Padi" else 0,
        "Daun padi mengalami kerusakan berat dengan adanya lubang-lubang besar": 5 if bagian_tanaman == "Daun" else 0,
        "Daun padi menjadi compang-camping dan terkoyak": 4 if bagian_tanaman == "Daun" else 0,
        "Tanaman padi yang terserang terlihat meranggas": 3 if bagian_tanaman == "Daun" else 0,
        "Kehadiran ulat pada tanaman padi terutama di malam hari": 2 if bagian_tanaman == "Daun" else 0,
        "Penurunan fotosintesis akibat kerusakan daun yang parah": 1 if bagian_tanaman == "Daun" else 0,
        "Tanaman layu meski kondisi tanah tidak kekurangan air": 5 if bagian_tanaman == "Akar" else 0,
        "Akar tanaman berubah warna menjadi coklat hingga hitam": 4 if bagian_tanaman == "Akar" else 0,
        "Tanaman mati secara tiba-tiba tanpa gejala awal yang jelas": 3 if bagian_tanaman == "Akar" else 0,
        "Akar terlihat busuk dan rapuh saat dicabut": 2 if bagian_tanaman == "Akar" else 0,
        "Pertumbuhan tanaman terhambat dan tidak normal": 1 if bagian_tanaman == "Akar" else 0,
        "Bercak kecil berwarna oranye muncul pada daun": 5 if bagian_tanaman == "Daun" else 0,
        "Bercak berkembang menjadi pustula berkarat": 4 if bagian_tanaman == "Daun" else 0,
        "Daun padi mengering dan mati dari ujung": 3 if bagian_tanaman == "Daun" else 0,
        "Batang padi patah dan terpotong": 5 if bagian_tanaman == "Batang" else 0,
        "Terdapat jejak gigitan pada batang padi": 4 if bagian_tanaman == "Batang" else 0,
        "Biji padi dimakan sehingga hasil panen berkurang": 3 if bagian_tanaman == "Batang" else 0,
        "Lubang dan sarang tikus terlihat di area sawah": 2 if bagian_tanaman == "Batang" else 0,
        "Terdapat bercak hitam pada biji padi yang terserang.": 1 if bagian_tanaman == "Bulir Padi" else 0,
        "Daun padi yang terserang menunjukkan perubahan warna.": 5 if bagian_tanaman == "Daun" else 0,
        "Penurunan hasil panen akibat biji padi yang rusak.": 4 if bagian_tanaman == "Bulir Padi" else 0,
        "Bulir padi yang berkembang menjadi kering dan hampa": 3 if bagian_tanaman == "Bulir Padi" else 0,
        "Daun padi yang terserang terlihat meranggas": 1 if bagian_tanaman == "Daun" else 0,
        "Kehadiran ulat pada tanaman padi terutama di malam hari": 5 if bagian_tanaman == "Daun" else 0,
        "Penurunan fotosintesis akibat kerusakan daun yang parah": 4 if bagian_tanaman == "Daun" else 0,
        "Tanaman layu meski kondisi tanah tidak kekurangan air": 3 if bagian_tanaman == "Akar" else 0,
        "Akar tanaman berubah warna menjadi coklat hingga hitam": 2 if bagian_tanaman == "Akar" else 0,
        "Tanaman mati secara tiba-tiba tanpa gejala awal yang jelas": 1 if bagian_tanaman == "Akar" else 0,
    }

    diagnosis_results = {}
    for disease, symptoms_info in diseases.items():
        logging.debug(f"Evaluating disease: {disease} with symptoms: {symptoms_info['gejala']} for {bagian_tanaman}")
        matching_symptoms = [symptom for symptom in symptoms_info['gejala'] if symptom in selected_symptoms]
        match_percentage = len(matching_symptoms) / len(symptoms_info['gejala']) * 100
        # Calculate the total weight for the matching symptoms
        total_weight = sum(symptom_weights.get(symptom, 0) for symptom in matching_symptoms)
        # Add additional weight based on climate condition match
        if kondisi_iklim == symptoms_info['kondisi_iklim']:
            total_weight += 1
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
