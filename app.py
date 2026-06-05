import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Dashboard IT Asset", layout="wide")

@st.cache_resource
def get_gspread_client():
    try:
        # Menggunakan nama file langsung dari folder proyek
        # Pastikan nama file ini SAMA PERSIS dengan file di folder GitHub
        json_keyfile = 'dashboard-laptop-it-f2733e150461.json'
        
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive',
            'https://spreadsheets.google.com/spreadsheets'
        ]
        
        # Menggunakan metode yang membaca file langsung
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error saat inisialisasi client: {e}")
        return None

st.title("Dashboard IT Asset Umara Group")
client = get_gspread_client()

if client:
    try:
        # Membuka sheet berdasarkan ID
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
else:
    st.warning("Client tidak ditemukan. Pastikan file .json ada di folder yang benar.")
