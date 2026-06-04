import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# 1. Konfigurasi Halaman (Harus di baris paling atas setelah import)
st.set_page_config(page_title="Dashboard IT Asset", layout="wide")

# 2. Fungsi Koneksi ke Google Sheets
def get_gspread_client():
    # Mengambil kredensial dari Secrets Streamlit
    creds_dict = st.secrets["gcp_service_account"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

# 3. Main Logic
st.title("Dashboard IT Asset Umara Group")
st.markdown("---")

try:
    # Inisialisasi client
    client = get_gspread_client()
    
    # GANTI DENGAN ID GOOGLE SHEET ASLI KAMU (diambil dari URL setelah /d/ dan sebelum /edit)
    SHEET_ID = "1msf4IK1ZJReQl5f_6VRbVCsGiJXcHUHENto1DqrQwkY"
    sheet = client.open_by_key(SHEET_ID).sheet1 

    # Ambil data
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # 4. Fitur Edit Data (Dynamic)
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    # 5. Tombol Simpan
    if st.button("Simpan Perubahan ke Google Sheets"):
        with st.spinner('Sedang menyimpan ke server...'):
            try:
                # Membersihkan sheet dan update dengan data baru
                sheet.clear()
                # Gabungkan header kolom dan isi data
                data_to_update = [edited_df.columns.values.tolist()] + edited_df.values.tolist()
                sheet.update(range_name='A1', values=data_to_update)
                
                st.success("Data berhasil diupdate!")
                st.rerun() # Refresh halaman untuk memuat data terbaru
            except Exception as e:
                st.error(f"Gagal menyimpan data: {e}")

except Exception as e:
    st.error(f"Gagal terhubung ke Google Sheets. Pastikan ID benar & Service Account sudah di-Share ke Google Sheets sebagai Editor. Detail: {e}")
