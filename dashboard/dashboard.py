import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st 
import datetime
sns.set(style='dark')
 
# Functions untuk membuat DataFrame baru dari Main DataFrame
def  create_monthly_rental_count_for_years_df(main_df):
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    main_df["mnth"] = pd.Categorical(main_df["mnth"], categories=month_order, ordered=True)
    return main_df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()

def create_mean_hourly_df(main_df):
    return main_df.groupby('hr')['cnt'].mean().reset_index()

def create_count_rental_df(main_df):
    return main_df[['hr', 'registered', 'casual', 'cnt']]

# Membaca file csv  main_df
hour_day_df = pd.read_csv("dashboard/main_data_bike_sharing.csv")
# hour_day_df = pd.read_csv("main_data_bike_sharing.csv")

# Menginisiasi min_date dan max_date
hour_day_df["dteday"] = pd.to_datetime(hour_day_df["dteday"]).dt.date
min_date = hour_day_df["dteday"].min()
max_date = hour_day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("dashboard/company-logo.png")
    # st.image("company-logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu :',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    # Menentukan batas jam awal dan akhir untuk grafik yang menggunakan parrameter jam
    values = st.slider('Rentang Jam :',0, 23, (0,23))
    start_hour, end_hour = values

# Menetapkan main_df berdasarkan rentang start_date dan end_date
main_df = hour_day_df[(hour_day_df["dteday"] >= start_date) & 
                (hour_day_df["dteday"] <= end_date)]

# Memasukkan nilai pengembalian fungsi berupa dataframe ke variabel
monthly_rental_count_for_years_df = create_monthly_rental_count_for_years_df(main_df)
mean_hourly_df = create_mean_hourly_df(main_df)
count_rental_df = create_count_rental_df(main_df)

# Menambahkan header
st.header('Bike Sharing Dashboard :bike:')

# Rata-rata peminjaman sepeda berdasarkan hari
st.subheader('Rata-rata peminjaman sepeda berdasarkan hari')
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1:
    try:
        st.metric('Monday', int(round(main_df[main_df['weekday'] == 'Monday'].cnt.mean(), 0)))
    except ValueError:
        st.metric('Monday', 0)

with col2:
    try:
        st.metric('Tuesday', int(round(main_df[main_df['weekday'] == 'Tuesday'].cnt.mean(), 0)))
    except ValueError:
        st.metric('Tuesday', 0)

with col3:
    try:
        st.metric('Wednesday', int(round(main_df[main_df['weekday'] == 'Wednesday'].cnt.mean(), 0)))
    except ValueError:
        st.metric('Wednesday', 0)

with col4:
    try:
        st.metric('Thursday', int(round(main_df[main_df['weekday'] == 'Thursday'].cnt.mean(), 0)))
    except ValueError:
        st.metric('Thursday', 0)

with col5:
    try:
        st.metric('Friday', int(round(main_df[main_df['weekday'] == 'Friday'].cnt.mean(), 0)))
    except ValueError:
        st.metric('Friday', 0)

with col6:
    try:
        st.metric('Saturday', int(round(main_df[main_df['weekday'] == 'Saturday'].cnt.mean(), 0)))
    except ValueError:
        st.metric('Saturday', 0)

with col7:
    try:
        st.metric('Sunday', int(round(main_df[main_df['weekday'] == 'Sunday'].cnt.mean(), 0)))   
    except ValueError:
        st.metric('Sunday', 0)

# Grafik Line Chart jumlah total peminjaman sepeda bulanan tiap tahunnya
st.subheader('Jumlah total peminjaman sepeda bulanan tiap tahunnya')

df_2011 = monthly_rental_count_for_years_df[monthly_rental_count_for_years_df['yr'] == 2011]
df_2012 = monthly_rental_count_for_years_df[monthly_rental_count_for_years_df['yr'] == 2012]

col1,col2,col3 = st.columns(3)
with col1:
    formatted_sum_total_count_2011 = "{:,.0f}".format(df_2011['cnt'].sum()).replace(',', '.')
    st.metric('Total peminjaman 2011', formatted_sum_total_count_2011)

with col2:
    formatted_sum_total_count_2012 = "{:,.0f}".format(df_2012['cnt'].sum()).replace(',', '.')
    st.metric('Total peminjaman 2012', formatted_sum_total_count_2012)

with col3:
    formatted_sum_total_count= "{:,.0f}".format(monthly_rental_count_for_years_df['cnt'].sum()).replace(',', '.')
    st.metric('Total peminjaman Seluruhnya', formatted_sum_total_count)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(
    df_2011['mnth'],
    df_2011['cnt'],
    marker="o",
    label='2011',
    color='orange'
)
ax.plot(
    df_2012['mnth'],
    df_2012['cnt'],
    marker="o",
    label='2012',
    color='red'
)

plt.xlabel('Month')
plt.ylabel('Sum of Total Rental')
plt.xticks(rotation=30)
plt.title('Monthly Bike Rentals Count for Each Year')
plt.grid()
plt.legend()

st.pyplot(fig)

with st.expander("Penjelasan Singkat"):
    st.write(
        "Performa dari data bike sharing cukup positif. Hal ini ditandai dengan naiknya total peminjaman tiap bulan dari tahun sebelumnya. Kenaikan signifikan terjadi pada bulan Februari-Maret 2012, Akan tetapi pada data terakhir tren terlihat menurun dengan Penurunan signifikan terjadi pada bulan Oktober-November 2012."
    )

# Klustering Musim Scatter plot berdasarkan temperature dan jumlah peminjaman sepeda
st.subheader('Klustering Musim berdasarkan temperature dan jumlah peminjaman sepeda')

season_options = st.multiselect(
'Pilih musim (dapat memilih lebih dari satu)',
['Springer', 'Summer', 'Fall', 'Winter'],
['Springer', 'Summer', 'Fall', 'Winter'])

palette = ['green','orange','brown','blue']

fig = plt.figure(figsize=(11, 6))
sns.scatterplot(data=main_df[main_df['season'].isin(season_options)], x='cnt', y='temp', hue="season", palette=palette)

plt.xlabel("Total Rental")
plt.ylabel("Temperature")
plt.title("Season clustering based on temperature and total rent")

st.pyplot(fig)

with st.expander("Penjelasan Singkat"):
    st.write(
        "Pada hasil visualisasi menggunakan scatterplot diatas, dapat dilihat bahwa pengguna banyak melakukan peminjaman sepeda pada musim gugur dan musim panas. Hal ini didasarkan pada keadaan cuaca yang hangat yang membuat pengguna cenderung lebih lama diluar ruangan."
    )

# Grafik line chart Jumlah rata-rata peminjaman sepeda setiap jam
st.subheader('Jumlah rata-rata peminjaman sepeda setiap jam')

fig= plt.figure(figsize=(14, 7))
ax = sns.lineplot(data=mean_hourly_df[(main_df['hr'] >= start_hour)&(main_df['hr'] <= end_hour)], x="hr", y="cnt", color='orange', errorbar=None, marker="o")

plt.xlabel("Hours")
plt.ylabel("Average of total rental")
plt.title("Average Count of Bike Rental per Hour")
plt.grid()

st.pyplot(fig)

with st.expander("Penjelasan Singkat"):
    st.write(
        "Dapat dilihat jam dengan rata-rata peminjaman sepeda terendah pada jam 12 malam hingga 5 pagi. Ini merupakan jam istirahat dan jam tidur bagi seluruh orang. Sedangkan jam dengan rata-rata peminjaman sepeda tertinggi yaitu pada jam 8 pagi, 5 dan 6 sore. Ini merupakan jam dimana orang pergi dan pulang bekerja."
    )

# Grafik line chart Tren jumlah peminjaman pengguna teregistrasi dan pengguna casual setiap jam
st.subheader('Tren jumlah peminjaman pengguna teregistrasi dan pengguna casual setiap jam')

fig = plt.figure(figsize=(14,7))
ax = sns.lineplot(x="hr", y="cnt", data=count_rental_df[(main_df['hr'] >= start_hour)&(main_df['hr'] <= end_hour)], label='Count of Rental')
ax = sns.lineplot(x="hr", y="registered", data=count_rental_df[(main_df['hr'] >= start_hour)&(main_df['hr'] <= end_hour)], label='Registered')
ax = sns.lineplot(x="hr", y="casual", data=count_rental_df[(main_df['hr'] >= start_hour)&(main_df['hr'] <= end_hour)], label='Casual')

plt.xticks([i for i in range(start_hour, end_hour+1)])
plt.xlabel("hours")
plt.ylabel("count of total rental")
plt.title("Bike Rental Trends per Hour")
plt.grid()

st.pyplot(fig)

with st.expander("Penjelasan Singkat"):
    st.write(
        "Dari total peminjaman sepeda dan total penggunanya yang teregistrasi atau kasual. Didapati bahwa hampir semua pengguna telah teregistrasi. Ini menandakan bahwa program peminjaman sepeda atau bike sharing ini merupakan program yang memiliki manfaat berkelanjutan dan memiliki komitmen yang kuat untuk menggunakannya lagi."
    )

st.caption('Copyright (c) Muhamad Meiko Triputra 2024')