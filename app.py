import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

@st.cache_resource
def get_gspread_client():
    try:
        # Mengambil dari secrets
        private_key = st.secrets["GCP_PRIVATE_KEY"]
        
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
        # Jika error, tampilkan detail errornya agar kita tahu apa yang terjadi
        st.error(f"Error Auth Detail: {e}")
        return None
