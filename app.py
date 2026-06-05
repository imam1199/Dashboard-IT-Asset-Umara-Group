import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Dashboard IT Asset", layout="wide")

@st.cache_resource
def get_gspread_client():
    try:
        # Mengambil dari secrets yang sudah kita buat tadi
        creds_dict = dict(st.secrets["gcp"])
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
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
            sheet.update(range_name='A1', values=[edited_df.columns.tolist()] + edited_df.values.tolist())
            st.success("Data berhasil disimpan!")
            st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Gagal terhubung ke Google Sheet. Pastikan Email Service Account sudah di-Share sebagai Editor.")
