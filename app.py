import streamlit as st
import gspread
import pandas as pd
import os
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Dashboard IT Asset", layout="wide")

@st.cache_resource
def get_gspread_client():
    try:
        # Menentukan path file JSON secara otomatis
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(BASE_DIR, 'dashboard-laptop-it-fe3ec7e15940.json')
        
        # Cek apakah file ditemukan
        if not os.path.exists(json_path):
            st.error(f"File tidak ditemukan di: {json_path}")
            return None
        
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        
        # Membaca credentials dari file
        creds = Credentials.from_service_account_file(json_path, scopes=scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error Auth: {e}")
        return None

st.title("Dashboard IT Asset Umara Group")
client = get_gspread_client()

if client:
    try:
        # Buka sheet
        sheet = client.open_by_key("1msf4IK1ZJReQl5f_6VRbVCsGiJXcHUHENto1DqrQwkY").sheet1
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        
        # Tampilkan editor
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        
        if st.button("Simpan Perubahan"):
            sheet.clear()
            sheet.update(range_name='A1', values=[edited_df.columns.tolist()] + edited_df.fillna("").values.tolist())
            st.success("Data berhasil disimpan!")
            st.rerun()
    except Exception as e:
        st.error(f"Error saat mengambil data: {e}")
