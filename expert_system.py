
rules = [
    {"if": ["Bulir padi mengering dan berubah warna menjadi putih", "Produksi biji padi berkurang"], "then": "Hama 1"},
    {"if": ["Bulir padi menjadi keriput", "Tanaman padi yang terserang menjadi kerdil"], "then": "Penyakit 1"},
    # Tambahkan aturan lainnya
]

def forward_chaining(facts):
    conclusions = []
    for rule in rules:
        if all(fact in facts for fact in rule["if"]):
            conclusions.append(rule["then"])
    return conclusions
