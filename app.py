import streamlit as st
import pandas as pd
import os
import plotly.express as px
import io

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
        except: return pd.DataFrame()
    return pd.DataFrame()

if 'df' not in st.session_state:
    st.session_state.df = load_data()

def auto_save():
    st.session_state.df.to_excel(FILE_NAME, index=False, engine='openpyxl')
    st.cache_data.clear()

def generate_asset_id(df):
    bu_map = {"UCR": "UCR", "UNB": "UNB", "LBI": "LBI", "RNB": "RNB", "UMK": "UMK"}
    for index, row in df.iterrows():
        val = str(row.get('No Aset', '-')).strip()
        if val in ["-", "nan", "None"]:
            bu = str(row.get('Bu Owner', '')).strip()
            if bu in bu_map:
                existing = df[(df['Bu Owner'] == bu) & (df['No Aset'].astype(str).str.contains(bu, na=False))]
                count = len(existing) + 1
                df.at[index, 'No Aset'] = f"{bu_map[bu]}-26-{count:03d}"
    return df

# 2. SIDEBAR
st.sidebar.title("Kontrol Dashboard")
status_filter = st.sidebar.selectbox("Filter Status:", ["Semua"] + list(st.session_state.df["Status"].unique()))

st.sidebar.subheader("Menu Aset")
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

# Filter & Search
filtered_df = st.session_state.df.copy()
if status_filter != "Semua":
    filtered_df = filtered_df[filtered_df["Status"] == status_filter]

search_query = st.text_input("🔍 Cari Laptop...", placeholder="Ketik Model, Serial, User, dll...")
if search_query:
    mask = filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    filtered_df = filtered_df[mask]

# Metrik
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total", len(filtered_df))
col2.metric("Tersedia", len(filtered_df[filtered_df["Status"] == "Tersedia"]))
col3.metric("Di Pakai", len(filtered_df[filtered_df["Status"] == "Di Pakai"]))
col4.metric("Rusak", len(filtered_df[filtered_df["Status"] == "Rusak"]))
col5.metric("Perlu Perbaikan", len(filtered_df[filtered_df["Status"] == "Perlu Perbaikan"]))

st.markdown("---")

# Data Editor (Auto-Save)
st.subheader("Data Inventaris")
df_edited = st.data_editor(
    filtered_df, use_container_width=True, num_rows="dynamic", key="inventory_editor",
    on_change=auto_save,
    column_config={"Status": st.column_config.SelectboxColumn("Status", options=["Tersedia", "Di Pakai", "Rusak", "Perlu Perbaikan"], required=True)}
)

if not df_edited.equals(filtered_df):
    st.session_state.df.update(df_edited)
    if len(df_edited) > len(filtered_df):
        st.session_state.df = df_edited

# Chart & Download
st.markdown("---")
c1, c2 = st.columns([1, 1])
with c1:
    st.write("**Distribusi Status**")
    fig = px.pie(filtered_df, names='Status', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.write("📥 Ekspor Data")
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as w: filtered_df.to_excel(w, index=False)
    st.download_button("Download Laporan Excel", buffer.getvalue(), "Laporan_Aset.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
