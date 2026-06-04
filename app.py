import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard IT Asset", layout="wide")

# Fungsi Koneksi ke Google Sheets
def get_gspread_client():
    # Mengambil kredensial dari Streamlit Secrets
    creds_dict = st.secrets["gcp_service_account"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

# --- UTAMA ---
try:
    client = get_gspread_client()
    # GANTI ID DI BAWAH INI DENGAN ID GOOGLE SHEET ASLI KAMU
    # Contoh ID: 1msf4IK1ZJReQl5f_6VRbVCsGiJXcHUHENto1DqrQwkY
    SHEET_ID = "1msf4IK1ZJReQl5f_6VRbVCsGiJXcHUHENto1DqrQwkY" 
    sheet = client.open_by_key(SHEET_ID).sheet1 

    # Ambil data
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    st.title("Dashboard IT Asset Umara Group")
    st.markdown("---")

    # Fitur Edit Data
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    # Tombol Simpan
    if st.button("Simpan Perubahan ke Google Sheets"):
        with st.spinner('Sedang menyimpan...'):
            try:
                # Hapus isi sheet dan update dengan data baru
                sheet.clear()
                # Menggabungkan header dan data
                data_to_update = [edited_df.columns.values.tolist()] + edited_df.values.tolist()
                sheet.update(range_name='A1', values=data_to_update)
                st.success("Data berhasil diupdate ke Google Sheets!")
                st.rerun()
            except Exception as e:
                st.error(f"Gagal menyimpan data: {e}")

except Exception as e:
    st.error(f"Koneksi ke Google Sheets gagal. Pastikan ID benar dan akses sudah diberikan ke service account. Detail: {e}")
