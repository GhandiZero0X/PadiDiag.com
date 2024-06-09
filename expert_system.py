import logging
from operator import itemgetter

logging.basicConfig(level=logging.DEBUG)

def forward_chaining(selected_symptoms, bagian_tanaman, kondisi_iklim, hama_terlihat, tanda_penyakit):
    logging.debug(f"Selected symptoms: {selected_symptoms}, Bagian Tanaman: {bagian_tanaman}, Kondisi Iklim: {kondisi_iklim}, hama terlihat : {hama_terlihat}, Tanda Penyakit: {tanda_penyakit}")
    
    # Define the diseases and their related plant parts
    diseases = {
        "Hama Walang Sangit": {"gejala": ["Bulir padi mengering dan berubah warna menjadi putih", 
                                            "Produksi biji padi berkurang", 
                                            "Bulir padi menjadi keriput", 
                                            "Tanaman padi yang terserang menjadi kerdil", 
                                            "Terdapat bau menyengat pada tanaman padi yang terserang"],

                                            "bagian_tanaman": "Bulir Padi", 
                                            "kondisi_iklim": "Panas", 
                                            "hama_terlihat": "Ada"},
        "Hama Ganjur": {"gejala": ["Bulir padi mengering dan berubah warna menjadi putih", 
                                    "Produksi biji padi berkurang", 
                                    "Bulir padi menjadi keriput", 
                                    "Tanaman padi yang terserang menjadi kerdil", 
                                    "Terdapat tanda bekas hisapan pada bulir padi"],

                                    "bagian_tanaman": "Batang", 
                                    "kondisi_iklim": "Hujan", 
                                    "hama_terlihat": "Ada"},
        "Hama Tikus Sawah": {"gejala": ["Batang padi patah dan terpotong",
                                            "Terdapat jejak gigitan pada batang padi",
                                            "Biji padi dimakan sehingga hasil panen berkurang",
                                            "Lubang dan sarang tikus terlihat di area sawah",
                                            "Daun dan batang tanaman padi terlihat rusak dan terpotong"],

                                            "bagian_tanaman": "Semua Bagian Tumbuhan", 
                                            "kondisi_iklim": "Hujan", 
                                            "hama_terlihat": "Ada"},
        "Hama Ulat Grayak": {"gejala": ["Daun padi mengalami kerusakan berat dengan adanya lubang-lubang besar",
                                            "Daun padi menjadi compang-camping dan terkoyak",
                                            "Tanaman padi yang terserang terlihat meranggas",
                                            "Kehadiran ulat pada tanaman padi terutama di malam hari",
                                            "Penurunan fotosintesis akibat kerusakan daun yang parah"],

                                            "bagian_tanaman": "Daun", 
                                            "kondisi_iklim": "Lembab", 
                                            "hama_terlihat": "Ada"},
        "Hama Hama Kepik Hijau": {"gejala": ["Bulir padi yang berkembang menjadi kering dan hampa", 
                                                "Terdapat bercak hitam pada biji padi yang terserang", 
                                                "Biji padi menjadi keriput dan tidak berkembang", 
                                                "Daun padi yang terserang menunjukkan perubahan warna", 
                                                "Penurunan hasil panen akibat biji padi yang rusak"],

                                                "bagian_tanaman": "Bulir Padi", 
                                                "kondisi_iklim": "Lembab", 
                                                "hama_terlihat": "Ada"},
        "Busuk Akar": {"gejala": ["Tanaman layu meski kondisi tanah tidak kekurangan air",
                                    "Akar tanaman berubah warna menjadi coklat hingga hitam",
                                    "Tanaman mati secara tiba-tiba tanpa gejala awal yang jelas",
                                    "Akar terlihat busuk dan rapuh saat dicabut",
                                    "Pertumbuhan tanaman terhambat dan tidak normal"],

                                    "bagian_tanaman": "Akar", 
                                    "kondisi_iklim": "Hujan", 
                                    "tanda_penyakit": "Ada"},
        "Penyakit Kresek": {"gejala": ["Muncul garis-garis coklat panjang pada daun padi", 
                                        "Daun padi mengering dan terlihat seperti terbakar", 
                                        "Lesi nekrotik berkembang pada daun", 
                                        "Daun padi menguning dan mati dari ujung daun", 
                                        "Tanaman padi yang terserang menunjukkan pertumbuhan terhambat"],

                                        "bagian_tanaman": "Daun", 
                                        "kondisi_iklim": "Hujan", 
                                        "tanda_penyakit": "Ada"},
        "Karat Daun": {"gejala": ["Bercak kecil berwarna oranye muncul pada daun",
                                    "Bercak berkembang menjadi pustula berkarat",
                                    "Daun padi mengering dan mati dari ujung",
                                    "Tanaman padi menjadi kerdil dan pertumbuhannya terhambat",
                                    "Produktivitas tanaman padi menurun akibat daun yang rusak"],

                                    "bagian_tanaman": "Daun", 
                                    "kondisi_iklim": "Hujan" , 
                                    "tanda_penyakit": "Ada"},
        "Penyakit Blas (Blast)": {"gejala": ["Lesi berbentuk berlian muncul pada daun", 
                                                "Lesi menyebar dan menyebabkan daun mengering", 
                                                "Batang padi yang terserang menunjukkan lesi berwarna coklat kehitaman", 
                                                "Tanaman padi yang terserang mengalami kematian jika tidak diobati", 
                                                "Pertumbuhan tanaman terhambat dan produksi biji padi menurun"],

                                                "bagian_tanaman": "Daun", 
                                                "kondisi_iklim": "Hujan", 
                                                "tanda_penyakit": "Ada"},
        "Tungro": {"gejala": ["Tanaman menunjukkan pertumbuhan yang terhambat",
                                "Daun padi menjadi kuning dengan garis-garis hijau",
                                "Biji padi tidak berkembang dan kering",
                                "Daun padi menggulung dan mengering",
                                "Tanaman padi yang terserang memiliki anakan yang lebih sedikit"],

                                "bagian_tanaman": "Batang", 
                                "kondisi_iklim": "Hujan", 
                                "tanda_penyakit": "Ada"},
    }

    # Define the weights for each symptom
    symptom_weights = {
        #Hama Walang sangit dan Ganjur
        "Bulir padi mengering dan berubah warna menjadi putih": (
            5 if (bagian_tanaman == "Bulir Padi" or bagian_tanaman == "Batang") and 
            (kondisi_iklim == "Panas" or kondisi_iklim == "Hujan") and 
            hama_terlihat == "Ada" else 0
        ),
        "Produksi biji padi berkurang": (
            4 if (bagian_tanaman == "Bulir Padi" or bagian_tanaman == "Batang") and 
            (kondisi_iklim == "Panas" or kondisi_iklim == "Hujan") and 
            hama_terlihat == "Ada" else 0
        ),
        "Bulir padi menjadi keriput": (
            3 if (bagian_tanaman == "Bulir Padi" or bagian_tanaman == "Batang") and 
            (kondisi_iklim == "Panas" or kondisi_iklim == "Hujan") and 
            hama_terlihat == "Ada" else 0
        ),
        "Tanaman padi yang terserang menjadi kerdil": (
            2 if (bagian_tanaman == "Bulir Padi" or bagian_tanaman == "Batang") and 
            (kondisi_iklim == "Panas" or kondisi_iklim == "Hujan") and 
            hama_terlihat == "Ada" else 0
        ),
        "Terdapat bau menyengat pada tanaman padi yang terserang": 1 if bagian_tanaman == "Bulir Padi" and kondisi_iklim == "Panas" and hama_terlihat == "Ada" else 0,
        "Terdapat tanda bekas hisapan pada bulir padi": 1 if bagian_tanaman == "Batang" and kondisi_iklim == "Hujan" and hama_terlihat == "Ada" else 0,

        #Hama Tikus Sawah
        "Batang padi patah dan terpotong": 5 if bagian_tanaman == "Semua Bagian Tumbuhan" and kondisi_iklim == "Hujan" and hama_terlihat == "Ada" else 0,
        "Terdapat jejak gigitan pada batang padi": 4 if bagian_tanaman == "Semua Bagian Tumbuhan" and kondisi_iklim == "Hujan" and hama_terlihat == "Ada" else 0,
        "Biji padi dimakan sehingga hasil panen berkurang": 3 if bagian_tanaman == "Semua Bagian Tumbuhan" and kondisi_iklim == "Hujan" and hama_terlihat == "Ada" else 0,
        "Lubang dan sarang tikus terlihat di area sawah": 2 if bagian_tanaman == "Semua Bagian Tumbuhan" and kondisi_iklim == "Hujan" and hama_terlihat == "Ada" else 0,
        "Daun dan batang tanaman padi terlihat rusak dan terpotong": 1 if bagian_tanaman == "Semua Bagian Tumbuhan" and kondisi_iklim == "Hujan" and hama_terlihat == "Ada" else 0,

        #Hama Ulat Grayak
        "Daun padi mengalami kerusakan berat dengan adanya lubang-lubang besar": 5 if bagian_tanaman == "Daun" and kondisi_iklim == "Lembab" and hama_terlihat == "Ada" else 0,
        "Daun padi menjadi compang-camping dan terkoyak": 4 if bagian_tanaman == "Daun" and kondisi_iklim == "Lembab" and hama_terlihat == "Ada" else 0,
        "Tanaman padi yang terserang terlihat meranggas": 3 if bagian_tanaman == "Daun" and kondisi_iklim == "Lembab" and hama_terlihat == "Ada" else 0,
        "Kehadiran ulat pada tanaman padi terutama di malam hari": 2 if bagian_tanaman == "Daun" and kondisi_iklim == "Lembab" and hama_terlihat == "Ada" else 0,
        "Penurunan fotosintesis akibat kerusakan daun yang parah": 1 if bagian_tanaman == "Daun" and kondisi_iklim == "Lembab" and hama_terlihat == "Ada" else 0,

        #Hama Hama Kepik Hijau
        "Bulir padi yang berkembang menjadi kering dan hampa": 5 if bagian_tanaman == "Bulir Padi" and kondisi_iklim == "Lembab" and hama_terlihat == "Ada" else 0,
        "Terdapat bercak hitam pada biji padi yang terserang": 4 if bagian_tanaman == "Bulir Padi" and kondisi_iklim == "Lembab" and hama_terlihat == "Ada" else 0,
        "Biji padi menjadi keriput dan tidak berkembang": 3 if bagian_tanaman == "Bulir Padi" and kondisi_iklim == "Lembab" and hama_terlihat == "Ada" else 0,
        "Daun padi yang terserang menunjukkan perubahan warna": 2 if bagian_tanaman == "Bulir Padi" and kondisi_iklim == "Lembab" and hama_terlihat == "Ada" else 0,
        "Penurunan hasil panen akibat biji padi yang rusak": 1 if bagian_tanaman == "Bulir Padi" and kondisi_iklim == "Lembab" and hama_terlihat == "Ada" else 0,

        #Busuk Akar
        "Tanaman layu meski kondisi tanah tidak kekurangan air": 5 if bagian_tanaman == "Akar" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0,
        "Akar tanaman berubah warna menjadi coklat hingga hitam": 4 if bagian_tanaman == "Akar" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0,
        "Tanaman mati secara tiba-tiba tanpa gejala awal yang jelas": 3 if bagian_tanaman == "Akar" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0,
        "Akar terlihat busuk dan rapuh saat dicabut": 2 if bagian_tanaman == "Akar" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0,
        "Pertumbuhan tanaman terhambat dan tidak normal": 1 if bagian_tanaman == "Akar" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0,

        #Penyakit Kresek
        "Muncul garis-garis coklat panjang pada daun padi": 5 if bagian_tanaman == "Daun" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0, 
        "Daun padi mengering dan terlihat seperti terbakar": 4 if bagian_tanaman == "Daun" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0, 
        "Lesi nekrotik berkembang pada daun": 3 if bagian_tanaman == "Daun" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0, 
        "Daun padi menguning dan mati dari ujung daun": 2 if bagian_tanaman == "Daun" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0, 
        "Tanaman padi yang terserang menunjukkan pertumbuhan terhambat": 1 if bagian_tanaman == "Daun" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0,

        #Karat Daun
        "Bercak kecil berwarna oranye muncul pada daun": 5 if bagian_tanaman == "Daun" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0,
        "Bercak berkembang menjadi pustula berkarat": 4 if bagian_tanaman == "Daun" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0,
        "Daun padi mengering dan mati dari ujung": 3 if bagian_tanaman == "Daun" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0,
        "Tanaman padi menjadi kerdil dan pertumbuhannya terhambat": 2 if bagian_tanaman == "Daun" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0,
        "Produktivitas tanaman padi menurun akibat daun yang rusak": 1 if bagian_tanaman == "Daun" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0,

        #Penyakit Blas (Blast)
        "Lesi berbentuk berlian muncul pada daun": 5 if bagian_tanaman == "Daun" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0, 
        "Lesi menyebar dan menyebabkan daun mengering": 4 if bagian_tanaman == "Daun" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0, 
        "Batang padi yang terserang menunjukkan lesi berwarna coklat kehitaman": 3 if bagian_tanaman == "Daun" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0, 
        "Tanaman padi yang terserang mengalami kematian jika tidak diobati": 2 if bagian_tanaman == "Daun" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0, 
        "Pertumbuhan tanaman terhambat dan produksi biji padi menurun": 1 if bagian_tanaman == "Daun" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0,

        #Tungro
        "Tanaman menunjukkan pertumbuhan yang terhambat": 5 if bagian_tanaman == "Batang" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0,
        "Daun padi menjadi kuning dengan garis-garis hijau": 4 if bagian_tanaman == "Batang" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0,
        "Biji padi tidak berkembang dan kering": 3 if bagian_tanaman == "Batang" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0,
        "Daun padi menggulung dan mengering": 2 if bagian_tanaman == "Batang" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0,
        "Tanaman padi yang terserang memiliki anakan yang lebih sedikit": 1 if bagian_tanaman == "Batang" and kondisi_iklim == "Hujan" and tanda_penyakit == "Ada" else 0,
    }

    diagnosis_results = {}
    for disease, symptoms_info in diseases.items():
        logging.debug(f"Evaluating disease: {disease} with symptoms: {symptoms_info['gejala']} for {bagian_tanaman}")
        
        # Evaluasi gejala yang cocok
        matching_symptoms = [symptom for symptom in symptoms_info['gejala'] if symptom in selected_symptoms]
        match_percentage = len(matching_symptoms) / len(symptoms_info['gejala']) * 100
        total_weight = sum(symptom_weights.get(symptom, 0) for symptom in matching_symptoms)
        
        # Evaluasi kondisi iklim, hama terlihat, dan tanda penyakit
        if symptoms_info.get('kondisi_iklim') == kondisi_iklim:
            match_percentage += 10  # Tambahkan 10% jika kondisi iklim cocok
        if symptoms_info.get('hama_terlihat') == hama_terlihat:
            match_percentage += 15  # Tambahkan 15% jika hama terlihat
        if symptoms_info.get('tanda_penyakit') == tanda_penyakit:
            match_percentage += 20  # Tambahkan 20% jika ada tanda penyakit
        
        diagnosis_results[disease] = (match_percentage, total_weight)
    
    # Sorting results
    sorted_results = sorted(diagnosis_results.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)
    
    # Return diagnosis based on match percentage
    if all(result[1][0] < 80 for result in sorted_results):
        top_two_results = sorted_results[:2]
        logging.debug(f"Top two diagnosis results: {top_two_results}")
        return top_two_results
    else:
        high_match_results = [result for result in sorted_results if result[1][0] >= 80]
        logging.debug(f"Diagnosis results with match percentage >= 80%: {high_match_results}")
        return high_match_results