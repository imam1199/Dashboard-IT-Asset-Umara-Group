import streamlit as st
import pandas as pd
import gspread
import plotly.express as px
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(layout="wide")
st.title("📊 Dashboard IT Asset Umara Group")

# Koneksi ke Google Sheets (PENTING: Pastikan Secrets sudah diisi di dashboard Streamlit)
def get_gspread_client():
    creds_dict = st.secrets["gcp_service_account"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

@st.cache_data(ttl=60)
def load_data():
    client = get_gspread_client()
    sheet = client.open_by_key("1msf4IK1ZJReQl5f_6VRbVCsGiJXcHUHENto1DqrQwkY").sheet1
    return pd.DataFrame(sheet.get_all_records())

df = load_data()

# 1. FITUR SEARCH
search = st.text_input("🔍 Cari Aset (berdasarkan Model atau Serial Number):")
if search:
    df = df[df.apply(lambda row: search.lower() in str(row['Model']).lower() or search.lower() in str(row['Serial Number']).lower(), axis=1)]

# 2. DATA EDITOR (Edit, Tambah, Hapus ada di sini)
st.subheader("Data Inventaris")
df_edited = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# 3. TOMBOL SAVE
if st.button("💾 Simpan Perubahan ke Google Sheets"):
    client = get_gspread_client()
    sheet = client.open_by_key("1msf4IK1ZJReQl5f_6VRbVCsGiJXcHUHENto1DqrQwkY").sheet1
    sheet.clear()
    sheet.update([df_edited.columns.values.tolist()] + df_edited.values.tolist())
    st.success("Data berhasil disimpan!")
    st.cache_data.clear()
    st.rerun()

st.markdown("---")

# 4. CHART (Pindah ke bawah)
st.subheader("Visualisasi Data")
col1, col2 = st.columns(2)
with col1:
    fig1 = px.pie(df_edited, names='Status', title="Distribusi Status Aset")
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    fig2 = px.bar(df_edited['Model'].value_counts().head(5), title="Top 5 Model Aset")
    st.plotly_chart(fig2, use_container_width=True)
