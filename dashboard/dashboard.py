import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Theme and layout adjustments
st.set_page_config(page_title="Analisis Peminjaman Sepeda", layout="wide", page_icon="🚲")

# Header and sidebar
st.sidebar.title("🚲 Analisis Peminjaman Sepeda")
st.sidebar.markdown("""
### Profil Pengguna:
- **Nama**: Achmad Warsito Sujatmiko
- **Email**: titojatmiko91@gmail.com
- **ID DICODING**: itsmxj29
""")

st.sidebar.markdown("## Pilih Analisis")
# Change the order of the options in the sidebar
selected_analysis = st.sidebar.radio("Pilih Analisis yang Ingin Ditampilkan:", 
                                     ["EDA", "Peminjaman Bulanan", "Kondisi Cuaca", "Musim"])

# Load and prepare the dataset
@st.cache_data
def load_data():
    daily_data = pd.read_csv('https://raw.githubusercontent.com/Achmaddd29/Analisis-Data/main/dataset/day.csv')
    daily_data['dteday'] = pd.to_datetime(daily_data['dteday'])
    daily_data_2011 = daily_data[daily_data['dteday'].dt.year == 2011]
    return daily_data, daily_data_2011

daily_data, daily_data_2011 = load_data()

# Helper function to format large numbers
def format_large_number(num):
    return f"{num:,.0f}"

# EDA
if selected_analysis == "EDA":
    st.title("📊 Eksplorasi Data (EDA)")

    # Monthly bike rentals
    st.write("### Jumlah Penyewaan Sepeda per Bulan (Jan 2011 - Des 2012)")
    bulanan = daily_data.groupby(pd.Grouper(key='dteday', freq='M')).sum()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(bulanan.index, bulanan['cnt'], marker='o', linestyle='-', color='cornflowerblue')
    ax.set_title("Jumlah Penyewaan Sepeda per Bulan (Jan 2011 - Des 2012)", fontsize=14)
    ax.set_xlabel("Bulan", fontsize=12)
    ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
    ax.grid(True, axis='both', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    # Daily trend
    st.write("### Tren Harian Penyewaan Sepeda (2011-2012)")
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(daily_data['dteday'], daily_data['cnt'], color='purple', linestyle='-', marker='.')
    ax.set_title("Tren Harian Penyewaan Sepeda (2011-2012)", fontsize=14)
    ax.set_xlabel("Tanggal", fontsize=12)
    ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
    ax.grid(True, axis='both', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    # Histograms for specific features
    fitur = ['mnth', 'weekday', 'temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered']
    for feature in fitur:
        st.write(f"### Distribusi Jumlah Penyewaan Berdasarkan {feature}")
        fig = px.histogram(daily_data, x=feature, y='cnt', title=f'Distribusi {feature}', color_discrete_sequence=["salmon"])
        fig.update_traces(marker_line_color='black', marker_line_width=1)
        fig.update_layout(yaxis_title='Jumlah peminjam', title=f'Distribusi {feature}')
        st.plotly_chart(fig)

    # Pie charts for categorical features
    w = ['season', 'yr', 'holiday', 'workingday', 'weathersit']
    for feature in w:
        st.write(f"### Distribusi Jumlah Penyewaan Berdasarkan {feature}")
        fig = px.pie(daily_data, names=feature, values='cnt', title=f'Distribusi Jumlah Penyewaan Berdasarkan {feature}')
        st.plotly_chart(fig)

    # Correlation heatmap
    st.write("### Korelasi Fitur dalam Data Harian")
    day_corr = daily_data.corr()
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(day_corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax, linewidths=0.5)
    ax.set_title("Heatmap Korelasi Data Harian", fontsize=14)
    st.pyplot(fig)

# Monthly analysis
elif selected_analysis == "Peminjaman Bulanan":
    st.title("📅 Analisis Peminjaman Sepeda per Bulan (2011)")

    monthly_counts_2011 = daily_data_2011.groupby(daily_data_2011['dteday'].dt.month)['cnt'].sum()
    bulan_indo = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    monthly_counts_2011.index = monthly_counts_2011.index.map(lambda x: bulan_indo[x - 1])

    st.write("### Jumlah Peminjaman Sepeda per Bulan pada Tahun 2011")
    fig, ax = plt.subplots(figsize=(12, 6))
    monthly_counts_2011.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)
    ax.set_title("Jumlah Peminjaman Sepeda per Bulan (2011)", fontsize=14)
    ax.set_xlabel("Bulan", fontsize=12)
    ax.set_ylabel("Jumlah Peminjaman", fontsize=12)
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    highest_month = monthly_counts_2011.idxmax()
    lowest_month = monthly_counts_2011.idxmin()
    st.write(f"**Bulan dengan Peminjaman Tertinggi**: {highest_month} ({format_large_number(monthly_counts_2011.max())} peminjaman)")
    st.write(f"**Bulan dengan Peminjaman Terendah**: {lowest_month} ({format_large_number(monthly_counts_2011.min())} peminjaman)")

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
    weather_rental_avg.plot(kind='bar', color='lightgreen', edgecolor='black', ax=ax)
    ax.set_title("Rata-rata Peminjaman Sepeda Berdasarkan Kondisi Cuaca (2011)", fontsize=14)
    ax.set_xlabel("Kondisi Cuaca", fontsize=12)
    ax.set_ylabel("Rata-rata Peminjaman", fontsize=12)
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    st.write("**Rata-rata peminjaman per kondisi cuaca**:")
    for condition, avg in weather_rental_avg.items():
        st.write(f"- {condition}: {format_large_number(avg)} peminjaman rata-rata")

    st.write("### 📌 Kesimpulan:")
    st.write("1. Peminjaman sepeda tertinggi terjadi pada kondisi cuaca cerah.")
    st.write("2. Peminjaman sepeda terendah tercatat pada kondisi cuaca hujan lebat.")
    st.write("3. Secara umum, kondisi cuaca yang lebih baik seperti cerah dan mendung mendukung peminjaman sepeda yang lebih banyak.")

# Seasonal analysis
elif selected_analysis == "Musim":
    st.title("🍂 Analisis Berdasarkan Musim (2011)")

    seasonal_rentals = daily_data_2011.groupby('season')['cnt'].mean()
    musim = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
    seasonal_rentals.index = seasonal_rentals.index.map(musim)

    st.write("### Rata-rata Peminjaman Sepeda Berdasarkan Musim pada Tahun 2011")
    fig, ax = plt.subplots(figsize=(10, 5))
    seasonal_rentals.plot(kind='bar', color='lightcoral', edgecolor='black', ax=ax)
    ax.set_title("Rata-rata Peminjaman Sepeda Berdasarkan Musim (2011)", fontsize=14)
    ax.set_xlabel("Musim", fontsize=12)
    ax.set_ylabel("Rata-rata Peminjaman", fontsize=12)
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    max_season = seasonal_rentals.idxmax()
    min_season = seasonal_rentals.idxmin()
    st.write(f"**Musim dengan Peminjaman Sepeda Tertinggi**: {max_season} ({format_large_number(seasonal_rentals.max())} peminjaman)")
    st.write(f"**Musim dengan Peminjaman Sepeda Terendah**: {min_season} ({format_large_number(seasonal_rentals.min())} peminjaman)")

    st.write("### 📌 Kesimpulan:")
    st.write(f"1. Musim dengan peminjaman sepeda tertinggi adalah {max_season}, dengan total peminjaman mencapai {format_large_number(seasonal_rentals.max())}.")
    st.write(f"2. Musim dengan peminjaman sepeda terendah adalah {min_season}, dengan hanya {format_large_number(seasonal_rentals.min())} peminjaman.")
    st.write("3. Musim panas dan musim semi cenderung menunjukkan peminjaman yang lebih tinggi, sementara musim dingin dan musim gugur menunjukkan peminjaman yang lebih rendah.")




