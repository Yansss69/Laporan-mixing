import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Konfigurasi halaman yang simpel dan elegan
st.set_page_config(page_title="Line Sachet Monitor", page_icon="🏭", layout="centered")

st.title("🚀 Line Mixing Sachet")
st.subheader("Production Data Entry")

# Layout Input dengan kolom agar lebih rapi di layar HP
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        op_name = st.text_input("Operator")
        jam_mulai = st.text_input("Jam Mulai", value="07:00")
    with col2:
        shift = st.selectbox("Shift", ["Shift 1", "Shift 2", "Shift 3"])
        durasi = st.radio("Durasi (Min)", [40, 50], horizontal=True)

# Tombol Tambah
if st.button("➕ TAMBAH LOG", use_container_width=True, type="primary"):
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
        st.rerun() # Refresh untuk update tabel
    except: st.error("Periksa kembali format jam (HH:MM)")

# Tampilan Tabel yang bersih
if 'log_data' in st.session_state and st.session_state.log_data:
    st.divider()
    df = pd.DataFrame(st.session_state.log_data)
    st.dataframe(df, use_container_width=True)
    
    # Tombol Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("💾 DOWNLOAD EXCEL", csv, "log_produksi.csv", "text/csv", use_container_width=True)
    
    if st.button("🔄 RESET"):
        st.session_state.log_data = []
        st.rerun()
