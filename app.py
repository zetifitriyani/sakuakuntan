import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="💼 SakuAkuntan", layout="wide")

st.title("💼 SakuAkuntan Dashboard")
st.caption("Dashboard Keuangan Kas Masuk & Keluar")

uploaded_file = st.file_uploader(
    "📂 Upload file Excel Kas",
    type=["xlsx", "xls", "csv"]
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Validasi kolom
        required_cols = ["Tanggal", "Keterangan", "Jenis", "Jumlah"]
        if not all(col in df.columns for col in required_cols):
            st.error("Kolom Excel harus: Tanggal, Keterangan, Jenis, Jumlah")
            st.stop()

        df["Tanggal"] = pd.to_datetime(df["Tanggal"])
        df["Jumlah"] = df["Jumlah"].astype(float)

        # =========================
        # FILTER BULAN
        # =========================
        df["Bulan"] = df["Tanggal"].dt.strftime("%Y-%m")
        bulan_list = df["Bulan"].unique()
        selected_bulan = st.selectbox("📅 Pilih Bulan", bulan_list)

        df_filtered = df[df["Bulan"] == selected_bulan]

        # =========================
        # METRICS
        # =========================
        kas_masuk = df_filtered[df_filtered_]()
