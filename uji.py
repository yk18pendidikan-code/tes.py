import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tes Pemilihan Jurusan SMA", layout="wide")

st.title("🎓 Tes Pemilihan Jurusan SMA")
st.write("Tes ini membantu menentukan jurusan yang paling sesuai: IPA, IPS, atau Bahasa.")

questions = [
    # NUMERIK (IPA)
    {"q": "Saya menyukai pelajaran Matematika.", "type": "IPA"},
    {"q": "Saya mudah memahami rumus dan perhitungan.", "type": "IPA"},
    {"q": "Saya tertarik dengan eksperimen sains.", "type": "IPA"},
    
    # SOSIAL (IPS)
    {"q": "Saya tertarik dengan isu sosial dan ekonomi.", "type": "IPS"},
    {"q": "Saya suka berdiskusi tentang masyarakat dan politik.", "type": "IPS"},
    {"q": "Saya menikmati pelajaran sejarah/geografi.", "type": "IPS"},
    
    # BAHASA
    {"q": "Saya suka menulis cerita atau artikel.", "type": "Bahasa"},
    {"q": "Saya mudah menghafal kosakata bahasa asing.", "type": "Bahasa"},
    {"q": "Saya tertarik mempelajari budaya dan sastra.", "type": "Bahasa"},
]

scores = {"IPA": 0, "IPS": 0, "Bahasa": 0}

st.header("📋 Jawab Sesuai Kondisi Anda")

for i, item in enumerate(questions):
    answer = st.radio(
        item["q"],
        ["Sangat Tidak Setuju", "Tidak Setuju", "Netral", "Setuju", "Sangat Setuju"],
        key=i
    )
    
    value_map = {
        "Sangat Tidak Setuju": 1,
        "Tidak Setuju": 2,
        "Netral": 3,
        "Setuju": 4,
        "Sangat Setuju": 5
    }
    
    scores[item["type"]] += value_map[answer]

if st.button("🔍 Lihat Rekomendasi Jurusan"):
    
    df = pd.DataFrame({
        "Jurusan": list(scores.keys()),
        "Skor": list(scores.values())
    })

    st.subheader("📊 Hasil Skor")
    st.dataframe(df)

    fig = px.bar(df, x="Jurusan", y="Skor", color="Jurusan")
    st.plotly_chart(fig, use_container_width=True)

    recommended = df.sort_values("Skor", ascending=False).iloc[0]["Jurusan"]

    st.header("🎯 Rekomendasi Jurusan")
    st.success(f"Jurusan yang paling sesuai untuk Anda adalah: {recommended}")

    explanation = {
        "IPA": "Anda cenderung kuat dalam logika, numerik, dan sains. Cocok untuk jurusan IPA.",
        "IPS": "Anda memiliki minat sosial dan analisis masyarakat. Cocok untuk jurusan IPS.",
        "Bahasa": "Anda memiliki kecenderungan linguistik dan komunikasi. Cocok untuk jurusan Bahasa."
    }

    st.info(explanation[recommended])

    st.warning("Catatan: Ini adalah tes simulasi sederhana dan bukan tes psikologi resmi.")
