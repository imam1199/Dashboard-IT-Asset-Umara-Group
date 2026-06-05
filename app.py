import streamlit as st
import gspread
import pandas as pd
from google.oauth2 import service_account

st.set_page_config(page_title="Dashboard IT Asset", layout="wide")

@st.cache_resource
def get_gspread_client():
    try:
        # Gunakan path file JSON yang sudah di-upload ke GitHub
        json_keyfile = 'dashboard-laptop-it-f2733e150461.json'
        
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
        
        # Cara baru yang lebih stabil (menggunakan google-auth)
        creds = service_account.Credentials.from_service_account_file(
            json_keyfile, scopes=scope
        )
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error Auth: {e}")
        return None

st.title("Dashboard IT Asset Umara Group")
client = get_gspread_client()

if client:
    try:
        sheet = client.open_by_key("1msf4IK1ZJReQl5f_6VRbVCsGiJXcHUHENto1DqrQwkY").sheet1
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        
        if st.button("Simpan Perubahan"):
            sheet.clear()
            sheet.update(range_name='A1', values=[edited_df.columns.tolist()] + edited_df.fillna("").values.tolist())
            st.success("Data berhasil disimpan!")
            st.rerun()
    except Exception as e:
        st.error(f"Error saat mengambil data: {e}")
