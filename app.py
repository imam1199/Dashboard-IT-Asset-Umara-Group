import streamlit as st
import pandas as pd
import os

# Konfigurasi Page
st.set_page_config(page_title="Dashboard Inventaris Laptop", layout="wide")

st.title("💻 Dashboard Pendataan Laptop Office")

# Fungsi untuk mencari dan load file otomatis
def load_data():
    # Mencari file yang berakhiran .xlsx
    files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
    if not files:
        st.error("File Excel (.xlsx) tidak ditemukan di folder ini! Pastikan file sudah diupload.")
        return None
    
    # Ambil file pertama yang ketemu
    file_path = files[0]
    st.write(f"Membaca file: **{file_path}**") # Memastikan file apa yang dibaca
    
    df = pd.read_excel(file_path, sheet_name=0) # Membaca sheet pertama
    df.columns = df.columns.str.strip()
    df = df.fillna("-")
    return df

df = load_data()

if df is not None:
    # Sidebar Filter
    status_filter = st.sidebar.multiselect("Pilih Status:", options=df["Status"].unique(), default=df["Status"].unique())
    df_filtered = df[df["Status"].isin(status_filter)]

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Unit", len(df))
    col2.metric("Di Pakai", len(df[df["Status"] == "Di Pakai"]))
    col3.metric("Rusak", len(df[df["Status"] == "Rusak"]))
    col4.metric("Tersedia", len(df[df["Status"] == "Tersedia"]))

    # Tabel
    def highlight_status(row):
        color = 'background-color: #ffcccc' if row['Status'] == 'Rusak' else ('background-color: #fff3cc' if row['Status'] == 'Perlu Perbaikan' else '')
        return [color] * len(row)

    st.subheader("Data Inventaris")
    st.dataframe(df_filtered.style.apply(highlight_status, axis=1), use_container_width=True)
