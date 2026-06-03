import streamlit as st
import pandas as pd
import os
import plotly.express as px
import io

# Konfigurasi Halaman
st.set_page_config(layout="wide", page_title="IT Asset Umara Group")

FILE_NAME = "laporan laptop terbaru (1).xlsx"

# Fungsi Load Data
@st.cache_data(ttl=60)
def load_data():
    if os.path.exists(FILE_NAME):
        try:
            df = pd.read_excel(FILE_NAME)
            df.columns = df.columns.str.strip()
            if 'No Aset' in df.columns:
                df['No Aset'] = df['No Aset'].astype(str).replace(['nan', 'None', ''], '-')
            return df.fillna("-")
        except:
            return pd.DataFrame()
    return pd.DataFrame()

if 'df' not in st.session_state:
    st.session_state.df = load_data()

# Fungsi Auto-Save (Menyimpan otomatis)
def auto_save():
    st.session_state.df.to_excel(FILE_NAME, index=False, engine='openpyxl')
    st.cache_data.clear()

# Fungsi Generate Nomor Aset
def generate_asset_id(df):
    bu_map = {"UCR": "UCR", "UNB": "UNB", "LBI": "LBI", "RNB": "RNB", "UMK": "UMK"}
    tahun = "26"
    for index, row in df.iterrows():
        val = str(row.get('No Aset', '-')).strip()
        if val in ["-", "nan", "None"]:
            bu = str(row.get('Bu Owner', '')).strip()
            if bu in bu_map:
                existing = df[(df['Bu Owner'] == bu) & (df['No Aset'].astype(str).str.contains(bu, na=False))]
                count = len(existing) + 1
                df.at[index, 'No Aset'] = f"{bu_map[bu]}-{tahun}-{count:03d}"
    return df

# 2. SIDEBAR
st.sidebar.title("Kontrol Dashboard")
status_filter = st.sidebar.selectbox("Filter Status:", ["Semua"] + list(st.session_state.df["Status"].unique()))

st.sidebar.subheader("Menu Aset")
if st.sidebar.button("➕ Tambah Baris"):
    new_row = pd.DataFrame([["-"] * len(st.session_state.df.columns)], columns=st.session_state.df.columns)
    st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
    auto_save()
    st.rerun()

if st.sidebar.button("🔢 Generate Nomor Aset"):
    st.session_state.df = generate_asset_id(st.session_state.df)
    auto_save()
    st.rerun()

# 4. MAIN DASHBOARD
st.title("📊 Dashboard IT Asset Umara Group")

filtered_df = st.session_state.df.copy()
if status_filter != "Semua":
    filtered_df = filtered_df[filtered_df["Status"] == status_filter]

# Tabel Data Editor (Auto-Save Aktif di Sini)
st.subheader("Data Inventaris")
df_edited = st.data_editor(
    filtered_df, use_container_width=True, num_rows="dynamic", key="inventory_editor",
    on_change=auto_save, # <--- DATA OTOMATIS TERSIMPAN SAAT EDIT
    column_config={"Status": st.column_config.SelectboxColumn("Status", options=["Tersedia", "Di Pakai", "Rusak", "Perlu Perbaikan"], required=True)}
)

if not df_edited.equals(filtered_df):
    st.session_state.df.update(df_edited)
    if len(df_edited) > len(filtered_df):
        st.session_state.df = df_edited

# Tombol Download (Pasti muncul di bawah tabel)
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    st.session_state.df.to_excel(writer, index=False)
buffer.seek(0)
st.download_button("📥 Download Laporan Lengkap (Excel)", buffer, "Laporan_IT_Asset.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
