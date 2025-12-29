import streamlit as st
import pandas as pd

st.set_page_config(page_title="💼 SakuAkuntan", layout="wide")

st.title("💼 SakuAkuntan")
st.write("Aplikasi kas sederhana")

uploaded_file = st.file_uploader(
    "📂 Upload file Excel",
    type=["xlsx", "xls", "csv"]
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("📄 Data Kas")
        st.dataframe(df)

        if all(col in df.columns for col in ["Tanggal", "Keterangan", "Jenis", "Jumlah"]):
            masuk = df[df["Jenis"] == "Masuk"]["Jumlah"].sum()
            keluar = df[df["Jenis"] == "Keluar"]["Jumlah"].sum()
            saldo = masuk - keluar

            col1, col2, col3 = st.columns(3)
            col1.metric("Kas Masuk", f"Rp {masuk:,.0f}")
            col2.metric("Kas Keluar", f"Rp {keluar:,.0f}")
            col3.metric("Saldo", f"Rp {saldo:,.0f}")
        else:
            st.warning("Kolom harus: Tanggal, Keterangan, Jenis, Jumlah")

    except Exception as e:
        st.error(f"Terjadi error: {e}")

else:
    st.info("Silakan upload file Excel")
