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
    
    # Fitur Interaktif: Filter berdasarkan rentang tahun
    st.sidebar.header("Filter Data")
    min_year = df_cleaned.index.year.min()
    max_year = df_cleaned.index.year.max()
    start_year, end_year = st.sidebar.slider("Pilih Rentang Tahun", min_year, max_year, (min_year, max_year))
    
    df_filtered = df_cleaned[(df_cleaned.index.year >= start_year) & (df_cleaned.index.year <= end_year)]
    
    if menu == "Tren Polusi Udara":
        st.subheader("Tren Polusi Udara per Tahun")

        # Gabungan tampilan 5 tahun dalam satu bagan
        fig, ax = plt.subplots(figsize=(12, 6))
        df_yearly.plot(kind='bar', ax=ax)
        ax.set_title("Rata-rata Polutan per Tahun dalam Rentang yang Dipilih")
        ax.set_ylabel("Konsentrasi (µg/m³)")
        ax.set_xlabel("Tahun")
        ax.legend(title="Polutan")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
        
        # Rata-rata per tahun dalam rentang yang dipilih
        if not df_filtered.empty:
            df_yearly = df_filtered.resample('Y').mean(numeric_only=True)
            df_yearly = df_yearly[['PM2.5', 'PM10', 'NO2', 'CO', 'O3']]
            
            fig, ax = plt.subplots(figsize=(12, 6))
            df_yearly.plot(kind='bar', ax=ax)
            ax.set_title("Rata-rata Polutan per Tahun dalam Rentang yang Dipilih")
            ax.set_ylabel("Konsentrasi (µg/m³)")
            ax.set_xlabel("Tahun")
            ax.legend(title="Polutan")
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            st.pyplot(fig)
        else:
            st.warning("Tidak ada data dalam rentang tahun yang dipilih.")
        
        # Insight
        st.markdown("""
        **Insight:**
        - Peningkatan polusi dapat dipengaruhi oleh faktor musiman dan kebijakan lingkungan.
        - CO sebagai polutan dominan menunjukkan adanya sumber utama seperti kendaraan bermotor dan industri.
        - Setiap awal dan akhir tahun, polutan mengalami kenaikan.
        """)

    elif menu == "Faktor yang Mempengaruhi Kualitas Udara":
        st.subheader("Faktor yang Mempengaruhi Kualitas Udara")
        
        # Visualisasi Korelasi Polutan dan Faktor Lingkungan
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(df_filtered[['PM2.5', 'PM10', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr(), 
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
