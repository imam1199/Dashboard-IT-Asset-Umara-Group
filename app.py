import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="IT Asset Umara Group")

# Link Google Sheets yang sudah di-Publish (format CSV)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-aQ2xulUo6MraDS6ohvL6BFFafR-njF45fbnKySxNkbWe12sDQhKr89Oh5k-A1Yy8SfjDPGnVvFKM/pub?output=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        # Membaca data langsung dari link CSV publik
        df = pd.read_csv(SHEET_URL)
        # Menghapus spasi di nama kolom agar tidak error saat diakses
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

# Load data
df = load_data()

st.title("📊 Dashboard IT Asset Umara Group")

# Pastikan data tidak kosong sebelum diolah
if not df.empty and "Status" in df.columns:
    # Sidebar Filter
    status_options = ["Semua"] + list(df["Status"].dropna().unique())
    status_filter = st.sidebar.selectbox("Filter Status:", status_options)

    # Filter Data
    filtered_df = df.copy()
    if status_filter != "Semua":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]

    # Metrik
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total", len(filtered_df))
    c2.metric("Tersedia", len(filtered_df[filtered_df["Status"] == "Tersedia"]))
    c3.metric("Di Pakai", len(filtered_df[filtered_df["Status"] == "Di Pakai"]))
    c4.metric("Rusak", len(filtered_df[filtered_df["Status"] == "Rusak"]))

    st.subheader("Data Inventaris")
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.info("Data sedang dimuat atau kolom 'Status' tidak ditemukan. Pastikan link Google Sheets sudah benar.")
