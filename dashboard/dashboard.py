import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Theme and layout adjustments
st.set_page_config(page_title="Analisis Peminjaman Sepeda", layout="wide", page_icon="🚲")

# Header and sidebar
st.sidebar.title("🚲 Analisis Peminjaman Sepeda")
st.sidebar.write("Nama : Achmad Warsito Sujatmiko \n \nemail : titojatmiko91@gmail.com \n \n ID DICODING : itsmxj29")

st.sidebar.markdown("## Pilih Analisis")
selected_analysis = st.sidebar.radio("Pilih Analisis yang Ingin Ditampilkan:", 
                                     ["Peminjaman Bulanan", "Kondisi Cuaca", "Musim"])

# Load and prepare the dataset
@st.cache_data
def load_data():
    daily_data = pd.read_csv('C:/Users/Achmad Warsito S/proyek_analisis_data/dataset/day.csv')
    daily_data['dteday'] = pd.to_datetime(daily_data['dteday'])
    daily_data_2011 = daily_data[daily_data['dteday'].dt.year == 2011]
    return daily_data_2011

daily_data_2011 = load_data()

# Helper function to format large numbers
def format_large_number(num):
    return f"{num:,.0f}"

# Monthly analysis
if selected_analysis == "Peminjaman Bulanan":
    st.title("📅 Analisis Peminjaman Sepeda per Bulan (2011)")

    monthly_counts_2011 = daily_data_2011.groupby(daily_data_2011['dteday'].dt.month)['cnt'].sum()
    bulan_indo = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    monthly_counts_2011.index = monthly_counts_2011.index.map(lambda x: bulan_indo[x - 1])

    st.write("### Jumlah Peminjaman Sepeda per Bulan pada Tahun 2011")
    fig, ax = plt.subplots(figsize=(12, 6))
    monthly_counts_2011.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)
    ax.set_title("Jumlah Peminjaman Sepeda per Bulan (2011)")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Peminjaman")
    st.pyplot(fig)

    highest_month = monthly_counts_2011.idxmax()
    lowest_month = monthly_counts_2011.idxmin()
    st.write(f"**Bulan dengan Peminjaman Tertinggi**: {highest_month} ({format_large_number(monthly_counts_2011.max())} peminjaman)")
    st.write(f"**Bulan dengan Peminjaman Terendah**: {lowest_month} ({format_large_number(monthly_counts_2011.min())} peminjaman)")

    # Kesimpulan untuk Analisis Bulanan
    st.write("### 📌 Kesimpulan:")
    st.write(f"1. Peminjaman sepeda tertinggi terjadi pada bulan {highest_month}, dengan total peminjaman mencapai {format_large_number(monthly_counts_2011.max())}.")
    st.write(f"2. Peminjaman sepeda terendah terjadi pada bulan {lowest_month}, dengan hanya {format_large_number(monthly_counts_2011.min())} peminjaman.")
    st.write("3. Secara umum, peminjaman sepeda cenderung lebih tinggi pada bulan-bulan tertentu yang bisa dipengaruhi oleh faktor cuaca atau musim.")

# Weather analysis
elif selected_analysis == "Kondisi Cuaca":
    st.title("☀️ Analisis Berdasarkan Kondisi Cuaca (2011)")
    
    weather_rental_avg = daily_data_2011.groupby('weathersit')['cnt'].mean()
    weather_conditions = {1: "Cerah", 2: "Mendung", 3: "Hujan", 4: "Hujan Lebat"}
    weather_rental_avg.index = weather_rental_avg.index.map(weather_conditions)

    st.write("### Rata-rata Peminjaman Sepeda Berdasarkan Kondisi Cuaca pada Tahun 2011")
    fig, ax = plt.subplots(figsize=(10, 5))
    weather_rental_avg.plot(kind='bar', color='orange', edgecolor='black', ax=ax)
    ax.set_title("Rata-rata Peminjaman Sepeda Berdasarkan Kondisi Cuaca (2011)")
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Peminjaman")
    st.pyplot(fig)

    st.write("**Rata-rata peminjaman per kondisi cuaca**:")
    for condition, avg in weather_rental_avg.items():
        st.write(f"- {condition}: {format_large_number(avg)} peminjaman rata-rata")

    # Kesimpulan untuk Analisis Cuaca
    st.write("### 📌 Kesimpulan:")
    st.write("1. Peminjaman sepeda tertinggi terjadi pada kondisi cuaca cerah.")
    st.write("2. Peminjaman sepeda terendah tercatat pada kondisi cuaca hujan lebat.")
    st.write("3. Secara umum, kondisi cuaca yang lebih baik seperti cerah dan mendung mendukung peminjaman sepeda yang lebih banyak.")

# Seasonal analysis
elif selected_analysis == "Musim":
    st.title("🍂 Analisis Berdasarkan Musim (2011)")
    
    season_rental_avg = daily_data_2011.groupby('season')['cnt'].mean()
    season_names = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
    season_rental_avg.index = season_rental_avg.index.map(season_names)

    st.write("### Rata-rata Peminjaman Sepeda Berdasarkan Musim pada Tahun 2011")
    fig, ax = plt.subplots(figsize=(10, 5))
    season_rental_avg.plot(kind='bar', color='green', edgecolor='black', ax=ax)
    for i, v in enumerate(season_rental_avg):
        ax.text(i, v + 50, f'{int(v)}', ha='center', va='bottom', fontsize=10)
    ax.set_title("Rata-rata Peminjaman Sepeda Berdasarkan Musim (2011)")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Peminjaman")
    st.pyplot(fig)

    max_season = season_rental_avg.idxmax()
    min_season = season_rental_avg.idxmin()
    st.write(f"**Musim dengan Peminjaman Sepeda Tertinggi**: {max_season} ({format_large_number(season_rental_avg.max())} peminjaman)")
    st.write(f"**Musim dengan Peminjaman Sepeda Terendah**: {min_season} ({format_large_number(season_rental_avg.min())} peminjaman)")

    # Kesimpulan untuk Analisis Musim
    st.write("### 📌 Kesimpulan:")
    st.write(f"1. Musim dengan peminjaman sepeda tertinggi adalah {max_season}, dengan total peminjaman mencapai {format_large_number(season_rental_avg.max())}.")
    st.write(f"2. Musim dengan peminjaman sepeda terendah adalah {min_season}, dengan hanya {format_large_number(season_rental_avg.min())} peminjaman.")
    st.write("3. Musim panas dan musim semi cenderung menunjukkan peminjaman yang lebih tinggi, sementara musim dingin dan musim gugur menunjukkan peminjaman yang lebih rendah.")



