import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

FILE_NAME = "laporan laptop terbaru (1).xlsx"

# 1. Load Data
@st.cache_data
def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_excel(FILE_NAME).fillna("-")
    return pd.DataFrame()

if 'df' not in st.session_state:
    st.session_state.df = load_data()

# 2. SIDEBAR (FILTER & TOMBOL FUNGSI)
st.sidebar.title("Kontrol Dashboard")

# Filter
unique_status = ["Semua"] + list(st.session_state.df["Status"].unique())
status_filter = st.sidebar.selectbox("Filter Status:", unique_status, key="status_key")

st.sidebar.markdown("---")
st.sidebar.subheader("Menu Edit Data")

# Tombol Tambah, Hapus, Simpan di Sidebar
if st.sidebar.button("➕ Tambah Baris Baru"):
    new_row = pd.DataFrame([["-"] * len(st.session_state.df.columns)], columns=st.session_state.df.columns)
    st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
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
st.session_state.df = st.data_editor(
    st.session_state.df, 
    use_container_width=True,
    num_rows="dynamic"
)

# Chart
st.markdown("---")
st.subheader("Analisis Status")
st.bar_chart(filtered_df["Status"].value_counts())
