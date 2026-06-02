import streamlit as st
import pandas as pd

# Konfigurasi Page
st.set_page_config(page_title="Dashboard Inventaris Laptop", layout="wide")

# Judul Dashboard
st.title("💻 Dashboard Pendataan Laptop Office")
st.write("Pantau status inventaris laptop kantor secara real-time.")

# Fungsi Load Data
@st.cache_data
def load_data():
    df = pd.read_excel("laporan laptop terbaru (1).xlsx", sheet_name='laporan laptop')
    df.columns = df.columns.str.strip() # Bersihkan spasi di nama kolom
    df = df.fillna("-") # Mengganti nilai kosong dengan "-"
    return df

df = load_data()

# Sidebar untuk Filter
st.sidebar.header("Filter Data")
status_filter = st.sidebar.multiselect(
    "Pilih Status:", 
    options=df["Status"].unique(), 
    default=df["Status"].unique()
)

# Filter data berdasarkan pilihan
df_filtered = df[df["Status"].isin(status_filter)]

# Tampilan Ringkasan (Metrics)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Unit", len(df))
col2.metric("Di Pakai", len(df[df["Status"] == "Di Pakai"]))
col3.metric("Rusak", len(df[df["Status"] == "Rusak"]))
col4.metric("Tersedia", len(df[df["Status"] == "Tersedia"]))

# Fungsi untuk Highlight Baris
def highlight_status(row):
    color = ''
    if row['Status'] == 'Rusak':
        color = 'background-color: #ffcccc' # Merah muda
    elif row['Status'] == 'Perlu Perbaikan':
        color = 'background-color: #fff3cc' # Kuning muda
    return [color] * len(row)

# Tampilkan Tabel
st.subheader("Data Inventaris")
columns_to_show = ["Model", "Serial Number", "Status", "User", "Notes"]
st.dataframe(
    df_filtered[columns_to_show].style.apply(highlight_status, axis=1), 
    use_container_width=True
)

# Tombol Download
st.subheader("Ekspor Data")
csv = df_filtered.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Download Data Terfilter (CSV)",
    data=csv,
    file_name='laporan_laptop_terbaru.csv',
    mime='text/csv',
)
