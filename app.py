import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="IT Asset Umara Group")

# Link hasil Publish to Web Anda
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-aQ2xulUo6MraDS6ohvL6BFFafR-njF45fbnKySxNkbWe12sDQhKr89Oh5k-A1Yy8SfJDPGnVvFKM/pub?output=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        # Membaca data langsung dari link CSV publik
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        return df.fillna("-")
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

# Load data
df = load_data()

# 2. SIDEBAR
st.sidebar.title("Kontrol Dashboard")
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

status_filter = st.sidebar.selectbox("Filter Status:", ["Semua"] + list(df["Status"].unique()))

# 3. MAIN DASHBOARD
st.title("📊 Dashboard IT Asset Umara Group")

filtered_df = df.copy()
if status_filter != "Semua":
    filtered_df = filtered_df[filtered_df["Status"] == status_filter]

# Metrik
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total", len(filtered_df))
col2.metric("Tersedia", len(filtered_df[filtered_df["Status"] == "Tersedia"]))
col3.metric("Di Pakai", len(filtered_df[filtered_df["Status"] == "Di Pakai"]))
col4.metric("Rusak", len(filtered_df[filtered_df["Status"] == "Rusak"]))
col5.metric("Perbaikan", len(filtered_df[filtered_df["Status"] == "Perlu Perbaikan"]))

st.markdown("---")

# Menampilkan Data
st.subheader("Data Inventaris")
st.dataframe(filtered_df, use_container_width=True)

# 4. CHART
st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    fig1 = px.pie(filtered_df, names='Status', hole=0.4)
    st.plotly_chart(fig1, use_container_width=True)
with c2:
    if 'Model' in filtered_df.columns:
        fig2 = px.bar(filtered_df['Model'].value_counts().head(5), orientation='h')
        st.plotly_chart(fig2, use_container_width=True)
