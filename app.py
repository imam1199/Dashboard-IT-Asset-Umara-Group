import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(layout="wide", page_title="IT Asset Umara Group")

FILE_NAME = "laporan laptop terbaru (1).xlsx"

# 1. Load Data dengan pembersihan nama kolom
@st.cache_data
def load_data():
    if os.path.exists(FILE_NAME):
        df = pd.read_excel(FILE_NAME)
        # Menghapus spasi di depan/belakang nama kolom agar tidak KeyError
        df.columns = df.columns.str.strip() 
        # Pastikan kolom No Aset dibaca sebagai string
        if 'No Aset' in df.columns:
            df['No Aset'] = df['No Aset'].astype(str).replace(['nan', 'None', ''], '-')
        return df.fillna("-")
    return pd.DataFrame()

if 'df' not in st.session_state:
    st.session_state.df = load_data()

# Fungsi Generate Nomor Aset
def generate_asset_id(df):
    bu_map = {"UCR": "UCR", "UNB": "UNB", "LBI": "LBI", "RNB": "RNB", "UMK": "UMK"}
    tahun = "26" 
    for index, row in df.iterrows():
        val = str(row.get('No Aset', '-')).strip()
        if val == "-" or val == "nan" or val == "None":
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

# 3. FILTER LOGIC
if status_filter == "Semua":
    filtered_df = st.session_state.df
else:
    filtered_df = st.session_state.df[st.session_state.df["Status"] == status_filter]

# 4. MAIN DASHBOARD
st.title("📊 Dashboard IT Asset Umara Group")

# Metrik
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Unit", len(filtered_df))
col2.metric("Tersedia", len(filtered_df[filtered_df["Status"] == "Tersedia"]))
col3.metric("Di Pakai", len(filtered_df[filtered_df["Status"] == "Di Pakai"]))
col4.metric("Rusak", len(filtered_df[filtered_df["Status"] == "Rusak"]))

st.markdown("---")

# Tabel Edit
st.subheader("Data Inventaris")
df_edited = st.data_editor(filtered_df, use_container_width=True, num_rows="dynamic")

if not df_edited.equals(filtered_df):
    st.session_state.df.update(df_edited)

# 5. CHART BERDAMPINGAN (DENGAN PENGECEKAN KOLOM)
st.markdown("---")
st.subheader("📊 Analisis Data Visual")

col_c1, col_c2 = st.columns(2)

# Chart 1: Status
with col_c1:
    st.write("**Distribusi Status Laptop**")
    fig1 = px.pie(filtered_df, names='Status', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    fig1.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Model (Ditambahkan pengecekan apakah kolom 'Model' ada)
with col_c2:
    st.write("**Top 5 Model Laptop Terbanyak**")
    if 'Model' in filtered_df.columns:
        top_models = filtered_df['Model'].value_counts().head(5).reset_index()
        top_models.columns = ['Model', 'Jumlah']
        fig2 = px.bar(top_models, x='Jumlah', y='Model', orientation='h', color='Jumlah', color_continuous_scale='Blues')
        fig2.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Kolom 'Model' tidak ditemukan di file Excel.")
