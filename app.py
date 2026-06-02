import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("laporan laptop terbaru (1).xlsx", sheet_name=0)
    df.columns = df.columns.str.strip()
    return df.fillna("-")

df = load_data()

st.title("💻 Dashboard Laptop Office Pro")

# --- CHART SECTION ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("Distribusi Status")
    st.bar_chart(df["Status"].value_counts())
with col2:
    st.subheader("Top Model Laptop")
    st.bar_chart(df["Model"].value_counts().head(5))

# --- DATA EDITOR (CRUD) ---
st.subheader("Edit Data Inventaris")
st.write("Anda bisa edit data langsung di tabel bawah ini. Perubahan akan tersimpan di sesi ini.")

# Grid Options untuk AgGrid
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(editable=True) # Aktifkan fitur edit
gb.configure_selection('single')
gridOptions = gb.build()

# Tampilkan Grid
grid_response = AgGrid(
    df,
    gridOptions=gridOptions,
    update_mode=GridUpdateMode.VALUE_CHANGED,
    height=400,
    use_container_width=True
)

# Simpan hasil edit
df_updated = pd.DataFrame(grid_response['data'])

# Tombol Tambah & Hapus
col_btn1, col_btn2 = st.columns(2)
if col_btn1.button("Tambah Baris Baru"):
    new_row = pd.DataFrame([["-"] * len(df.columns)], columns=df.columns)
    df = pd.concat([df, new_row], ignore_index=True)
    st.rerun()

import os

if col_btn2.button("Simpan Perubahan ke Excel"):
    file_name = "laporan laptop terbaru (1).xlsx"
    try:
        # Kita buat nama file sementara untuk memastikan data aman sebelum menimpa file asli
        temp_file = "temp_data.xlsx"
        df_updated.to_excel(temp_file, index=False)
        
        # Hapus file lama dan ganti dengan file baru
        if os.path.exists(file_name):
            os.remove(file_name)
        os.rename(temp_file, file_name)
        
        st.success("Data berhasil disimpan!")
        st.rerun() # Refresh dashboard untuk memuat data baru
    except Exception as e:
        st.error(f"Gagal menyimpan: {e}. Pastikan folder tidak di-read only.")
