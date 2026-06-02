import streamlit as st
import pandas as pd

# Konfigurasi Page
st.set_page_config(page_title="Dashboard Aset Laptop", layout="wide")

st.title("💻 Dashboard Pendataan Laptop Office")
st.write("Pantau status inventaris laptop kantor secara real-time.")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_excel("laporan laptop terbaru (1).xlsx", sheet_name='laporan laptop')
    df.columns = df.columns.str.strip() # Bersihkan spasi di nama kolom
    return df

df = load_data()

# Sidebar untuk Filter
st.sidebar.header("Filter Data")
status_filter = st.sidebar.multiselect("Pilih Status:", options=df["Status"].unique(), default=df["Status"].unique())

# Filter data berdasarkan pilihan
df_filtered = df[df["Status"].isin(status_filter)]

# Tampilan Ringkasan (Metrics)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Unit", len(df))
col2.metric("Di Pakai", len(df[df["Status"] == "Di Pakai"]))
col3.metric("Rusak", len(df[df["Status"] == "Rusak"]))
col4.metric("Tersedia", len(df[df["Status"] == "Tersedia"]))

# Tampilkan Tabel
st.subheader("Data Inventaris")
st.dataframe(df_filtered, use_container_width=True)

# Visualisasi Sederhana
st.subheader("Distribusi Status Laptop")
st.bar_chart(df["Status"].value_counts())