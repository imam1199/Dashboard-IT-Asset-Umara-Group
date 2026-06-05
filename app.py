import streamlit as st
import gspread
import pandas as pd
import json
from oauth2client.service_account import ServiceAccountCredentials

@st.cache_resource
def get_gspread_client():
    try:
        # Membaca file JSON langsung dari folder proyek
        # Pastikan nama filenya persis sama
        json_file = 'dashboard-laptop-it-f2733e150461.json'
        
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive',
            'https://spreadsheets.google.com/spreadsheets'
        ]
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error: {e}")
        return None
