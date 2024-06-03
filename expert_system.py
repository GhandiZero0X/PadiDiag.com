def diagnose_symptoms(symptoms):
    dengue_fever_symptoms = {
        "demam tinggi": True,
        "sakit kepala parah": True,
        "nyeri di belakang mata": True,
        "nyeri sendi dan otot": True,
        "mual dan muntah": True,
        "ruam kulit": True,
        "pembengkakan kelenjar": True
    }
    
    typhoid_symptoms = {
        "demam yang meningkat bertahap": True,
        "sakit kepala": True,
        "kelelahan dan kelemahan": True,
        "nyeri otot": True,
        "berkeringat": True,
        "batuk kering": True,
        "nafsu makan menurun": True,
        "penurunan berat badan": True
    }
    
    dengue_fever_score = sum(symptom in dengue_fever_symptoms for symptom in symptoms)
    typhoid_score = sum(symptom in typhoid_symptoms for symptom in symptoms)
    
    if dengue_fever_score > typhoid_score:
        return "Kemungkinan besar Anda mengalami demam berdarah."
    elif typhoid_score > dengue_fever_score:
        return "Kemungkinan besar Anda mengalami tipes."
    else:
        return "Gejala Anda tidak cukup spesifik untuk menentukan apakah Anda mengalami demam berdarah atau tipes. Silakan konsultasikan dengan dokter."
