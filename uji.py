import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tes Pemilihan Jurusan SMA", layout="wide")

st.title("🎓 Tes Pemilihan Jurusan SMA")
st.write("""
Geser slider sesuai dengan diri Anda:

1 = Sangat Tidak Sesuai  
2 = Tidak Sesuai  
3 = Netral  
4 = Sesuai  
5 = Sangat Sesuai
""")

questions = [
    # IPA
    {"q": "Saya menyukai Matematika.", "type": "IPA"},
    {"q": "Saya mudah memahami rumus dan perhitungan.", "type": "IPA"},
    {"q": "Saya tertarik dengan eksperimen sains.", "type": "IPA"},
    {"q": "Saya suka pelajaran Fisika atau Biologi.", "type": "IPA"},

    # IPS
    {"q": "Saya tertarik dengan isu sosial dan ekonomi.", "type": "IPS"},
    {"q": "Saya suka berdiskusi tentang masyarakat dan politik.", "type": "IPS"},
    {"q": "Saya menikmati pelajaran sejarah/geografi.", "type": "IPS"},
    {"q": "Saya tertarik memahami perilaku manusia.", "type": "IPS"},

    # Bahasa
    {"q": "Saya suka menulis cerita atau artikel.", "type": "Bahasa"},
    {"q": "Saya mudah menghafal kosakata bahasa asing.", "type": "Bahasa"},
    {"q": "Saya tertarik mempelajari budaya dan sastra.", "type": "Bahasa"},
    {"q": "Saya nyaman berbicara di depan umum.", "type": "Bahasa"},
]

scores = {"IPA": 0, "IPS": 0, "Bahasa": 0}

st.header("📋 Jawab Pertanyaan Berikut")

for i, item in enumerate(questions):
    value = st.slider(
        item["q"],
        min_value=1,
        max_value=5,
        value=3,
        key=i
    )
    scores[item["type"]] += value

if st.button("🔍 Lihat Rekomendasi Jurusan"):
    
    df = pd.DataFrame({
        "Jurusan": list(scores.keys()),
        "Skor": list(scores.values())
    })

    st.subheader("📊 Hasil Skor")
    st.dataframe(df)

    # Grafik batang
    fig = px.bar(
        df,
        x="Jurusan",
        y="Skor",
        color="Jurusan",
        text="Skor"
    )
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    # Rekomendasi
    recommended = df.sort_values("Skor", ascending=False).iloc[0]["Jurusan"]

    st.header("🎯 Rekomendasi Jurusan")
    st.success(f"Jurusan yang paling sesuai untuk Anda adalah: {recommended}")

    explanation = {
        "IPA": "Anda cenderung kuat dalam logika, numerik, dan sains. Cocok memilih jurusan IPA.",
        "IPS": "Anda memiliki minat pada sosial, ekonomi, dan analisis masyarakat. Cocok memilih jurusan IPS.",
        "Bahasa": "Anda memiliki kecenderungan linguistik dan komunikasi yang baik. Cocok memilih jurusan Bahasa."
    }

    st.info(explanation[recommended])

    st.warning("Tes ini adalah simulasi sederhana dan bukan tes psikologi resmi.")
