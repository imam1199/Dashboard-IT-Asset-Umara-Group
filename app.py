import streamlit as st
import pandas as pd
import plotly.express as px

# Pengaturan Halaman
st.set_page_config(layout="wide", page_title="IT Asset Umara Group")

# Link CSV dari Publish to Web
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-aQ2xulUo6MraDS6ohvL6BFFafR-njF45fbnKySxNkbWe12sDQhKr89Oh5k-A1Yy8SfjDPGnVvFKM/pub?output=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# Judul
st.title("📊 Dashboard IT Asset Umara Group")

# 1. CHART STATUS (PIE CHART)
if "Status" in df.columns:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribusi Status Aset")
        fig_status = px.pie(df, names='Status')
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        st.subheader("Model Aset Terbanyak")
        # Menghitung 5 model terbanyak
        model_counts = df['Model'].value_counts().head(5).reset_index()
        fig_model = px.bar(model_counts, x='count', y='Model', orientation='h')
        st.plotly_chart(fig_model, use_container_width=True)

# 2. DATA TABLE
st.subheader("Data Inventaris")
# Kita gunakan dataframe biasa karena CSV bersifat Read-Only
st.dataframe(df, use_container_width=True)
