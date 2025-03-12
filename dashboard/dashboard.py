import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Memuat dataset
@st.cache_data 
def load_data():
    daily_data = pd.read_csv("day_df.csv")
    hourly_data = pd.read_csv("hour_df.csv")
    
    daily_data['date'] = pd.to_datetime(daily_data['date'])
    hourly_data['date'] = pd.to_datetime(hourly_data['date'])
    
    return daily_data, hourly_data

daily_data, hourly_data = load_data()

def categorize_atemp(atemp_value):
    if atemp_value < 0.3:
        return 'Dingin'
    elif 0.3 <= atemp_value < 0.6:
        return 'Sedang'
    else:
        return 'Panas'

daily_data['kategori_atemp'] = daily_data['atemp'].apply(categorize_atemp)
hourly_data['kategori_atemp'] = hourly_data['atemp'].apply(categorize_atemp)

st.sidebar.markdown("<h1 style='text-align: center; font-size: 80px;'>🚲</h1>", unsafe_allow_html=True)
st.sidebar.title("Pilih Dataset")
selected_dataset = st.sidebar.radio("Pilih dataset:", ("Harian", "Per Jam"))

if selected_dataset == "Harian":
    data = daily_data  
else:
    data = hourly_data 

start_date_default = data["date"].min()
end_date_default = data["date"].max()

start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu', 
    min_value=start_date_default, 
    max_value=end_date_default, 
    value=[start_date_default, end_date_default]
)

filtered_data = data[(data["date"] >= pd.to_datetime(start_date)) & (data["date"] <= pd.to_datetime(end_date))]

def generate_daily_orders(data):
    daily_orders = data.resample(rule='D', on='date').agg({"count": "sum"}).reset_index()
    daily_orders.rename(columns={"count": "total_users"}, inplace=True)
    return daily_orders

def generate_seasonal_data(data):
    seasonal_data = data.groupby(by="season")["count"].sum().reset_index()
    seasonal_data.rename(columns={"count": "total_users"}, inplace=True)
    return seasonal_data

def generate_hourly_data(data):
    if 'hour' in data.columns:
        hourly_data = data.groupby(by="hour")["count"].sum().reset_index()
        hourly_data.rename(columns={"count": "total_users"}, inplace=True)
        return hourly_data
    return pd.DataFrame()


daily_orders_data = generate_daily_orders(filtered_data)
seasonal_data = generate_seasonal_data(filtered_data)
hourly_data = generate_hourly_data(filtered_data)

total_users = daily_orders_data["total_users"].sum()
st.title("🚴‍♂️ Dashboard Penyewaan Sepeda")

with st.expander("ℹ️ Tentang Dashboard"):
    st.write("Dashboard ini menampilkan data penyewaan sepeda berdasarkan berbagai aspek seperti waktu, musim, dan suhu.")


tabs = st.tabs(["📅 Harian", "⏰ Per Jam", "🌤️ Musim", "🌡️ Suhu"])


daily_orders_data = generate_daily_orders(filtered_data)
hourly_data_processed = generate_hourly_data(filtered_data)
seasonal_data = generate_seasonal_data(filtered_data)
temp_category_summary = filtered_data.groupby('kategori_atemp')["count"].sum().reset_index()

# Visualization
with tabs[0]:
    st.subheader("Pengguna Harian")
    st.markdown(f"""
        <div style='display: flex; justify-content: space-around;'>
            <div style='text-align: center;'>📊 <br><b>Rata-rata:</b> {int(daily_orders_data['total_users'].mean())}</div>
            <div style='text-align: center;'>📉 <br><b>Min:</b> {int(daily_orders_data['total_users'].min())}</div>
            <div style='text-align: center;'>📈 <br><b>Max:</b> {int(daily_orders_data['total_users'].max())}</div>
        </div>
    """, unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(daily_orders_data["date"], daily_orders_data["total_users"], marker='o', linewidth=2, color="#42A5F5")
    ax.set_xlabel("Tanggal")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))
    ax.set_ylabel("Total Pengguna")
    st.pyplot(fig)

with tabs[1]:
    st.subheader("Pengguna Berdasarkan Jam")
    if not hourly_data_processed.empty:
        st.markdown(f"""
            <div style='display: flex; justify-content: space-around;'>
                <div style='text-align: center;'>📊 <br><b>Rata-rata:</b> {int(hourly_data_processed['total_users'].mean())}</div>
                <div style='text-align: center;'>📉 <br><b>Min:</b> {int(hourly_data_processed['total_users'].min())}</div>
                <div style='text-align: center;'>📈 <br><b>Max:</b> {int(hourly_data_processed['total_users'].max())}</div>
            </div>
        """, unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(x="hour", y="total_users", data=hourly_data_processed, marker='o', linewidth=2, color="#1E88E5")
        ax.set_xlabel("Jam")
        ax.set_ylabel("Total Pengguna")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center')
        plt.xticks(ticks=range(0, 24), labels=[f"{h % 12 or 12} {'am' if h < 12 else 'pm'}" for h in range(0, 24)], rotation=45)
        st.pyplot(fig)
    else:
        st.warning("Kolom 'hour' tidak ditemukan di dataset.")

with tabs[2]:
    st.subheader("Pengguna Berdasarkan Musim")
    if not seasonal_data.empty:
        st.markdown(f"""
            <div style='display: flex; justify-content: space-around;'>
                <div style='text-align: center;'>📊 <br><b>Rata-rata:</b> {int(seasonal_data['total_users'].mean())}</div>
                <div style='text-align: center;'>📉 <br><b>Min:</b> {int(seasonal_data['total_users'].min())}</div>
                <div style='text-align: center;'>📈 <br><b>Max:</b> {int(seasonal_data['total_users'].max())}</div>
            </div>
        """, unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.barplot(x="season", y="total_users", data=seasonal_data, palette="Blues", ax=ax)
        ax.set_xlabel("Musim")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))
        ax.set_ylabel("Total Pengguna")
        st.pyplot(fig)
    else:
        st.warning("Kolom 'season' tidak ditemukan di dataset.")

with tabs[3]:
    st.subheader("Pengguna Berdasarkan Kategori Suhu")
    st.markdown(f"""
        <div style='display: flex; justify-content: space-around;'>
            <div style='text-align: center;'>🌡️ <br><b>Rata-rata:</b> {int(temp_category_summary['count'].mean())}</div>
            <div style='text-align: center;'>📉 <br><b>Min:</b> {int(temp_category_summary['count'].min())}</div>
            <div style='text-align: center;'>📈 <br><b>Max:</b> {int(temp_category_summary['count'].max())}</div>
        </div>
    """, unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(data=temp_category_summary, x='kategori_atemp', y='count', palette="Blues", ax=ax)
    ax.set_xlabel("Kategori Suhu")
    ax.set_ylabel("Total Pengguna")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))
    st.pyplot(fig)


