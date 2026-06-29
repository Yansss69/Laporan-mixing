import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Line Sachet Monitor", layout="wide")

st.markdown("### 🏭 Line Sachet Production Monitor")

# Menggunakan kolom agar form lebih ringkas
col1, col2 = st.columns(2)
with col1:
    op_name = st.text_input("Nama Operator")
    jam_mulai = st.text_input("Jam Mulai (HH:MM)", value="07:00")
with col2:
    shift = st.selectbox("Shift", ["Shift 1 (Pagi)", "Shift 2 (Siang)", "Shift 3 (Malam)"])
    durasi = st.radio("Durasi (Menit)", [40, 50], horizontal=True)

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
            "3m + 12m": detail_waktu,
            "Proses": f"{t1.strftime('%H:%M')} - {t2.strftime('%H:%M')}",
            "Hasil": f"{t_start.strftime('%H:%M')} - {t_end.strftime('%H:%M')}"
        })
    except: st.error("Format jam salah!")

# Tampilan tabel yang lebih profesional
if 'log_data' in st.session_state and st.session_state.log_data:
    df = pd.DataFrame(st.session_state.log_data)
    st.divider()
    st.write("### Data Log Hari Ini")
    st.dataframe(df, use_container_width=True) # Lebih modern daripada st.table()
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("💾 EXPORT KE EXCEL", csv, "log_produksi.csv", "text/csv", use_container_width=True)

if st.button("🔄 RESET SEMUA"):
    st.session_state.log_data = []
    st.rerun()
