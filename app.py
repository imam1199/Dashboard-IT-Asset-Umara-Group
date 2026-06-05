import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Dashboard IT Asset", layout="wide")

@st.cache_resource
def get_gspread_client():
    try:
        # Kita gunakan dictionary untuk mengonfigurasi kredensial
        creds_dict = {
            "type": "service_account",
            "project_id": "dashboard-laptop-it",
            "private_key_id": "1c1c634485655a799638c741b62fb705521e7f8e",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQC/INPp9AvnIUnCNTXz3gFKQQSwM8quOOU/U2PEshvaoWdthMqiMwIqr67gaIHs9uPeWgcE1z81qlWSC5wWx8bgC9DLII5ci5CsUGMKFRKBEbQuZSxiNYF7Mb/V207isL3NTI/RsKKTLnS28jBNfl5K7nBCxNzol2RlYH4xUF8yj+tIiY1R10+azfM/An4Yv8fNHqX3JmPxs8yQe6pT89J3Cp5Xudp4NpEJRSHtfPPL0mP8p3HAqYAQ5PI3wMcmk8q1uNfThkdNsKm5f5K82I5CgTrE1CD6fRZ9al+HPf+dEdhU/tvHT6vrzv+QCrbKeUAmRp+UP5DPG5Nw4awTlYxNAgMBAAECggEABn8WwbFnF8VMsB2fs3K5iuaVQpzGdNy/0ULQwoZmf/kgfnTj1la/6hq5A2B9M6rCQ0DxubsydAaE8uCsi4tHoHHsxOeN/ANNny3HgzfRvmVcDhlBd8BN1S9ZtlEsznPBEwTyybPXstA102Ow1J5I+88JYQIEAdWAUIA5I3MrgswAFc6zw04QJtKvuZc4FcJe0imITvO2Y9zhXaAjuF83ml6Qr5YaQBSp38lliETCPMIiG7+uDpb5Ie/DdfszXQF07YuN4Sm9Y7mKf++6qZRqBzmDHBgE7Do4YW+Zxy6hH+RqIIt6mIja1rBdfnAeQQegWzuBLAMVvqlVwb/vGgPtmQKBgQDgUc7bxwVHMxaBhP+QQir8kMtKkyh0D22EQZpB9oeVqnhTLk8eLdVeAhwvNCIUIFhuWj6TxpRvYVQWZaxIQ0heg8dnjtwJZV3njoqpcvbB3St1dr2qaUnf5+yxI5oYXwEfOIhypjdEcncabbq1AOURoavrBR8B1Lv/YovQO3tElwKBgQDa92iHZt4rWgjStt9o2yBjrEY+o70A8GXTeOd09RZUMwVogPPiVe47Sfj5IeU8ELHiKZYLrWYLZ6l9Qia6v0C2NneJGvkKO8zIGVTCd+p+VMfCLWGd81rIbeMLZ4qMUif1kVE3cYSjAWSWlbSXcNhszHi0Oq8BK9mugpFmrhn6AwKBgQDvSnb7BWzDNo4Dym823NBUX9F7xHj2OVI215YakwS3k22fexXd8HFzjya7toF1/NzdU5YRrxZGn9IQZvMPZ4MgjJvM5RsDkyvgxLFIxrwlZ7DiTReF3gU3+PK5WDcl3SleTXfAbJ9R6xJyU+y4Awl9f4YlBo3nMkpTjvf+EGLQAQKBgQCCEqRagsYJdKN3IMEYFctoyka0ISo+a4/hjpnYBVttSx20VZ4K3sb1G102CWeWRciVs+R5LVlH/x1U1j4Rg1kapMJfhNFZvepJF5sdJoT65LwBYlnxrUVJeNV9ydUoxAkOvHNFfz6uYj5xoZ60s4ktIE23qoCZLoZSPyfGmje+JwKBgQDEP7voD5lTHSOUsDRX2L/xM5KIuk/tpnm5eM7rxV8qJWiEnyiv1BXgudxKy1CqiGNbClP6kdrccTLJrzbKxR10kZRlBTDu3kY9r9W5IBB8Evfs/y2tq0qkmjnS7rTZhAT/vo+UULTnM3PntNdYaq9kQMlPcdoE7P0gHxj4NhhYHg==\n-----END PRIVATE KEY-----",
            "client_email": "dashboard-it-asset@dashboard-laptop-it.iam.gserviceaccount.com",
            "client_id": "112552009541399448470",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dashboard-it-asset%40dashboard-laptop-it.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        }
        
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
        # Menggunakan from_json_keyfile_dict untuk membaca langsung dari dictionary
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error Auth: {e}")
        return None

st.title("Dashboard IT Asset Umara Group")
client = get_gspread_client()

if client:
    try:
        sheet = client.open_by_key("1msf4IK1ZJReQl5f_6VRbVCsGiJXcHUHENto1DqrQwkY").sheet1
        data = sheet.get_all_records()
        if data:
            df = pd.DataFrame(data)
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
            if st.button("Simpan Perubahan"):
                sheet.clear()
                sheet.update(range_name='A1', values=[edited_df.columns.tolist()] + edited_df.values.tolist())
                st.success("Data tersimpan!")
                st.rerun()
        else:
            st.info("Sheet kosong.")
    except Exception as e:
        st.error(f"Error Sheets: {e}")
else:
    st.warning("Client gagal dibuat. Pastikan kodingan sudah benar.")
