import streamlit as st
import pandas as pd
import os
import plotly.express as px

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

# Inisialisasi Session State
if 'df' not in st.session_state:
    st.session_state.df = load_data()

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

# 2. SIDEBAR - Kontrol Dashboard
st.sidebar.title("Kontrol Dashboard")

unique_status = ["Semua"] + list(st.session_state.df["Status"].unique())
status_filter = st.sidebar.selectbox("Filter Status:", unique_status, key="status_key")

st.sidebar.markdown("---")
st.sidebar.subheader("Menu Edit & Aset")

if st.sidebar.button("➕ Tambah Baris"):
    new_row = pd.DataFrame([["-"] * len(st.session_state.df.columns)], columns=st.session_state.df.columns)
    st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
    st.rerun()

if st.sidebar.button("🔢 Generate Nomor Aset"):
    st.session_state.df = generate_asset_id(st.session_state.df)
    st.rerun()

if st.sidebar.button("🗑️ Hapus Baris Terakhir"):
    if not st.session_state.df.empty:
        st.session_state.df = st.session_state.df.iloc[:-1]
        st.rerun()

if st.sidebar.button("💾 Simpan Data"):
    try:
        # Menggunakan engine openpyxl untuk hasil export excel yang rapi
        st.session_state.df.to_excel(FILE_NAME, index=False, engine='openpyxl')
        st.cache_data.clear()
        st.success("Data berhasil disimpan!")
        st.rerun()
    except Exception as e:
        st.error(f"Gagal menyimpan data: {e}")

# 3. FILTER LOGIC
filtered_df = st.session_state.df.copy()

if status_filter != "Semua":
    filtered_df = filtered_df[filtered_df["Status"] == status_filter]

search_query = st.text_input("🔍 Cari Laptop...", placeholder="Ketik Model, Serial, User, dll...")
if search_query:
    mask = filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    filtered_df = filtered_df[mask]

# 4. MAIN DASHBOARD
st.title("📊 Dashboard IT Asset Umara Group")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Unit", len(filtered_df))
col2.metric("Tersedia", len(filtered_df[filtered_df["Status"] == "Tersedia"]))
col3.metric("Di Pakai", len(filtered_df[filtered_df["Status"] == "Di Pakai"]))
col4.metric("Rusak", len(filtered_df[filtered_df["Status"] == "Rusak"]))
col5.metric("Perlu Perbaikan", len(filtered_df[filtered_df["Status"] == "Perlu Perbaikan"]))

st.markdown("---")

st.subheader("Data Inventaris")
df_edited = st.data_editor(
    filtered_df, 
    use_container_width=True, 
    num_rows="dynamic",
    key="inventory_editor",
    column_config={
        "Status": st.column_config.SelectboxColumn(
            "Status",
            options=["Tersedia", "Di Pakai", "Rusak", "Perlu Perbaikan"],
            required=True,
        ),
        "Notes": st.column_config.TextColumn("Notes", width="large"),
        "No Aset": st.column_config.TextColumn("No Aset", width="small")
    }
)

if not df_edited.equals(filtered_df):
    st.session_state.df.update(df_edited)
    if len(df_edited) > len(filtered_df):
        st.session_state.df = df_edited

# 5. CHART BERDAMPINGAN
st.markdown("---")
st.subheader("📊 Analisis Data Visual")
col_c1, col_c2 = st.columns(2)

with col_c1:
    st.write("**Distribusi Status Laptop**")
    fig1 = px.pie(filtered_df, names='Status', hole=0.4, 
                  color='Status',
                  color_discrete_map={'Tersedia': '#00CC96', 
                                      'Di Pakai': '#636EFA', 
                                      'Rusak': '#EF553B', 
                                      'Perlu Perbaikan': '#FFA500'}) 
    fig1.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
    st.plotly_chart(fig1, use_container_width=True)

with col_c2:
    st.write("**Top 5 Model Laptop Terbanyak**")
    if 'Model' in filtered_df.columns:
        # Filter agar tidak menghitung baris kosong "-"
        df_plot = filtered_df[filtered_df['Model'] != "-"]
        top_models = df_plot['Model'].value_counts().head(5).reset_index()
        top_models.columns = ['Model', 'Jumlah']
        fig2 = px.bar(top_models, x='Jumlah', y='Model', orientation='h', color='Jumlah', color_continuous_scale='Blues')
        fig2.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Kolom 'Model' tidak ditemukan.")
