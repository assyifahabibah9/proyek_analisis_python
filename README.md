# 🚴‍♂️ Bike Sharing Analytics Dashboard

## 📌 Overview
Dashboard ini dirancang untuk menganalisis pola penyewaan sepeda berdasarkan berbagai faktor seperti cuaca, waktu, dan musim. Dibangun dengan Python dan Streamlit, dashboard ini menawarkan visualisasi data yang interaktif dan informatif.

## 🚀 Getting Started
### 1. Prerequisites
Pastikan Python (versi 3.7 atau lebih baru) sudah terinstal di sistem.

### 2. Install Required Library
Jalankan perintah berikut untuk menginstal library yang diperlukan:
```sh
pip install streamlit pandas numpy matplotlib seaborn
```

### 3. Run the Dashboard
Gunakan perintah berikut untuk menjalankan dashboard:
```sh
streamlit run dashboard.py
```

### 4. Mengakses Dashboard
Setelah dijalankan, dashboard akan otomatis terbuka di browser default.

## Key Features
- **Data Visualization**: Menampilkan pola penyewaan sepeda berdasarkan berbagai faktor.
- **Time Analysis**: Tren penyewaan berdasarkan harian, jam, musim dan suhu.
- **Interactive Filters**: Memungkinkan eksplorasi data dengan filter dinamis.
- **Weather Impact**: Analisis pengaruh musim terhadap jumlah penyewaan.
- **Temperature Trends**: Analisis penyewaan berdasarkan suhu yang dirasakan.
- **Seasonal Trends**: Analisis penyewaan berdasarkan musim.
- **Hourly Trends**: Analisis penyewaan berdasarkan jam (hanya tersedia untuk dataset per jam).

## Struktur Projek
```
projek_submission
├───dashboard/
│   ├───dashboard.py             
│   ├───day_df.csv              
│   └───hour_df.csv 
├───data 
│   ├───day.csv             
│   └───hour.csv           
├───notebook.ipynb               
├───README.md                    
├───requirements.txt             
└───url.txt                      
```