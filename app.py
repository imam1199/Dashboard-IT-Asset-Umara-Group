import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Pengaturan Google Sheets
SHEET_ID = "1msf4IK1ZJReQl5f_6VRbVCsGiJXcHUHENto1DqrQwkY"

# Fungsi untuk koneksi (Perlu file JSON credentials dari Google Cloud Console)
def get_gspread_client():
    # Catatan: Di Streamlit Cloud, Anda harus menyimpan credential JSON 
    # sebagai "Secrets" di menu dashboard Streamlit Cloud
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    return gspread.authorize(creds)

@st.cache_data(ttl=60)
def load_data():
    client = get_gspread_client()
    sheet = client.open_by_key(SHEET_ID).sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def save_data(df):
    client = get_gspread_client()
    sheet = client.open_by_key(SHEET_ID).sheet1
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())
    st.success("Data tersimpan ke Google Sheets!")
