import shutil

def save_data(df):
    try:
        # 1. Simpan ke file sementara dulu
        temp_file = "temp_laporan.xlsx"
        df.to_excel(temp_file, index=False, engine='openpyxl')
        
        # 2. Paksa pindahkan file temp ke file tujuan (ini akan menimpa file lama)
        # Jika cara ini gagal, berarti file sedang benar-benar di-lock oleh Excel desktop
        shutil.move(temp_file, FILE_NAME) 
        
        st.cache_data.clear()
        st.success("Data berhasil disinkronisasi ke Excel!")
    except Exception as e:
        st.error(f"Gagal Simpan! Pastikan Excel tertutup. Error: {e}")

def update_df():
    # Mengambil perubahan dari data_editor
    if st.session_state.inventory_editor["edited_rows"]:
        for idx, row_delta in st.session_state.inventory_editor["edited_rows"].items():
            for col, val in row_delta.items():
                st.session_state.df.at[int(idx), col] = val
        save_data(st.session_state.df)
