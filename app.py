import streamlit as st
import pandas as pd
import gspread
import plotly.express as px
from oauth2client.service_account import ServiceAccountCredentials

# Pengaturan
SHEET_ID = "1msf4IK1ZJReQl5f_6VRbVCsGiJXcHUHENto1DqrQwkY"

# Fungsi Koneksi
def get_gspread_client():
    creds_dict = st.secrets["gcp_service_account"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

@st.cache_data(ttl=60)
def load_data():
    client = get_gspread_client()
    sheet = client.open_by_key(SHEET_ID).sheet1
    return pd.DataFrame(sheet.get_all_records())

# Tampilan
st.set_page_config(layout="wide")
st.title("📊 Dashboard IT Asset Umara Group")

df = load_data()

# Chart
col1, col2 = st.columns(2)
with col1:
    fig = px.pie(df, names='Status', title="Distribusi Status Aset")
    st.plotly_chart(fig)

# Data Editor (Fitur Edit)
st.subheader("Data Inventaris")
df_edited = st.data_editor(df, num_rows="dynamic")

if st.button("💾 Simpan Perubahan"):
    client = get_gspread_client()
    sheet = client.open_by_key(SHEET_ID).sheet1
    sheet.clear()
    sheet.update([df_edited.columns.values.tolist()] + df_edited.values.tolist())
    st.success("Data berhasil disimpan!")
    st.rerun()
