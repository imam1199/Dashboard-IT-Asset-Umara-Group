import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="IT Asset Umara Group")

# Pastikan link ini benar dan sudah di-Publish to Web
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-aQ2xulUo6MraDS6ohvL6BFFafR-njF45fbnKySxNkbWe12sDQhKr89Oh5k-A1Yy8SfJDPGnVvFKM/pub?output=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip() # Menghapus spasi di nama kolom
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

df = load_data()

st.title("📊 Dashboard IT Asset Umara Group")

if not df.empty and "Status" in df.columns:
    # Sidebar Filter
    status_options = ["Semua"] + list(df["Status"].unique())
    status_filter = st.sidebar.selectbox("Filter Status:", status_options)

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
    st.warning("Data belum berhasil dimuat atau kolom 'Status' tidak ditemukan. Pastikan Google Sheets sudah dipublish dengan benar.")
