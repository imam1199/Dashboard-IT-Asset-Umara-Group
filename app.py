import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard IT Asset", layout="wide")

# Fungsi Koneksi ke Google Sheets
def get_gspread_client():
    creds_dict = st.secrets["gcp_service_account"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

st.title("Dashboard IT Asset Umara Group")
st.markdown("---")

# 1. Opsi Upload Manual (Backup)
st.subheader("Opsi Upload File (Jika koneksi Sheets error)")
uploaded_file = st.file_uploader("Upload file Excel (.xlsx)", type=["xlsx"])

# 2. Logika Pemanggilan Data
df = None

if uploaded_file is not None:
    # Mode Upload
    df = pd.read_excel(uploaded_file)
    st.info("Menggunakan data dari file yang di-upload.")
else:
    # Mode Google Sheets
    try:
        client = get_gspread_client()
        # GANTI ID INI DENGAN ID GOOGLE SHEET ASLI KAMU!
        SHEET_ID = "1msf4IK1ZJReQl5f_6VRbVCsGiJXcHUHENto1DqrQwkY"
        sheet = client.open_by_key(SHEET_ID).sheet1 
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        st.success("Berhasil terhubung ke Google Sheets!")
    except Exception as e:
        st.error(f"Belum bisa terhubung ke Sheets: {e}")
        st.warning("Silakan upload file Excel di atas untuk mulai mengedit.")

# 3. Menampilkan dan Mengedit Data
if df is not None:
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    if st.button("Simpan Perubahan"):
        if uploaded_file is None:
            # Simpan balik ke Google Sheets
            try:
                sheet.clear()
                data_to_update = [edited_df.columns.values.tolist()] + edited_df.values.tolist()
                sheet.update(range_name='A1', values=data_to_update)
                st.success("Data berhasil diupdate ke Google Sheets!")
                st.rerun()
            except Exception as e:
                st.error(f"Gagal simpan ke Sheets: {e}")
        else:
            st.warning("Perubahan tidak tersimpan permanen (mode upload).")
