import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import os

st.set_page_config(page_title="Dashboard Inventaris IT", layout="wide")
st.title("💻 Dashboard Inventaris Laptop - Umara Group")

FILE_NAME = "laporan laptop terbaru (1).xlsx"

@st.cache_data
def load_data():
    if not os.path.exists(FILE_NAME):
        return None
    df = pd.read_excel(FILE_NAME, sheet_name=0)
    df.columns = df.columns.str.strip()
    return df.fillna("-")

df = load_data()

if df is not None:
    # --- 1. TABEL DENGAN TOMBOL EDIT/TAMBAH/HAPUS ---
    st.subheader("Data Inventaris")
    
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True) 
    gb.configure_selection('multiple', use_checkbox=True) # Aktifkan checkbox untuk hapus
    gridOptions = gb.build()

    grid_response = AgGrid(df, gridOptions=gridOptions, update_mode=GridUpdateMode.VALUE_CHANGED, height=300)
    df_updated = pd.DataFrame(grid_response['data'])

    # Tombol Aksi
    col_a, col_b, col_c = st.columns(3)
    
    if col_a.button("➕ Tambah Baris"):
        new_row = pd.DataFrame([["-"] * len(df.columns)], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_excel(FILE_NAME, index=False)
        st.rerun()

    if col_b.button("🗑️ Hapus Baris Terpilih"):
        selected = grid_response['selected_rows']
        if selected:
            indices = [row['_selectedRowNodeInfo']['nodeRowIndex'] for row in selected]
            df = df.drop(indices).reset_index(drop=True)
            df.to_excel(FILE_NAME, index=False)
            st.rerun()
            
    if col_c.button("💾 Simpan Perubahan"):
        df_updated.to_excel(FILE_NAME, index=False)
        st.success("Data tersimpan!")
        st.rerun()

    # --- 2. CHART SECTION (DIPINDAHKAN KE BAWAH) ---
    st.markdown("---")
    st.subheader("Analisis Data (Chart)")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Distribusi Status")
        st.bar_chart(df_updated["Status"].value_counts())
    with col2:
        st.write("Model Laptop Terbanyak")
        st.bar_chart(df_updated["Model"].value_counts().head(10))
