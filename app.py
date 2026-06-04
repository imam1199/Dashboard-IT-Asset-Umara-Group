import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="IT Asset Umara Group")

# Link ini didapat dari hasil "Publish to Web" (Entire document, .csv)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-aQ2xulUo6MraDS6ohvL6BFFafR-njF45fbnKySxNkbWe12sDQhKr89Oh5k-A1Yy8SfjDPGnVvFKM/pub?output=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()  # Membersihkan spasi pada nama kolom
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

df = load_data()

st.title("📊 Dashboard IT Asset Umara Group")

# Cek apakah data berhasil dimuat
if not df.empty and "Status" in df.columns:
    # Sidebar Search & Filter
    search = st.sidebar.text_input("🔍 Cari Aset:")
    status_options = ["Semua"] + list(df["Status"].dropna().unique())
    status_filter = st.sidebar.selectbox("Filter Status:", status_options)

    # Filter Data
    filtered_df = df.copy()
    if search:
        filtered_df = filtered_df[filtered_df.apply(lambda row: search.lower() in str(row).lower(), axis=1)]
    if status_filter != "Semua":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]

    # Metrik di atas
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total", len(filtered_df))
    c2.metric("Tersedia", len(filtered_df[filtered_df["Status"] == "Tersedia"]))
    c3.metric("Di Pakai", len(filtered_df[filtered_df["Status"] == "Di Pakai"]))
    c4.metric("Rusak", len(filtered_df[filtered_df["Status"] == "Rusak"]))

    st.subheader("Data Inventaris")
    st.dataframe(filtered_df, use_container_width=True)

    # Chart di bawah
    st.markdown("---")
    st.subheader("Visualisasi")
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.pie(filtered_df, names='Status', title="Distribusi Status Aset")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        if 'Model' in filtered_df.columns:
            fig2 = px.bar(filtered_df['Model'].value_counts().head(5), title="Top 5 Model Aset")
            st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("Data tidak ditemukan. Pastikan link Google Sheets sudah di-publish dengan format CSV.")
