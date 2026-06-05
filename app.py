import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# Nama file JSON yang kamu upload ke folder GitHub
JSON_FILE = 'dashboard-laptop-it-fe3ec7e15940.json'

@st.cache_resource
def get_gspread_client():
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        # Membaca file JSON langsung dari sistem
        creds = Credentials.from_service_account_file(JSON_FILE, scopes=scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error Auth: {e}")
        return None

st.title("Dashboard IT Asset Umara Group")
client = get_gspread_client()

if client:
    try:
        # Ganti dengan ID Google Sheet kamu
        sheet = client.open_by_key("1msf4IK1ZJReQl5f_6VRbVCsGiJXcHUHENto1DqrQwkY").sheet1
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        
        st.data_editor(df, num_rows="dynamic", use_container_width=True)
    except Exception as e:
        st.error(f"Error saat mengambil data: {e}")
