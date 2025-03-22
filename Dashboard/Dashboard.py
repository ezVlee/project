import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Kualitas Udara", layout="wide")

# Judul Dashboard
st.title("Dashboard Analisis Kualitas Udara")

# Load Data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/ezVlee/project/main/Dashboard/PRSA_Data_Nongzhanguan_20130301-20170228.csv"
    try:
        df = pd.read_csv(url)
        
        # Konversi tanggal
        df['date'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
        df.set_index('date', inplace=True)

        # Hapus nilai NaN
        df_cleaned = df.dropna()

        return df_cleaned

    except Exception as e:
        st.error(f"Terjadi kesalahan saat mengunduh data: {e}")
        return None

df_cleaned = load_data()

if df_cleaned is not None:
    # Sidebar
    st.sidebar.header("Pilih Analisis")
    menu = st.sidebar.radio("Navigasi", ["Tren Polusi Udara", "Faktor yang Mempengaruhi Kualitas Udara"])

    if menu == "Tren Polusi Udara":
        st.subheader("Tren Polusi Udara per Tahun dan Bulan")
        
        # Rata-rata tahunan
        df_yearly = df_cleaned.resample('Y').mean(numeric_only=True)
        fig, ax = plt.subplots(figsize=(10, 5))
        for year, row in df_yearly.iterrows():
            ax.bar(row.index, row.values, label=str(year.year))
        ax.set_title("Rata-rata Polutan per Tahun")
        ax.set_ylabel("Konsentrasi (µg/m³)")
        ax.set_xlabel("Polutan")
        ax.legend(title="Tahun")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
        
        # Rata-rata bulanan
        df_monthly = df_cleaned.resample('M').mean(numeric_only=True)
        fig, ax = plt.subplots(figsize=(12, 6))
        df_monthly.plot(kind='bar', ax=ax)
        ax.set_title("Rata-rata Polutan per Bulan")
        ax.set_ylabel("Konsentrasi (µg/m³)")
        ax.set_xlabel("Bulan")
        ax.legend(title="Polutan")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)

        # Insight
        st.markdown("""
        **Insight:**
        - Peningkatan polusi di awal tahun bisa disebabkan oleh faktor musiman, seperti peningkatan aktivitas industri dan kondisi atmosfer yang memerangkap polutan.
        - CO sebagai polutan dominan menunjukkan adanya sumber utama seperti kendaraan bermotor dan industri.
        - Polutan lain punya nilai yang lebih kecil dibanding CO
        - Setiap awal dan akhir tahun, polutan menagalami kenaikan
        """)

    elif menu == "Faktor yang Mempengaruhi Kualitas Udara":
        st.subheader("Faktor yang Mempengaruhi Kualitas Udara")

        # Visualisasi Korelasi Polutan dan Faktor Lingkungan
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(df_cleaned[['PM2.5', 'PM10', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr(), 
                    annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        ax.set_title('Korelasi antara Polutan dan Faktor Lingkungan')
        st.pyplot(fig)

        # Insight
        st.markdown("""
        **Insight:**
        - Polusi udara dipengaruhi oleh kombinasi sumber emisi (misalnya pembakaran) dan faktor lingkungan.
        - PM2.5 dan PM10 sangat berkorelasi karena memiliki sumber yang sama, yaitu pembakaran dan polusi kendaraan.
        - Suhu, kecepatan angin, dan tekanan udara juga mempengaruhi polusi udara.
        - Memahami tren polusi dan faktor lingkungan dapat membantu dalam pengambilan keputusan untuk mengurangi dampak polusi udara.
        """)
else:
    st.error("Data gagal dimuat. Periksa kembali URL atau format file CSV.")
