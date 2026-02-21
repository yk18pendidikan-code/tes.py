import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="Tes Pemilihan Jurusan SMA", layout="wide")
st.title("🎓 Tes Pemilihan Jurusan SMA – Neutron Murangan")

# ----------------------------
# Kode akses
# ----------------------------
ACCESS_CODE = "neutronmurangan"

if "access_granted" not in st.session_state:
    st.session_state.access_granted = False
if "test_completed" not in st.session_state:
    st.session_state.test_completed = False
if "scores" not in st.session_state:
    st.session_state.scores = {}

# ----------------------------
# Akses & Cek 1 Kali Pengerjaan
# ----------------------------
if not st.session_state.access_granted:
    kode = st.text_input("Masukkan Kode Akses:", type="password")
    if st.button("🔑 Submit"):
        if kode.strip() == ACCESS_CODE:
            st.session_state.access_granted = True
            st.success("Kode valid! Anda dapat melanjutkan tes.")
        else:
            st.error("Kode salah! Silakan coba lagi.")
    st.stop()  # Hentikan eksekusi sampai kode valid

if st.session_state.test_completed:
    st.info("Anda sudah menyelesaikan tes. Silakan download PDF laporan jika perlu.")
else:
    # ----------------------------
    # Tes Slider
    # ----------------------------
    st.write("""
    Geser slider sesuai dengan diri Anda:

    1 = Sangat Tidak Sesuai  
    2 = Tidak Sesuai  
    3 = Netral  
    4 = Sesuai  
    5 = Sangat Sesuai
    """)

    questions = [
        {"q": "Saya menyukai Matematika.", "type": "IPA"},
        {"q": "Saya mudah memahami rumus dan perhitungan.", "type": "IPA"},
        {"q": "Saya tertarik dengan eksperimen sains.", "type": "IPA"},
        {"q": "Saya suka pelajaran Fisika atau Biologi.", "type": "IPA"},
        {"q": "Saya tertarik dengan isu sosial dan ekonomi.", "type": "IPS"},
        {"q": "Saya suka berdiskusi tentang masyarakat dan politik.", "type": "IPS"},
        {"q": "Saya menikmati pelajaran sejarah/geografi.", "type": "IPS"},
        {"q": "Saya tertarik memahami perilaku manusia.", "type": "IPS"},
        {"q": "Saya suka menulis cerita atau artikel.", "type": "Bahasa"},
        {"q": "Saya mudah menghafal kosakata bahasa asing.", "type": "Bahasa"},
        {"q": "Saya tertarik mempelajari budaya dan sastra.", "type": "Bahasa"},
        {"q": "Saya nyaman berbicara di depan umum.", "type": "Bahasa"},
    ]

    scores = {"IPA": 0, "IPS": 0, "Bahasa": 0}

    st.header("📋 Jawab Pertanyaan Berikut")
    for i, item in enumerate(questions):
        val = st.slider(item["q"], 1,5,3,key=i)
        scores[item["type"]] += val

    if st.button("🔍 Lihat Hasil & Selesaikan Tes"):
        st.session_state.scores = scores
        st.session_state.test_completed = True
        st.success("Tes selesai! Anda dapat melihat hasil dan mendownload PDF.")

# ----------------------------
# Jika tes sudah selesai → tampilkan hasil & PDF
# ----------------------------
if st.session_state.test_completed:
    scores = st.session_state.scores

    df = pd.DataFrame({
        "Jurusan": list(scores.keys()),
        "Skor": list(scores.values())
    })
    df["Persentase (%)"] = df["Skor"] / df["Skor"].sum() * 100

    st.subheader("📊 Hasil Skor & Persentase")
    st.dataframe(df)

    # Radar chart
    fig = px.line_polar(df, r="Persentase (%)", theta="Jurusan", line_close=True)
    fig.update_traces(fill='toself')
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])))
    st.plotly_chart(fig, use_container_width=True)

    # Jurusan dominan & alternatif
    sorted_df = df.sort_values("Persentase (%)", ascending=False)
    main = sorted_df.iloc[0]["Jurusan"]
    second = sorted_df.iloc[1]["Jurusan"]

    st.header("🎯 Jurusan Dominan")
    st.success(f"{main} ({sorted_df.iloc[0]['Persentase (%)']:.1f}%)")

    st.subheader("📚 Program Studi Cocok")
    prodi_map = {
        "IPA":["Kedokteran","Teknik","Farmasi","Fisika","Kimia","Biologi",
               "Statistika","Keperawatan","Kesehatan Masyarakat","Teknik Elektro",
               "Teknik Mesin","Teknik Sipil"],
        "IPS":["Manajemen","Akuntansi","Ilmu Hukum","Psikologi","Ilmu Komunikasi",
               "Hubungan Internasional","Sosiologi","Ilmu Politik","Administrasi Negara",
               "Ekonomi Pembangunan"],
        "Bahasa":["Sastra Indonesia","Sastra Inggris","Pendidikan Bahasa Inggris",
                  "Pendidikan Bahasa Indonesia","Linguistik","Ilmu Perpustakaan",
                  "Penerjemahan","Jurnalistik"]
    }

    for idx, p in enumerate(prodi_map[main], start=1):
        st.write(f"{idx}. {p} (Kecocokan ± {sorted_df.iloc[0]['Persentase (%)']:.0f}%)")

    st.subheader("🔄 Alternatif Jurusan Kedua")
    for idx, p in enumerate(prodi_map[second][:5], start=1):
        st.write(f"{idx}. {p}")

    # ----------------------------
    # Export PDF Lengkap
    # ----------------------------
    pdf_buffer = BytesIO()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0,10,"Laporan Tes Pemilihan Jurusan SMA", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)

    # Skor
    for i, row in df.iterrows():
        pdf.cell(0,8,f"{row['Jurusan']}: {row['Persentase (%)']:.1f}%", ln=True)
    pdf.ln(5)

    pdf.cell(0,8,f"Jurusan Dominan: {main}", ln=True)
    pdf.cell(0,8,"Program Studi Cocok:", ln=True)
    for idx, p in enumerate(prodi_map[main], start=1):
        pdf.cell(0,8,f"{idx}. {p}", ln=True)

    pdf.ln(5)
    pdf.cell(0,8,"Alternatif Jurusan Kedua:", ln=True)
    for idx, p in enumerate(prodi_map[second][:5], start=1):
        pdf.cell(0,8,f"{idx}. {p}", ln=True)

    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    st.download_button(
        label="⬇ Unduh PDF Laporan",
        data=pdf_buffer,
        file_name="Laporan_Tes_Jurusan.pdf",
        mime="application/pdf"
    )
