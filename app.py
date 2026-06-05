import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Dashboard IT Asset", layout="wide")

@st.cache_resource
def get_gspread_client():
    try:
        # Kita menggunakan file fisik 'service_account.json' yang ada di folder proyekmu
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        # Membaca file langsung (lebih stabil dari Secrets)
        creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error saat memuat kredensial: {e}")
        return None

st.title("Dashboard IT Asset Umara Group")

client = get_gspread_client()

if client:
    try:
        spreadsheet_id = "1msf4IK1ZJReQl5f_6VRbVCsGiJXcHUHENto1DqrQwkY"
        sheet = client.open_by_key(spreadsheet_id).sheet1
        
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        
        if st.button("Simpan Perubahan"):
            sheet.clear()
            data_to_update = [edited_df.columns.values.tolist()] + edited_df.values.tolist()
            sheet.update(range_name='A1', values=data_to_update)
            st.success("Data berhasil disimpan!")
            st.rerun()
                
    except gspread.exceptions.APIError as e:
        st.error(f"Gagal akses Sheets. Pastikan email Service Account sudah di-Share sebagai Editor ke Sheets tersebut. Pesan: {e}")
    except Exception as e:
        st.error(f"Error tak terduga: {e}")
else:
    st.warning("Client belum siap. Pastikan file 'service_account.json' sudah di-upload ke GitHub.")
