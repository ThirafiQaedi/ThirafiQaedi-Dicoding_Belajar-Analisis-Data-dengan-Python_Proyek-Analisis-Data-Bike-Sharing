import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


day_df = pd.read_csv("https://raw.githubusercontent.com/ThirafiQaedi/ThirafiQaedi-Dicoding_Belajar-Analisis-Data-dengan-Python_Proyek-Analisis-Data-Bike-Sharing/refs/heads/main/Dataset/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/ThirafiQaedi/ThirafiQaedi-Dicoding_Belajar-Analisis-Data-dengan-Python_Proyek-Analisis-Data-Bike-Sharing/refs/heads/main/Dataset/hour.csv")
all_df = pd.read_csv("https://raw.githubusercontent.com/ThirafiQaedi/ThirafiQaedi-Dicoding_Belajar-Analisis-Data-dengan-Python_Proyek-Analisis-Data-Bike-Sharing/refs/heads/main/dashboard/all_data.csv")


# Judul Dashboard
st.title("Dashboard Penyewaan Sepeda 🚴🏻")

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

    # Rentang hari
    day_range = st.multiselect("Pilih Hari dalam Seminggu", options=[0, 1, 2, 3, 4, 5, 6], default=[0, 1, 2, 3, 4, 5, 6], format_func=lambda x: ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"][x])

    # Rentang jam
    hour_range = st.slider("Pilih Rentang Jam", 0, 23, (0, 23))

    # Rentang musim
    season_range = st.multiselect("Pilih Musim", options=[1, 2, 3, 4], default=[1, 2, 3, 4], format_func=lambda x: ["Musim Semi", "Musim Panas", "Musim Gugur", "Musim Dingin"][x-1])


# Filter data berdasarkan rentang yang dipilih
filtered_day_df = day_df[
    (day_df['temp'] >= temp_range[0]) & (day_df['temp'] <= temp_range[1]) &
    (day_df['hum'] >= hum_range[0]) & (day_df['hum'] <= hum_range[1]) &
    (day_df['windspeed'] >= windspeed_range[0]) & (day_df['windspeed'] <= windspeed_range[1]) &
    (day_df['season'].isin(season_range)) &
    (day_df['cnt'])
]

# Filter data berdasarkan hari
filtered_hour_df = hour_df[hour_df['weekday'].isin(day_range)]

# 1. Visualisasi korelasi kondisi cuaca terhadap jumlah penyewaan sepeda Menggunakan heatmap 
st.header("Menggunakan heatmap untuk visualisasi korelasi kondisi cuaca terhadap jumlah penyewaan sepeda")
correlation = filtered_day_df[['temp', 'hum', 'windspeed', 'cnt']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Korelasi antara Kondisi Cuaca dan Jumlah Penyewaan ')
st.pyplot(plt)


# 2. Visualisasi rata-rata penyewaan berdasarkan jenis cuaca dengan bar chart
st.header("Rata-rata Penyewaan Berdasarkan Jenis Cuaca ")
weather_summary = filtered_day_df.groupby('weathersit')['cnt'].agg(['mean', 'sum', 'count']).reset_index()
weather_summary.columns = ['Weather Situation', 'Average Rentals', 'Total Rentals', 'Days Count']
plt.figure(figsize=(10, 5))
sns.barplot(x='Weather Situation', y='Average Rentals', data=weather_summary, palette='viridis')
plt.title('Rata-rata Penyewaan Berdasarkan Jenis Cuaca')
plt.xlabel('Jenis Cuaca')
plt.ylabel('Rata-rata Penyewaan')
plt.xticks(ticks=[0, 1, 2, 3], labels=['Cerah', 'Berkabut', 'Hujan Ringan', 'Hujan Berat/salju'])
st.pyplot(plt)

# 3. jumlah penyewaan sepeda berdasarkan hari dalam seminggu dan jam dalam sehari
st.header("penyewaan sepeda berdasarkan hari dalam seminggu dan jam dalam sehari")
# 3. Visualisasi Jumlah Penyewaan Berdasarkan Hari dalam Seminggu
daily_rentals = filtered_hour_df.groupby('weekday')['cnt'].sum().reset_index()
daily_rentals.columns = ['Day of Week', 'Total Rentals']
plt.figure(figsize=(10, 5))
sns.barplot(x='Day of Week', y='Total Rentals', data=daily_rentals, palette='Blues')
plt.title('Jumlah Penyewaan Berdasarkan Hari dalam Seminggu')
plt.xlabel('Hari dalam Seminggu')
plt.ylabel('Total Penyewaan')
plt.xticks(ticks=[0, 1, 2, 3, 4, 5, 6], labels=["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"])
st.pyplot(plt)

# 3. Visualisasi Jumlah Penyewaan Berdasarkan Jam dalam Sehari
hourly_rentals = filtered_hour_df.groupby('hr')['cnt'].sum().reset_index()
hourly_rentals.columns = ['Hour', 'Total Rentals']
plt.figure(figsize=(10, 5))
sns.lineplot(x='Hour', y='Total Rentals', data=hourly_rentals, marker='o')
plt.title('Jumlah Penyewaan Berdasarkan Jam dalam Sehari')
plt.xlabel('Jam dalam Sehari')
plt.ylabel('Total Penyewaan')
plt.xticks(range(0, 24))
plt.grid()
st.pyplot(plt)

# 4. Visualisasi Jumlah Penyewaan Berdasarkan Musim
st.header("Jumlah Penyewaan Berdasarkan Musim")
seasonal_rentals = filtered_day_df.groupby('season')['cnt'].agg(['mean', 'sum', 'count']).reset_index()
seasonal_rentals.columns = ['Season', 'Average Rentals', 'Total Rentals', 'Days Count']
plt.figure(figsize=(10, 5))
sns.barplot(x='Season', y='Average Rentals', data=seasonal_rentals, palette='Set2')
plt.title('Jumlah Penyewaan Berdasarkan Musim')
plt.xlabel('Musim')
plt.ylabel('Rata-rata Penyewaan')
plt.xticks(ticks=[0, 1, 2, 3], labels=['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])
st.pyplot(plt)

# Insight dan Kesimpulan
st.header("Insight dan Kesimpulan")

st.header("1. Seberapa besar pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda?")
st.write("""
- Dari analisa yang dilakukan, suhu memiliki hubungan positif yang kuat dengan jumlah penyewaan, sedangkan kelembapan memiliki hubungan negatif. 
Ini menunjukkan bahwa semakin tinggi suhu cuaca, semakin banyak orang yang menyewa sepeda, sementara cuaca dengan kelembapan yang tinggi cenderung mengurangi minat penyewaan.
""")

st.markdown("---") 

st.header("2. Apakah ada jenis cuaca tertentu yang menyebabkan lonjakan atau penurunan penyewaan?")
st.write("""
- Cuaca cerah memiliki rata-rata penyewaan yang jauh lebih tinggi dibandingkan dengan cuaca hujan, mendung, atau pun cuaca ekstrem. 
Ini menunjukkan bahwa orang lebih cenderung menyewa sepeda saat cuaca baik.
""")

st.markdown("---")


st.header("3. Bagaimana pola jumlah penyewaan sepeda bervariasi berdasarkan hari dalam seminggu dan jam dalam sehari?")
st.write("""
- Analisa menunjukkan di akhir pekan (Jumat, Sabtu, dan Minggu) jumlah penyewaan yang lebih tinggi dibandingkan dengan hari kerja. 
Analisis berdasarkan jam juga dapat menunjukkan jam-jam sibuk, seperti pagi dan sore hari. Penyewaan tertinggi terjadi pada hari Sabtu dengan total 300 penyewaan, 
ini menunjukkan bahwa akhir pekan adalah waktu yang populer untuk menyewa sepeda.
""")

st.markdown("---")  


st.header("4. Bagaimana pola permintaan sepeda berbagi berubah berdasarkan musim?")
st.write("""
- Musim panas memiliki rata-rata penyewaan yang jauh lebih tinggi dibandingkan dengan musim dingin. 
Ini menunjukkan bahwa cuaca yang lebih hangat dan lebih banyak aktivitas luar ruangan selama musim panas mendorong lebih banyak penyewaan sepeda.
""")

st.markdown("---")  
st.header("za maker 🗿 : ")
st.write("**Nama:**  Muhamad Thirafi Qaedi Setiawan")
st.write("**Email:** Qaedi68@gmail.com")
st.write("**ID Dicoding:** muhamadthirafi")

st.markdown("---")  

st.write("© 2025 Muhammad Thirafi Qaedi Setiawan")