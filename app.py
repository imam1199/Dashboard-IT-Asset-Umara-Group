import streamlit as st
import pandas as pd
import os
import plotly.express as px
import io

# Konfigurasi Halaman
st.set_page_config(layout="wide", page_title="IT Asset Umara Group")

FILE_NAME = "laporan laptop terbaru (1).xlsx"

# 1. Load Data
@st.cache_data(ttl=60)
def load_data():
    if os.path.exists(FILE_NAME):
        try:
            df = pd.read_excel(FILE_NAME)
            df.columns = df.columns.str.strip()
            if 'No Aset' in df.columns:
                df['No Aset'] = df['No Aset'].astype(str).replace(['nan', 'None', ''], '-')
            return df.fillna("-")
        except Exception as e:
            st.error(f"Error memuat file: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

if 'df' not in st.session_state:
    st.session_state.df = load_data()

# Fungsi Auto-Save untuk Data Editor
def auto_save():
    st.session_state.df.to_excel(FILE_NAME, index=False, engine='openpyxl')
    st.cache_data.clear()

# Fungsi Generate Nomor Aset
def generate_asset_id(df):
    bu_map = {"UCR": "UCR", "UNB": "UNB", "LBI": "LBI", "RNB": "RNB", "UMK": "UMK"}
    tahun = "26" 
    for index, row in df.iterrows():
        val = str(row.get('No Aset', '-')).strip()
        if val in ["-", "nan", "None"]:
            bu = str(row.get('Bu Owner', '')).strip()
            if bu in bu_map:
                existing = df[(df['Bu Owner'] == bu) & (df['No Aset'].astype(str).str.contains(bu, na=False))]
                count = len(existing) + 1
                df.at[index, 'No Aset'] = f"{bu_map[bu]}-{tahun}-{count:03d}"
    return df

# 2. SIDEBAR
st.sidebar.title("Kontrol Dashboard")
unique_status = ["Semua"] + list(st.session_state.df["Status"].unique())
status_filter = st.sidebar.selectbox("Filter Status:", unique_status, key="status_key")

st.sidebar.markdown("---")
st.sidebar.subheader("Menu Edit & Aset")

if st.sidebar.button("➕ Tambah Baris"):
    new_row = pd.DataFrame([["-"] * len(st.session_state.df.columns)], columns=st.session_state.df.columns)
    st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
    auto_save()
    st.rerun()

if st.sidebar.button("🔢 Generate Nomor Aset"):
    st.session_state.df = generate_asset_id(st.session_state.df)
    auto_save()
    st.rerun()

if st.sidebar.button("🗑️ Hapus Baris Terakhir"):
    if not st.session_state.df.empty:
        st.session_state.df = st.session_state.df.iloc[:-1]
        auto_save()
        st.rerun()

# 3. MAIN DASHBOARD
st.title("📊 Dashboard IT Asset Umara Group")

# Filter Logic
filtered_df = st.session_state.df.copy()
if status_filter != "Semua":
    filtered_df = filtered_df[filtered_df["Status"] == status_filter]

# Metrik & Tombol Download
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total", len(filtered_df))
col2.metric("Tersedia", len(filtered_df[filtered_df["Status"] == "Tersedia"]))
col3.metric("Di Pakai", len(filtered_df[filtered_df["Status"] == "Di Pakai"]))
col4.metric("Rusak", len(filtered_df[filtered_df["Status"] == "Rusak"]))
col5.metric("Perbaikan", len(filtered_df[filtered_df["Status"] == "Perlu Perbaikan"]))

st.markdown("---")

# Tombol Download
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    filtered_df.to_excel(writer, index=False)
buffer.seek(0)

st.download_button(
    label="📥 Download Laporan (Excel)",
    data=buffer,
    file_name="Laporan_IT_Asset_Umara.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Search
search_query = st.text_input("🔍 Cari Laptop...", placeholder="Ketik Model, Serial, User, dll...")
if search_query:
    mask = filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    filtered_df = filtered_df[mask]

# Data Editor dengan Auto-Save
st.subheader("Data Inventaris")
df_edited = st.data_editor(
    filtered_df, use_container_width=True, num_rows="dynamic", key="inventory_editor",
    on_change=auto_save, # Otomatis simpan setiap ada perubahan
    column_config={
        "Status": st.column_config.SelectboxColumn("Status", options=["Tersedia", "Di Pakai", "Rusak", "Perlu Perbaikan"], required=True),
    }
)

if not df_edited.equals(filtered_df):
    st.session_state.df.update(df_edited)
    if len(df_edited) > len(filtered_df):
        st.session_state.df = df_edited

# Chart
st.markdown("---")
col_c1, col_c2 = st.columns(2)
with col_c1:
    fig1 = px.pie(filtered_df, names='Status', hole=0.4, color='Status',
                  color_discrete_map={'Tersedia': '#00CC96', 'Di Pakai': '#636EFA', 'Rusak': '#EF553B', 'Perlu Perbaikan': '#FFA500'})
    st.plotly_chart(fig1, use_container_width=True)
