import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi tampilan
st.set_page_config(page_title="Dashboard Kualitas Udara", layout="wide")

# Judul Dashboard
st.title("Dashboard Analisis Kualitas Udara")

# Load Data
@st.cache_data
def load_data():
    url = "https://github.com/ezVlee/project/blob/main/Dashboard/PRSA_Data_Nongzhanguan_20130301-20170228.csv"
    df = pd.read_csv(url)
    df_cleaned = df.dropna()
    df_cleaned['date'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df_cleaned.set_index('date', inplace=True)
    return df_cleaned

df_cleaned = load_data()

# Sidebar
st.sidebar.header("Pilih Analisis")
menu = st.sidebar.radio("Navigasi", ["Tren Polusi Udara", "Faktor yang Mempengaruhi Kualitas Udara"])

if menu == "Tren Polusi Udara":
    st.subheader("Tren Polusi Udara dalam Lima Tahun")

    # Visualisasi Tren Polusi Udara
    monthly_avg = df_cleaned.resample('ME').mean(numeric_only=True)
    fig, ax = plt.subplots(figsize=(12, 6))
    for polutan in ['PM2.5', 'PM10', 'NO2', 'CO', 'O3']:
        ax.plot(monthly_avg.index, monthly_avg[polutan], label=polutan)
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Konsentrasi (µg/m³)')
    ax.set_title('Tren Polusi Udara')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Insight
    st.markdown("""
    **Insight:**
    - Peningkatan polusi di awal tahun bisa disebabkan oleh faktor musiman, seperti peningkatan aktivitas industri dan kondisi atmosfer yang memerangkap polutan.
    - CO sebagai polutan dominan menunjukkan adanya sumber utama seperti kendaraan bermotor dan industri.
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

