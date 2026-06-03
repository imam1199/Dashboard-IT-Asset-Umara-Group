import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide", page_title="IT Asset Umara Group")

FILE_NAME = "laporan laptop terbaru (1).xlsx"

# 1. Load Data dengan pembersihan
@st.cache_data
def load_data():
    if os.path.exists(FILE_NAME):
        df = pd.read_excel(FILE_NAME)
        # Pastikan kolom No Aset dibaca sebagai string dan isi kosong jadi '-'
        df['No Aset'] = df['No Aset'].astype(str).replace(['nan', 'None', ''], '-')
        return df.fillna("-")
    return pd.DataFrame()

if 'df' not in st.session_state:
    st.session_state.df = load_data()

# Fungsi Generate Nomor Aset
def generate_asset_id(df):
    bu_map = {"UCR": "UCR", "UNB": "UNB", "LBI": "LBI", "RNB": "RNB", "UMK": "UMK"}
    tahun = "26" 
    
    for index, row in df.iterrows():
        # Cek jika baris kosong atau No Aset belum ada
        val = str(row['No Aset']).strip()
        if val == "-" or val == "nan" or val == "None":
            bu = str(row['Bu Owner']).strip()
            if bu in bu_map:
                # Hitung urutan berdasarkan BU yang sama
                existing = df[(df['Bu Owner'] == bu) & (df['No Aset'].str.contains(bu, na=False))]
                count = len(existing) + 1
                df.at[index, 'No Aset'] = f"{bu_map[bu]}-{tahun}-{count:03d}"
    return df

# 2. SIDEBAR (FILTER & TOMBOL FUNGSI)
st.sidebar.title("Kontrol Dashboard")

# Filter Status
unique_status = ["Semua"] + list(st.session_state.df["Status"].unique())
status_filter = st.sidebar.selectbox("Filter Status:", unique_status, key="status_key")

st.sidebar.markdown("---")
st.sidebar.subheader("Menu Edit & Aset")

if st.sidebar.button("➕ Tambah Baris Baru"):
    new_row = pd.DataFrame([["-"] * len(st.session_state.df.columns)], columns=st.session_state.df.columns)
    st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
    st.rerun()

if st.sidebar.button("🔢 Generate Nomor Aset"):
    st.session_state.df = generate_asset_id(st.session_state.df)
    st.rerun()

if st.sidebar.button("🗑️ Hapus Baris Terakhir"):
    if not st.session_state.df.empty:
        st.session_state.df = st.session_state.df.iloc[:-1]
        st.rerun()

if st.sidebar.button("💾 Simpan Data"):
    st.session_state.df.to_excel(FILE_NAME, index=False)
    st.success("Berhasil disimpan!")

# 3. FILTER LOGIC
if status_filter == "Semua":
    filtered_df = st.session_state.df
else:
    filtered_df = st.session_state.df[st.session_state.df["Status"] == status_filter]

# 4. MAIN DASHBOARD
st.title("📊 Dashboard IT Asset Umara Group")

# Metrik
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Unit", len(filtered_df))
col2.metric("Tersedia", len(filtered_df[filtered_df["Status"] == "Tersedia"]))
col3.metric("Di Pakai", len(filtered_df[filtered_df["Status"] == "Di Pakai"]))
col4.metric("Rusak", len(filtered_df[filtered_df["Status"] == "Rusak"]))

st.markdown("---")

# Tabel Edit
st.subheader("Data Inventaris")
# Menggunakan data_editor untuk edit langsung
st.session_state.df = st.data_editor(
    st.session_state.df, 
    use_container_width=True,
    num_rows="dynamic"
)

# Chart
st.markdown("---")
st.subheader("Analisis Status")
st.bar_chart(filtered_df["Status"].value_counts())
