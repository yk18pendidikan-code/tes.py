import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Tes Bakat Diferensial (DAT)", layout="wide")

st.title("🧠 Tes Bakat Diferensial (DAT)")
st.write("""
Tes ini mengukur 5 kemampuan spesifik:
- Verbal Reasoning
- Numerical Ability
- Abstract Reasoning
- Mechanical Reasoning
- Spatial Ability
""")

# ----------------------------
# BANK SOAL
# ----------------------------

questions = {
    "Verbal Reasoning": [
        {"q": "Antonim dari 'Optimis' adalah:", "o": ["Pesimis", "Yakin", "Semangat", "Percaya"], "a": "Pesimis"},
        {"q": "Sinonim dari 'Cermat' adalah:", "o": ["Ceroboh", "Teliti", "Cepat", "Lambat"], "a": "Teliti"}
    ],
    "Numerical Ability": [
        {"q": "12 + 15 x 2 =", "o": ["54", "42", "30", "39"], "a": "42"},
        {"q": "25% dari 200 =", "o": ["25", "50", "75", "100"], "a": "50"}
    ],
    "Abstract Reasoning": [
        {"q": "Pola: 3, 6, 12, 24, ...", "o": ["36", "48", "30", "60"], "a": "48"},
        {"q": "A, C, F, J, ...", "o": ["O", "N", "P", "M"], "a": "O"}
    ],
    "Mechanical Reasoning": [
        {"q": "Jika gaya diperbesar maka percepatan:", "o": ["Tetap", "Berkurang", "Bertambah", "Hilang"], "a": "Bertambah"},
        {"q": "Katrol tetap berfungsi untuk:", "o": ["Mengurangi gaya", "Mengubah arah gaya", "Menambah berat", "Menghilangkan beban"], "a": "Mengubah arah gaya"}
    ],
    "Spatial Ability": [
        {"q": "Kubus memiliki berapa rusuk?", "o": ["8", "12", "6", "10"], "a": "12"},
        {"q": "Bangun 3D dari lingkaran diputar:", "o": ["Kubus", "Tabung", "Prisma", "Balok"], "a": "Tabung"}
    ]
}

# ----------------------------
# FORM TES
# ----------------------------

st.header("📋 Jawab Semua Pertanyaan")

scores = {}
total_questions = sum(len(qs) for qs in questions.values())
answered = 0

for category, qs in questions.items():
    st.subheader(f"🔹 {category}")
    score = 0
    
    for i, item in enumerate(qs):
        answer = st.radio(
            item["q"],
            item["o"],
            key=f"{category}_{i}"
        )
        if answer:
            answered += 1
        if answer == item["a"]:
            score += 1
    
    scores[category] = score

progress = answered / total_questions
st.progress(progress)

# ----------------------------
# HASIL
# ----------------------------

if st.button("🔍 Lihat Hasil Tes"):
    st.success("Tes selesai! Berikut hasil Anda:")

    df = pd.DataFrame({
        "Kategori": list(scores.keys()),
        "Skor": list(scores.values())
    })

    df["Maksimal"] = 2
    df["Persentase (%)"] = (df["Skor"] / df["Maksimal"]) * 100

    st.dataframe(df)

    # ----------------------------
    # RADAR CHART INTERAKTIF
    # ----------------------------

    fig = px.line_polar(
        df,
        r="Persentase (%)",
        theta="Kategori",
        line_close=True
    )

    fig.update_traces(fill='toself')
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,100])),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # INTERPRETASI
    # ----------------------------

    strongest = df.sort_values("Persentase (%)", ascending=False).iloc[0]

    st.header("📊 Interpretasi Hasil")
    st.write(f"💡 Kemampuan paling dominan Anda adalah **{strongest['Kategori']}** ({strongest['Persentase (%)']:.0f}%)")

    interpretation_map = {
        "Verbal Reasoning": "Cocok untuk hukum, komunikasi, pendidikan, sastra.",
        "Numerical Ability": "Cocok untuk teknik, akuntansi, statistika, data science.",
        "Abstract Reasoning": "Cocok untuk IT, programming, analisis sistem, riset.",
        "Mechanical Reasoning": "Cocok untuk teknik mesin, otomotif, teknik industri.",
        "Spatial Ability": "Cocok untuk arsitektur, desain, teknik sipil."
    }

    st.info(interpretation_map[strongest["Kategori"]])
    st.warning("Ini adalah simulasi sederhana dan bukan tes psikologi resmi.")
