import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Konfigurasi
st.set_page_config(page_title="Dashboard IT Asset", layout="wide")

# Fungsi koneksi yang aman dari Secrets
def get_gspread_client():
    # Mengambil dict dari st.secrets
    creds_dict = st.secrets["gcp_service_account"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

st.title("Dashboard IT Asset Umara Group")

# --- Logika Data ---
try:
    client = get_gspread_client()
    sheet = client.open_by_key("1msf4IK1ZJReQl5f_6VRbVCsGiJXcHUHENto1DqrQwkY").sheet1
    df = pd.DataFrame(sheet.get_all_records())
    
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    if st.button("Simpan Perubahan"):
        sheet.clear()
        # Mengubah dataframe ke list of lists
        data_to_update = [edited_df.columns.values.tolist()] + edited_df.values.tolist()
        sheet.update(range_name='A1', values=data_to_update)
        st.success("Data berhasil disimpan!")
        st.rerun()

except Exception as e:
    st.error(f"Terjadi kesalahan koneksi. Pastikan Secrets sudah benar. Detail: {e}")
