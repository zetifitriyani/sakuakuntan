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

        st.subheader("📄 Data Kas")
        st.dataframe(df, use_container_width=True)

        if all(col in df.columns for col in ["Tanggal", "Keterangan", "Jenis", "Jumlah"]):

            df["Jumlah"] = df["Jumlah"].astype(float)

            kas_masuk = df[df["Jenis"] == "Masuk"]["Jumlah"].sum()
            kas_keluar = df[df["Jenis"] == "Keluar"]["Jumlah"].sum()
            saldo = kas_masuk - kas_keluar

            st.subheader("📊 Ringkasan Dashboard")
            col1, col2, col3 = st.columns(3)
            col1.metric("💰 Kas Masuk", f"Rp {kas_masuk:,.0f}")
            col2.metric("💸 Kas Keluar", f"Rp {kas_keluar:,.0f}")
            col3.metric("🧮 Saldo Akhir", f"Rp {saldo:,.0f}")

            # Dashboard Chart
            chart_df = pd.DataFrame({
                "Kategori": ["Kas Masuk", "Kas Keluar"],
                "Jumlah": [kas_masuk, kas_keluar]
            })

            fig = px.bar(
                chart_df,
                x="Kategori",
                y="Jumlah",
                text_auto=True,
                title="Grafik Kas Masuk vs Kas Keluar"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("Kolom Excel harus: Tanggal, Keterangan, Jenis, Jumlah")

    except Exception as e:
        st.error(f"Terjadi error: {e}")

else:
    st.info("⬆️ Upload file Excel untuk melihat dashboard")
