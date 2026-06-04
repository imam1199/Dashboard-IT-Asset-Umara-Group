import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# 1. Fungsi Koneksi
def get_gspread_client():
    creds_dict = st.secrets["gcp_service_account"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

# 2. Ambil data
client = get_gspread_client()
sheet = client.open_by_key("ID_GOOGLE_SHEETS_KAMU").sheet1 # Cari ID di URL Sheets
df = pd.DataFrame(sheet.get_all_records())

# 3. Fitur Edit
st.title("Dashboard IT Asset")
edited_df = st.data_editor(df, num_rows="dynamic")

# 4. Tombol Simpan
if st.button("Simpan Perubahan"):
    sheet.clear()
    sheet.update([edited_df.columns.values.tolist()] + edited_df.values.tolist())
    st.success("Data berhasil diupdate!")
    st.rerun()
