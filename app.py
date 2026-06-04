import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import json

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard IT Asset", layout="wide")

# Fungsi Koneksi pakai file JSON di folder yang sama
def get_gspread_client():
    # Pastikan nama file JSON di bawah sama persis dengan yang kamu upload ke GitHub
    json_keyfile = 'kredensial.json' 
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    return gspread.authorize(creds)

# --- (Sisa kodingan sama seperti yang kemarin) ---
# [Copy kode yang kemarin, tapi di fungsi get_gspread_client gunakan fungsi di atas]
