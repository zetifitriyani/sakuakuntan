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
        kas_masuk = df_filtered[df_filtered["Jenis"] == "Masuk"]["Jumlah"].sum()
        kas_keluar = df_filtered[df_filtered["Jenis"] == "Keluar"]["Jumlah"].sum()
        saldo = kas_masuk - kas_keluar

        st.subheader("📊 Ringkasan Keuangan")
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Kas Masuk", f"Rp {kas_masuk:,.0f}")
        col2.metric("💸 Kas Keluar", f"Rp {kas_keluar:,.0f}")
        col3.metric("🧮 Saldo", f"Rp {saldo:,.0f}")

        # =========================
        # GRAFIK TREN
        # =========================
        st.subheader("📈 Tren Kas Harian")
        daily = df_filtered.groupby(["Tanggal", "Jenis"])["Jumlah"].sum().reset_index()

        fig_trend = px.line(
            daily,
            x="Tanggal",
            y="Jumlah",
            color="Jenis",
            markers=True
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        # =========================
        # PIE CHART
        # =========================
        st.subheader("🧁 Komposisi Kas")
        pie_df = pd.DataFrame({
            "Kategori": ["Kas Masuk", "Kas Keluar"],
            "Jumlah": [kas_masuk, kas_keluar]
        })

        fig_pie = px.pie(
            pie_df,
            names="Kategori",
            values="Jumlah",
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # =========================
        # DATA TABLE
        # =========================
        st.subheader("📄 Detail Transaksi")
        st.dataframe(df_filtered, use_container_width=True)

    except Exception as e:
        st.error(f"Terjadi error: {e}")

else:
    st.info("⬆️ Upload file Excel untuk melihat dashboard")
