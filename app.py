import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Dashboard IT Asset", layout="wide")

@st.cache_resource
def get_gspread_client():
    try:
        # Mengambil key dari secrets dan memperbaiki format \n
        raw_key = st.secrets["GCP_PRIVATE_KEY"]
        private_key = raw_key.replace("\\n", "\n")
        
        creds_dict = {
            "type": "service_account",
            "project_id": "dashboard-laptop-it",
            "private_key_id": "f2733e150461a3dacf6af401943b3dafbe098bf4",
            "private_key": private_key, 
            "client_email": "dashboard-it-asset@dashboard-laptop-it.iam.gserviceaccount.com",
            "client_id": "112552009541399448470",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dashboard-it-asset%40dashboard-laptop-it.iam.gserviceaccount.com"
        }
        
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
            sheet.update(range_name='A1', values=[edited_df.columns.tolist()] + edited_df.fillna("").values.tolist())
            st.success("Data berhasil disimpan!")
            st.rerun()
    except Exception as e:
        st.error(f"Error saat mengambil data: {e}")
else:
    st.warning("Gagal terhubung. Pastikan email Service Account sudah di-Share sebagai Editor di Google Sheets.")
