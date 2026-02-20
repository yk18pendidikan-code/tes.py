import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Tes Minat & Bakat (RIASEC)",
    layout="centered"
)

st.title("Tes Minat & Bakat Neutron Murangan - Model RIASEC")
st.write("Jawablah setiap pernyataan sesuai dengan diri Anda.")
st.write("Skala: 1 = Sangat Tidak Sesuai | 5 = Sangat Sesuai")

questions = {
    "R": [
        "Saya senang bekerja dengan alat atau mesin.",
        "Saya suka kegiatan di luar ruangan.",
        "Saya tertarik memperbaiki barang rusak.",
        "Saya menikmati aktivitas fisik.",
        "Saya suka bekerja dengan tangan."
    ],
    "I": [
        "Saya suka memecahkan masalah kompleks.",
        "Saya menikmati penelitian atau eksperimen.",
        "Saya senang menganalisis data.",
        "Saya tertarik pada sains atau matematika.",
        "Saya suka berpikir logis dan sistematis."
    ],
    "A": [
        "Saya menikmati menggambar atau mendesain.",
        "Saya suka menulis cerita atau puisi.",
        "Saya tertarik pada musik atau seni pertunjukan.",
        "Saya senang mengekspresikan diri secara kreatif.",
        "Saya suka menciptakan ide-ide baru."
    ],
    "S": [
        "Saya senang membantu orang lain.",
        "Saya suka mengajar atau membimbing.",
        "Saya nyaman bekerja dalam tim.",
        "Saya peduli terhadap kesejahteraan orang lain.",
        "Saya senang berinteraksi dengan banyak orang."
    ],
    "E": [
        "Saya suka memimpin kelompok.",
        "Saya senang meyakinkan orang lain.",
        "Saya tertarik pada bisnis atau wirausaha.",
        "Saya suka mengambil keputusan penting.",
        "Saya senang berkompetisi."
    ],
    "C": [
        "Saya suka pekerjaan yang terstruktur.",
        "Saya teliti dalam mengerjakan tugas.",
        "Saya nyaman bekerja dengan angka atau data.",
        "Saya suka membuat perencanaan rinci.",
        "Saya mengikuti aturan dengan baik."
    ]
}

scores = {key: 0 for key in questions.keys()}

st.subheader("Silakan jawab pertanyaan berikut:")

for category, qs in questions.items():
    st.markdown(f"### Bagian {category}")
    for i, q in enumerate(qs):
        response = st.slider(
            label=q,
            min_value=1,
            max_value=5,
            value=3,
            key=f"{category}_{i}"
        )
        scores[category] += response

if st.button("Lihat Hasil"):
    st.subheader("Hasil Tes Anda")

    df = pd.DataFrame(scores.items(), columns=["Tipe", "Skor"])
    st.bar_chart(df.set_index("Tipe"))

    dominant = max(scores, key=scores.get)

    rekomendasi = {
        "R": "Teknik, Arsitektur, Otomotif, Teknologi Industri",
        "I": "Ilmu Data, Penelitian, Kedokteran, Sains",
        "A": "Desain Grafis, Musik, Seni, Penulisan",
        "S": "Psikologi, Pendidikan, Konseling, Keperawatan",
        "E": "Bisnis, Manajemen, Marketing, Wirausaha",
        "C": "Akuntansi, Administrasi, Keuangan, Analis Data"
    }

    st.success(f"Tipe dominan Anda adalah: {dominant}")
    st.info(f"Rekomendasi bidang yang cocok: {rekomendasi[dominant]}")

    st.caption("Tes ini berbasis teori RIASEC (Holland Code) dan bersifat eksploratif.")
