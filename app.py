import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="💼 SakuAkuntan", layout="wide")

st.title("💼 SakuAkuntan")
st.caption("Aplikasi Akuntansi Sederhana + Dashboard & Insight")

# =============================
# INPUT MANUAL
# =============================
st.subheader("✍️ Input Transaksi Manual")

with st.form("form_input"):
    tgl = st.date_input("Tanggal")
    ket = st.text_input("Keterangan")
    jenis = st.selectbox("Jenis", ["Masuk", "Keluar"])
    kategori = st.text_input("Kategori")
    jumlah = st.number_input("Jumlah", min_value=0)
    submit = st.form_submit_button("Tambah Transaksi")

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Tanggal", "Keterangan", "Jenis", "Kategori", "Jumlah"]
    )

if submit:
    new_row = {
        "Tanggal": tgl,
        "Keterangan": ket,
        "Jenis": jenis,
        "Kategori": kategori,
        "Jumlah": jumlah
    }
    st.session_state.data = pd.concat(
        [st.session_state.data, pd.DataFrame([new_row])],
        ignore_index=True
    )
    st.success("Transaksi berhasil ditambahkan")

st.divider()

# =============================
# UPLOAD EXCEL
# =============================
st.subheader("📂 Upload File Excel (Opsional)")

uploaded_file = st.file_uploader(
    "Upload Excel Kas",
    type=["xlsx", "xls", "csv"]
)

df_excel = pd.DataFrame()

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df_excel = pd.read_csv(uploaded_file)
    else:
        df_excel = pd.read_excel(uploaded_file)

# =============================
# GABUNG DATA
# =============================
df = pd.concat([st.session_state.data, df_excel], ignore_index=True)

if df.empty:
    st.info("Silakan input manual atau upload Excel")
    st.stop()

# =============================
# PROCESS
# =============================
df["Tanggal"] = pd.to_datetime(df["Tanggal"])
df["Jumlah"] = df["Jumlah"].astype(float)
df["Bulan"] = df["Tanggal"].dt.strftime("%Y-%m")

bulan = st.selectbox("📅 Pilih Bulan", df["Bulan"].unique())
df = df[df["Bulan"] == bulan]

# =============================
# DASHBOARD
# =============================
masuk = df[df["Jenis"] == "Masuk"]["Jumlah"].sum()
keluar = df[df["Jenis"] == "Keluar"]["Jumlah"].sum()
saldo = masuk - keluar

st.subheader("📊 Ringkasan Keuangan")
c1, c2, c3 = st.columns(3)
c1.metric("💰 Kas Masuk", f"Rp {masuk:,.0f}")
c2.metric("💸 Kas Keluar", f"Rp {keluar:,.0f}")
c3.metric("🧮 Saldo", f"Rp {saldo:,.0f}")

# =============================
# AI INSIGHT
# =============================
st.subheader("🤖 Insight Otomatis")

if keluar > masuk:
    st.error("⚠️ Keuangan defisit. Pengeluaran lebih besar dari pemasukan.")
elif keluar > 0.7 * masuk:
    st.warning("⚠️ Pengeluaran tinggi. Perlu pengendalian biaya.")
else:
    st.success("✅ Keuangan sehat dan terkendali.")

# =============================
# CHARTS
# =============================
st.subheader("📈 Tren Kas")
trend = df.groupby(["Tanggal", "Jenis"])["Jumlah"].sum().reset_index()
fig_trend = px.line(trend, x="Tanggal", y="Jumlah", color="Jenis", markers=True)
st.plotly_chart(fig_trend, use_container_width=True)

st.subheader("🧁 Pengeluaran per Kategori")
kat = df[df["Jenis"] == "Keluar"].groupby("Kategori")["Jumlah"].sum().reset_index()
if not kat.empty:
    fig_pie = px.pie(kat, names="Kategori", values="Jumlah", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

# =============================
# DATA TABLE
# =============================
st.subheader("📄 Detail Transaksi")
st.dataframe(df, use_container_width=True)
