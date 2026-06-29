import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
from streamlit_lottie import st_lottie

# 1. Konfigurasi Halaman & Animasi
st.set_page_config(page_title="Line Sachet Monitor", page_icon="🚀", layout="centered")

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Load animasi
lottie_rocket = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_tTAb2t.json")

# 2. Tampilan Header
if lottie_rocket:
    st_lottie(lottie_rocket, height=150, key="rocket")
st.title("🚀 Line Sachet Monitor")
st.subheader("Sistem Monitoring Produksi")

# 3. Form Input
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        op_name = st.text_input("Nama Operator")
        jam_mulai = st.text_input("Jam Mulai (HH:MM)", value="07:00")
    with col2:
        shift = st.selectbox("Shift", ["Shift 1", "Shift 2", "Shift 3"])
        durasi = st.radio("Durasi (Min)", [40, 50], horizontal=True)

# 4. Logika Tambah Data
if st.button("➕ TAMBAH DATA PRODUKSI", use_container_width=True, type="primary"):
    try:
        t_start = datetime.strptime(jam_mulai, "%H:%M")
        t1 = t_start + timedelta(minutes=3)
        t2 = t1 + timedelta(minutes=12)
        t3 = t2 + timedelta(minutes=3)
        t_end = t_start + timedelta(minutes=durasi)
        
        detail_waktu = f"{t_start.strftime('%H:%M')}→{t1.strftime('%H:%M')}→{t2.strftime('%H:%M')}→{t3.strftime('%H:%M')}"
        
        if 'log_data' not in st.session_state: st.session_state.log_data = []
        st.session_state.log_data.append({
            "Operator": op_name, "Shift": shift,
            "Timeline": detail_waktu,
            "Proses": f"{t1.strftime('%H:%M')} - {t2.strftime('%H:%M')}",
            "Hasil": f"{t_start.strftime('%H:%M')} - {t_end.strftime('%H:%M')}"
        })
        st.rerun()
    except:
        st.error("Format jam salah! Gunakan HH:MM")

# 5. Tampilan Data & Download
if 'log_data' in st.session_state and st.session_state.log_data:
    st.divider()
    st.write("### 📋 Data Log Produksi")
    df = pd.DataFrame(st.session_state.log_data)
    st.dataframe(df, use_container_width=True)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("💾 EXPORT KE EXCEL", csv, "log_produksi.csv", "text/csv", use_container_width=True)
    
    if st.button("🔄 RESET SEMUA DATA"):
        st.session_state.log_data = []
        st.rerun()
