import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def Load_data():
    day_df = pd.read_csv("https://raw.githubusercontent.com/ThirafiQaedi/ThirafiQaedi-Dicoding_Belajar-Analisis-Data-dengan-Python_Proyek-Analisis-Data-Bike-Sharing/refs/heads/main/Dataset/day.csv")
    hour_df = pd.read_csv("https://raw.githubusercontent.com/ThirafiQaedi/ThirafiQaedi-Dicoding_Belajar-Analisis-Data-dengan-Python_Proyek-Analisis-Data-Bike-Sharing/refs/heads/main/Dataset/hour.csv")
    all_df = pd.read_csv("https://raw.githubusercontent.com/ThirafiQaedi/ThirafiQaedi-Dicoding_Belajar-Analisis-Data-dengan-Python_Proyek-Analisis-Data-Bike-Sharing/refs/heads/main/dashboard/all_data.csv")
    return day_df, hour_df, all_df

def Visualisasi_sewa_musim(data_df):
    st.header("Jumlah Penyewaan Berdasarkan Musim")
    Rental_Musiman = data_df.groupby('season')['cnt'].agg(['mean', 'sum', 'count']).reset_index()
    Rental_Musiman.columns = ['Musim', 'Rata2 rental', 'Total Rental', 'Jumlah']
    Season_mapping = {
        1: 'Musim Semi',
        2: 'Musim Panas',
        3: 'Musim Gugur',
        4: 'Musim Dingin'
    }
    Rental_Musiman['Musim'] = Rental_Musiman['Musim'].map(Season_mapping)
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Musim', y='Rata2 rental', data=Rental_Musiman, palette='Set2')
    plt.title('Jumlah Penyewaan Berdasarkan Musim ')
    plt.xlabel('Musim')
    plt.ylabel('Rata-rata Penyewaan')
    st.pyplot(plt)

def Visualisasi_korelasi(day_df):
    st.header("Menggunakan heatmap untuk visualisasi korelasi kondisi cuaca terhadap jumlah penyewaan sepeda")
    correlation = day_df[['temp', 'hum', 'windspeed', 'cnt']].corr()
    correlation.columns = ['Temperatur','humidity','windspeed','Total Jumlah']
    correlation.index = ['Temperatur', 'Humidity', 'Windspeed', 'Total Jumlah']
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Korelasi antara Kondisi Cuaca dan Jumlah Penyewaan ')
    st.pyplot(plt)

def Visualisasi_Penyewaan_cuaca(weather_data):
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Situasi Cuaca', y='Average Rentals', data=weather_data, palette='viridis')
    plt.title('Rata-rata Penyewaan Berdasarkan Jenis Cuaca ')
    plt.xlabel('Jenis Cuaca')
    plt.ylabel('Rata-rata Penyewaan')
    st.pyplot(plt)

def visualisasi_jam_Sehari(data_df):
    Rental_per_jam = data_df.groupby('hr')['cnt'].sum().reset_index()
    Rental_per_jam.columns = ['Jam', 'Total Rental']
    Hour_mapping = {
        0: '0',
        1: '1',
        2: '2',
        3: '3',
        4: '4' ,
        5: '5',
        6: '6',
        7: '7',
        8: '8',
        9: '9',
        10: '10',
        11: '11',
        12: '12',
        13: '13',
        14: '14',
        15: '15',
        16: '16',
        17: '17',
        18: '18',
        19: '19',
        20: '20',
        21: '21',
        22: '22',
        23: '23'  
    }
    Rental_per_jam['Jam'] = Rental_per_jam['Jam'].map(Hour_mapping)
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='Jam', y='Total Rental', data=Rental_per_jam, marker='o')
    plt.title('Jumlah Penyewaan Berdasarkan Jam dalam Sehari')
    plt.xlabel('Jam dalam Sehari')
    plt.ylabel('Total Penyewaan')
    plt.grid()
    st.pyplot(plt)

def visualisasi_Hari_Seminggu(data_df):
    rental_Harian  = data_df.groupby('weekday')['cnt'].sum().reset_index()
    rental_Harian .columns = ['Hari dalam seminggu', 'Total Rentals']
    day_mapping = {
        0: 'Senin',
        1: 'Selasa',
        2: 'Rabu',
        3: 'Kamis',
        4: 'Jumat',
        5: 'Sabtu',
        6: 'Minggu'
    }
    rental_Harian ['Hari dalam seminggu'] = rental_Harian ['Hari dalam seminggu'].map(day_mapping)
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Hari dalam seminggu', y='Total Rentals', data=rental_Harian , palette='Blues')
    plt.title('Jumlah Penyewaan Berdasarkan Hari dalam Seminggu')
    plt.xlabel('Hari dalam Seminggu')
    plt.ylabel('Total Penyewaan')
    st.pyplot(plt)



### main
# Judul Dashboard
st.title("Dashboard Penyewaan Sepeda 🚴🏻")
day_df, hour_df, all_df =Load_data()
# Sidebar untuk memilih rentang data
with st.sidebar:
    st.sidebar.title("Da bike Sharing detail 🌤☀☁🌧🌦🌩🌨📅")
    st.header("Filter Data")

    # Rentang suhu
    temp_range = st.slider("Pilih Rentang Suhu", float(day_df['temp'].min()), float(day_df['temp'].max()), (float(day_df['temp'].min()), float(day_df['temp'].max())))

    # Rentang kelembapan
    hum_range = st.slider("Pilih Rentang Kelembapan", float(day_df['hum'].min()), float(day_df['hum'].max()), (float(day_df['hum'].min()), float(day_df['hum'].max())))

    # Rentang kecepatan angin
    windspeed_range = st.slider("Pilih Rentang Kecepatan Angin", float(day_df['windspeed'].min()), float(day_df['windspeed'].max()), (float(day_df['windspeed'].min()), float(day_df['windspeed'].max())))

    # Rentang musim
    season_range = st.multiselect("Pilih Musim", options=[1, 2, 3, 4], default=[1, 2, 3, 4], format_func=lambda x: ["Musim Semi", "Musim Panas", "Musim Gugur", "Musim Dingin"][x-1])
    
    # Rentang cuaca 
    weather_options = {
        1: "Cerah",
        2: "Berkabut",
        3: "Hujan Ringan",
        4: "Hujan Berat/salju"
    }
    weather_range = st.multiselect(
        "Pilih Jenis Cuaca",
        options=list(weather_options.keys()),
        default=list(weather_options.keys()),
        format_func=lambda x: weather_options[x]
    )

    # Rentang hari
    day_range = st.multiselect("Pilih Hari dalam Seminggu", options=[0, 1, 2, 3, 4, 5, 6], default=[0, 1, 2, 3, 4, 5, 6], format_func=lambda x: ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"][x])

    # Rentang jam
    hour_range = st.slider("Pilih Rentang Jam", 0, 23, (0, 23))

    

# Filter data berdasarkan rentang yang dipilih
filtered_day_df = day_df[
    (day_df['temp'] >= temp_range[0]) & (day_df['temp'] <= temp_range[1]) &
    (day_df['hum'] >= hum_range[0]) & (day_df['hum'] <= hum_range[1]) &
    (day_df['windspeed'] >= windspeed_range[0]) & (day_df['windspeed'] <= windspeed_range[1]) &
    (day_df['season'].isin(season_range)) &
    (day_df['weathersit'].isin(weather_range)) &
    (day_df['cnt'])
]
# Filter data berdasarkan hari
filtered_hour_df = hour_df[
    hour_df['weekday'].isin(day_range) & 
    (hour_df['hr'] >= hour_range[0]) & (hour_df['hr'] <= hour_range[1])
]



# 1. Visualisasi korelasi kondisi cuaca terhadap jumlah penyewaan sepeda Menggunakan heatmap 
Visualisasi_korelasi(filtered_day_df)

# 2. Visualisasi rata-rata penyewaan berdasarkan jenis cuaca dengan bar chart
st.header("Rata-rata Penyewaan Berdasarkan Jenis Cuaca ")
weather_summary = filtered_day_df.groupby('weathersit')['cnt'].agg(['mean', 'sum', 'count']).reset_index()
weather_summary.columns = ['Situasi Cuaca', 'Average Rentals', 'Total Rentals', 'Days Count']
weather_mapping = {
    1: 'Cerah',
    2: 'Berkabut',
    3: 'Hujan Ringan',
    4: 'Hujan Berat/salju',
}
weather_summary['Situasi Cuaca'] = weather_summary['Situasi Cuaca'].map(weather_mapping)
Visualisasi_Penyewaan_cuaca(weather_summary)


# 3. Visualisasi jumlah penyewaan sepeda berdasarkan hari dalam seminggu dan jam dalam sehari
st.header("penyewaan sepeda berdasarkan hari dalam seminggu dan jam dalam sehari")
# - Visualisasi Jumlah Penyewaan Berdasarkan Hari dalam Seminggu
visualisasi_Hari_Seminggu(filtered_hour_df)

# - Visualisasi Jumlah Penyewaan Berdasarkan Jam dalam Sehari
visualisasi_jam_Sehari(filtered_hour_df)


# 4. Visualisasi Jumlah Penyewaan Berdasarkan Musim
Visualisasi_sewa_musim(filtered_day_df)


# Insight dan Kesimpulan
st.header("Insight dan Kesimpulan")

st.subheader("1. Seberapa besar pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda?")
st.write("""
- Dari analisa yang di lakukan suhu memiliki hubungan positif yang kuat dengan jumlah penyewaan, sedangkan dengan kelembapan memiliki hubungan negatif. 
    Ini menunjukkan bahwa semakin tinggi suhu cuaca , semakin banyak orang yang menyewa sepeda, 
    sementara cuaca dengan kelembapan yang tinggi cenderung mengurangi minat penyewaan.
""")

st.markdown("---") 

st.subheader("2. Apakah ada jenis cuaca tertentu yang menyebabkan lonjakan atau penurunan penyewaan?")
st.write("""
- cuaca cerah memiliki rata-rata penyewaan yang jauh lebih tinggi dibandingkan dengan cuaca hujan, mendung atau pun cuaca extrem. 
    Ini menunjukkan bahwa orang lebih cenderung menyewa sepeda saat cuaca baik.
""")

st.markdown("---")


st.subheader("3. Bagaimana pola jumlah penyewaan sepeda bervariasi berdasarkan hari dalam seminggu dan jam dalam sehari?")
st.write("""
- Analisa menunjukan di akhir pekan (jumat, Sabtu dan Minggu) jumlah penyewaan yang lebih tinggi dibandingkan dengan hari kerja. 
    Analisis berdasarkan jam juga dapat menunjukkan jam-jam sibuk, seperti pagi dan sore hari. penyewaan tertinggi terjadi pada hari Sabtu dengan total 300 penyewaan, 
    ini menunjukkan bahwa akhir pekan adalah waktu yang populer untuk menyewa sepeda.
""")

st.markdown("---")  


st.subheader("4. Bagaimana pola permintaan sepeda berbagi berubah berdasarkan musim?")
st.write("""
- musim panas dan musim gugur memiliki rata-rata penyewaan yang jauh lebih tinggi dibandingkan dengan musim dingin dan musim semi. 
    Ini menunjukkan bahwa cuaca yang lebih hangat dan lebih banyak aktivitas luar ruangan 
    selama musim panas mendorong lebih banyak penyewaan sepeda.
""")

st.markdown("---")  
st.header("za maker 🗿 : ")
st.write("**Nama:**  Muhamad Thirafi Qaedi Setiawan")
st.write("**Email:** Qaedi68@gmail.com")
st.write("**ID Dicoding:** muhamadthirafi")

st.markdown("---")  

st.write("Copyright (c) Muhammad Thirafi Qaedi Setiawan 2025 ")