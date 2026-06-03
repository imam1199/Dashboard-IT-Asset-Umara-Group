import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")
st.title("💻 Dashboard Inventaris - Umara Group")

FILE_NAME = "laporan laptop terbaru (1).xlsx"

# 1. Load Data
@st.cache_data
def load_data():
    if os.path.exists(FILE_NAME):
        df = pd.read_excel(FILE_NAME)
        return df.fillna("-")
    return pd.DataFrame()

df = load_data()

# 2. EDITING (Gunakan st.data_editor yang resmi dari Streamlit)
st.subheader("Edit Data di Bawah (Klik sel untuk edit):")
df_edited = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# 3. TOMBOL SIMPAN
if st.button("💾 Simpan Perubahan ke Excel"):
    try:
        df_edited.to_excel(FILE_NAME, index=False)
        st.success("Data berhasil disimpan!")
        st.rerun()
    except Exception as e:
        st.error(f"Gagal simpan: {e}. Pastikan file tidak sedang dibuka di Excel!")

# 4. CHART (Otomatis update berdasarkan hasil edit)
st.markdown("---")
st.subheader("Analisis Data")
col1, col2 = st.columns(2)
with col1:
    st.write("Distribusi Status")
    st.bar_chart(df_edited["Status"].value_counts())
with col2:
    st.write("Model Laptop Terbanyak")
    st.bar_chart(df_edited["Model"].value_counts().head(5))
