import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="💼 SakuAkuntan AI", layout="wide")

st.title("💼 SakuAkuntan Dashboard")
st.caption("Dashboard Akuntansi + Analisis Keuangan Otomatis")

uploaded_file = st.file_uploader(
    "📂 Upload file Excel Kas",
    type=["xlsx", "xls", "csv"]
)

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        required_cols = ["Tanggal", "Keterangan", "Jenis", "Kategori", "Jumlah"]
        if not all(col in df.columns for col in required_cols):
            st.error("Kolom wajib: Tanggal, Keterangan, Jenis, Kategori, Jumlah")
            st.stop()

        df["Tanggal"] = pd.to_datetime(df["Tanggal"])
        df["Jumlah"] = df["Jumlah"].astype(float)

        # =====================
        # FILTER BULAN
        # =====================
        df["Bulan"] = df["Tanggal"].dt.strftime("%Y-%m")
        bulan = st.selectbox("📅 Pilih Bulan", df["Bulan"].unique())
        df = df[df["Bulan"] == bulan]

        # =====================
        # RINGKASAN
        # =====================
        masuk = df[df["Jenis"] == "Masuk"]["Jumlah"].sum()
        keluar = df[df["Jenis"] == "Keluar"]["Jumlah"].sum()
        saldo = masuk - keluar

        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Kas Masuk", f"Rp {masuk:,.0f}")
        col2.metric("💸 Kas Keluar", f"Rp {keluar:,.0f}")
        col3.metric("🧮 Saldo", f"Rp {saldo:,.0f}")

        # =====================
        # AI INSIGHT
        # =====================
        st.subheader("🤖 AI Insight Keuangan")

        if keluar > masuk:
            st.error("⚠️ Pengeluaran lebih besar dari pemasukan. Perlu pengendalian biaya.")
        elif keluar > 0.7 * masuk:
            st.warning("⚠️ Pengeluaran cukup tinggi. Disarankan evaluasi pos pengeluaran.")
        else:
            st.success("✅ Keuangan sehat. Pengeluaran masih dalam batas aman.")

        # =====================
        # GRAFIK TREN
        # =====================
        st.subheader("📈 Tren Kas")
        trend = df.groupby(["Tanggal", "Jenis"])["Jumlah"].sum().reset_index()
        fig_trend = px.line(trend, x="Tanggal", y="Jumlah", color="Jenis", markers=True)
        st.plotly_chart(fig_trend, use_container_width=True)

        # =====================
        # PIE KATEGORI
        # =====================
        st.subheader("🧁 Pengeluaran per Kategori")
        kategori_df = df[df["Jenis"] == "Keluar"].groupby("Kategori")["Jumlah"].sum().reset_index()
        fig_pie = px.pie(kategori_df, names="Kategori", values="Jumlah", hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

        # =====================
        # DATA
        # =====================
        st.subheader("📄 Detail Transaksi")
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Terjadi error: {e}")
else:
    st.info("⬆️ Upload file Excel untuk melihat dashboard")
