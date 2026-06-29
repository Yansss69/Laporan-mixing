import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Pengaturan Halaman
st.set_page_config(page_title="Line Sachet Monitor", layout="centered")

st.title("Line Sachet Monitor 📊")

# Inisialisasi session state untuk menyimpan data
if 'log_data' not in st.session_state:
    st.session_state.log_data = []

# Input Form
op_name = st.text_input("Nama Operator")
shift = st.selectbox("Shift", ["Shift 1 (Pagi)", "Shift 2 (Siang)", "Shift 3 (Malam)"])
jam_mulai = st.text_input("Jam Mulai (HH:MM)", value="07:00")
durasi = st.radio("Durasi", [40, 50], horizontal=True)

if st.button("➕ TAMBAH LOG"):
    try:
        t_start = datetime.strptime(jam_mulai, "%H:%M")
        t1 = t_start + timedelta(minutes=3)
        t2 = t1 + timedelta(minutes=12)
        t3 = t2 + timedelta(minutes=3)
        t_end = t_start + timedelta(minutes=durasi)
        
        st.session_state.log_data.append({
            "Operator": op_name,
            "Shift": shift,
            "3m + 12m": f"{t_start.strftime('%H:%M')} - {t3.strftime('%H:%M')}",
            "Proses": f"{t1.strftime('%H:%M')} - {t2.strftime('%H:%M')}",
            "Hasil": f"{t_start.strftime('%H:%M')} - {t_end.strftime('%H:%M')}"
        })
        st.success("Data berhasil ditambahkan!")
    except:
        st.error("Format jam salah! Gunakan HH:MM")

# Tampilan Data
if st.session_state.log_data:
    df = pd.DataFrame(st.session_state.log_data)
    st.table(df)
    
    # Tombol Download Excel
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("💾 DOWNLOAD EXCEL", csv, "log_produksi.csv", "text/csv")

if st.button("🔄 RESET"):
    st.session_state.log_data = []
    st.rerun()
