import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Fungsi Koneksi
def get_gspread_client():
    creds_dict = st.secrets["gcp_service_account"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

# Ambil data
client = get_gspread_client()
# PASTIIN ID DI BAWAH INI ADALAH ID ASLI SHEET KAMU!
sheet = client.open_by_key("ISI_DENGAN_ID_SHEETS_ASLI_KAMU_DISINI").sheet1 

df = pd.DataFrame(sheet.get_all_records())

st.title("Dashboard IT Asset")
edited_df = st.data_editor(df, num_rows="dynamic")

if st.button("Simpan Perubahan"):
    try:
        # Hapus isi lama
        sheet.clear()
        # Update dengan data baru mulai dari sel A1
        data_to_update = [edited_df.columns.values.tolist()] + edited_df.values.tolist()
        sheet.update(range_name='A1', values=data_to_update)
        st.success("Data berhasil diupdate!")
        st.rerun()
    except Exception as e:
        st.error(f"Gagal simpan: {e}")
