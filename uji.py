import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Tes Bakat Diferensial (DAT)", layout="wide")

st.title("🧠 Tes Bakat Diferensial (DAT)")
st.write("""
Tes ini mengukur kemampuan spesifik (aptitude):
- Verbal Reasoning
- Numerical Ability
- Abstract Reasoning
- Mechanical Reasoning
- Spatial Ability
""")

# -----------------------------
# BANK SOAL
# -----------------------------

questions = {
    "Verbal Reasoning": [
        {
            "question": "Antonim dari 'Optimis' adalah:",
            "options": ["Pesimis", "Semangat", "Percaya", "Yakin"],
            "answer": "Pesimis"
        },
        {
            "question": "Kalimat yang paling tepat secara tata bahasa:",
            "options": [
                "Dia pergi ke pasar kemarin.",
                "Dia kemarin pergi ke pasar akan.",
                "Pergi dia pasar kemarin.",
                "Kemarin pasar dia pergi akan."
            ],
            "answer": "Dia pergi ke pasar kemarin."
        }
    ],
    "Numerical Ability": [
        {
            "question": "12 + 15 x 2 = ?",
            "options": ["54", "42", "30", "39"],
            "answer": "42"
        },
        {
            "question": "Jika 25% dari 200 adalah:",
            "options": ["25", "50", "75", "100"],
            "answer": "50"
        }
    ],
    "Abstract Reasoning": [
        {
            "question": "Pola angka: 3, 6, 12, 24, ...",
            "options": ["36", "48", "30", "60"],
            "answer": "48"
        },
        {
            "question": "A, C, F, J, ... huruf berikutnya?",
            "options": ["O", "N", "P", "M"],
            "answer": "O"
        }
    ],
    "Mechanical Reasoning": [
        {
            "question": "Jika gaya diperbesar, maka percepatan akan:",
            "options": ["Tetap", "Berkurang", "Bertambah", "Hilangkan"],
            "answer": "Bertambah"
        },
        {
            "question": "Katrol tetap berfungsi untuk:",
            "options": [
                "Mengurangi gaya",
                "Mengubah arah gaya",
                "Menambah berat",
                "Menghilangkan beban"
            ],
            "answer": "Mengubah arah gaya"
        }
    ],
    "Spatial Ability": [
        {
            "question": "Kubus memiliki berapa rusuk?",
            "options": ["8", "12", "6", "10"],
            "answer": "12"
        },
        {
            "question": "Bangun 3D dari lingkaran yang diputar adalah:",
            "options": ["Kubus", "Tabung", "Prisma", "Balok"],
            "answer": "Tabung"
        }
    ]
}

# -----------------------------
# FORM TES
# -----------------------------

st.header("📋 Jawab Semua Pertanyaan")

scores = {}
total_questions = {}

for category, qs in questions.items():
    st.subheader(f"🔹 {category}")
    score = 0
    total_questions[category] = len(qs)
    
    for i, q in enumerate(qs):
        answer = st.radio(
            q["question"],
            q["options"],
            key=f"{category}_{i}"
        )
        if answer == q["answer"]:
            score += 1
    
    scores[category] = score

# -----------------------------
# HASIL
# -----------------------------

if st.button("🔍 Lihat Hasil Tes"):
    st.success("Tes selesai! Berikut hasil Anda:")

    df = pd.DataFrame({
        "Kategori": scores.keys(),
        "Skor": scores.values(),
        "Maksimal": total_questions.values()
    })

    df["Persentase (%)"] = (df["Skor"] / df["Maksimal"]) * 100
    st.dataframe(df)

    # -----------------------------
    # RADAR CHART
    # -----------------------------

    categories = list(scores.keys())
    values = df["Persentase (%)"].tolist()
    values += values[:1]

    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_yticklabels([])
    ax.set_title("Profil Bakat Diferensial (%)")

    st.pyplot(fig)

    # -----------------------------
    # INTERPRETASI
    # -----------------------------

    st.header("📊 Interpretasi")

    strongest = df.sort_values("Persentase (%)", ascending=False).iloc[0]

    st.write(f"💡 Kemampuan paling dominan Anda adalah **{strongest['Kategori']}** ({strongest['Persentase (%)']:.0f}%).")

    interpretations = {
        "Verbal Reasoning": "Cocok untuk hukum, komunikasi, pendidikan, sastra.",
        "Numerical Ability": "Cocok untuk teknik, akuntansi, statistika, data science.",
        "Abstract Reasoning": "Cocok untuk IT, programming, analisis sistem, riset.",
        "Mechanical Reasoning": "Cocok untuk teknik mesin, otomotif, teknik industri.",
        "Spatial Ability": "Cocok untuk arsitektur, desain, teknik sipil."
    }

    st.info(interpretations[strongest["Kategori"]])

    st.warning("Catatan: Ini adalah simulasi sederhana Tes DAT dan bukan tes psikologi resmi.")
