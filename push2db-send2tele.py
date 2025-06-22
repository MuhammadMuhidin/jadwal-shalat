import os, psycopg2, requests, pytz
from datetime import datetime

class JadwalShalat:
    def __init__(self):
        self.db = os.getenv('NEONDB_URI')
        self.uri_telegram = os.getenv('TELEGRAM_URI')
    
    def fetch_and_store(self):
        tz = pytz.timezone('Asia/Jakarta')
        today = datetime.now(tz).strftime('%Y-%m-%d')
        url_jadwal = f'https://api.myquran.com/v2/sholat/jadwal/1204/{today}'
        uri_husna='https://api.myquran.com/v2/husna/acak'

        try:
            d_jadwal = requests.get(url_jadwal).json()
            d_husna = requests.get(uri_husna).json()

            if d_jadwal.get('status'):
                tanggal = d_jadwal['data']['jadwal']['tanggal']
                lokasi = d_jadwal['data']['lokasi']
                subuh = d_jadwal['data']['jadwal']['subuh']
                terbit = d_jadwal['data']['jadwal']['terbit']
                dhuha = d_jadwal['data']['jadwal']['dhuha']
                dzuhur = d_jadwal['data']['jadwal']['dzuhur']
                ashar = d_jadwal['data']['jadwal']['ashar']
                maghrib = d_jadwal['data']['jadwal']['maghrib']
                isya = d_jadwal['data']['jadwal']['isya']
                asmaul_husna = f"{d_husna['data']['latin']} ({d_husna['data']['indo']})"
                


                data = (lokasi, tanggal, subuh, terbit, dhuha, dzuhur, ashar, maghrib, isya, asmaul_husna)
                conn = psycopg2.connect(self.db)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO jadwal_shalat (lokasi, tanggal, subuh, terbit, dhuha, dzuhur, ashar, maghrib, isya, asmaul_husna)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (tanggal) DO NOTHING
                """, data)
                conn.commit()
                cursor.close()
                conn.close()
                print(f"Data for {tanggal} stored successfully.")

        except Exception as e:
            print(f"Error fetch/store data: {e}")
                
    def read_and_send2telegram(self):
        try:
            conn = psycopg2.connect(self.db)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jadwal_shalat ORDER BY tanggal ASC LIMIT 1")
            jadwal = cursor.fetchone()
            cursor.execute("SELECT COUNT(*) FROM realtime_traffic_sensor")
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()

            if jadwal:
                message = f"""🕌 *Jadwal Shalat Hari Ini*
📅 {jadwal[0]}
📍 Wilayah {jadwal[1]}

🌅 Subuh: {jadwal[2]}
⛅ Terbit: {jadwal[3]}
🌞 Dhuha: {jadwal[4]}
🏙 Dzuhur: {jadwal[5]}
🌇 Ashar: {jadwal[6]}
🌆 Maghrib: {jadwal[7]}
🌃 Isya: {jadwal[8]}
------------------
*Asmaul Husna*
📿 "{jadwal[9]}"
------------------
📊 *Total Data Traffic Sensor:* {count}
"""
                requests.post(self.uri_telegram, json={'msg': message})
                print("Message sent to Telegram.")
            else:
                print("No data found.")

        except Exception as e:
            print(f"Error reading/sending data: {e}")

if __name__ == '__main__':
    jadwal_shalat = JadwalShalat()
    jadwal_shalat.fetch_and_store()
    jadwal_shalat.read_and_send2telegram()

        
