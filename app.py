import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Inventaris IT", layout="wide")
st.title("💻 Dashboard Inventaris Laptop - Umara Group")

# Nama file
FILE_NAME = "laporan laptop terbaru (1).xlsx"

# Fungsi Load Data
@st.cache_data
def load_data():
    if not os.path.exists(FILE_NAME):
        st.error(f"File {FILE_NAME} tidak ditemukan!")
        return None
    df = pd.read_excel(FILE_NAME, sheet_name=0)
    df.columns = df.columns.str.strip()
    return df.fillna("-")

df = load_data()

if df is not None:
    # 1. CHART SECTION
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribusi Status")
        status_counts = df["Status"].value_counts()
        st.bar_chart(status_counts)
    with col2:
        st.subheader("Model Laptop Terbanyak")
        model_counts = df["Model"].value_counts().head(10)
        st.bar_chart(model_counts)

    # 2. CRUD SECTION (AgGrid)
    st.subheader("Data Inventaris (Edit Langsung)")
    
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True) # Aktifkan fitur edit di semua kolom
    gb.configure_selection('single')
    gridOptions = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        height=400,
        use_container_width=True
    )

    df_updated = pd.DataFrame(grid_response['data'])

    # 3. TOMBOL TAMBAH & SIMPAN
    col_btn1, col_btn2 = st.columns(2)
    
    if col_btn1.button("➕ Tambah Baris Baru"):
        new_row = pd.DataFrame([["-"] * len(df.columns)], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
        st.rerun()

    if col_btn2.button("💾 Simpan Perubahan"):
        try:
            df_updated.to_excel(FILE_NAME, index=False)
            st.success("Data berhasil disimpan ke Excel!")
            st.rerun()
        except Exception as e:
            st.error(f"Gagal simpan: {e}. Pastikan file Excel tidak sedang terbuka!")
