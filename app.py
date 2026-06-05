import streamlit as st
import gspread
import pandas as pd
import json
from oauth2client.service_account import ServiceAccountCredentials

@st.cache_resource
def get_gspread_client():
    try:
        # Baca JSON langsung dari secrets
        creds_json = json.loads(st.secrets["GCP_JSON"])
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# ... (sisa kodingan sama seperti sebelumnya)
