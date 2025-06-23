import os, requests
from datetime import datetime

class WeatherClient:
    telegram_uri = ${{ TELEGRAM_URI}}
    weather_codes = {
        0: "Cerah", 1: "Cerah sebagian", 2: "Berawan", 3: "Berawan tebal",
        45: "Kabut", 48: "Kabut membeku",
        51: "Gerimis", 61: "Hujan ringan", 63: "Hujan sedang", 65: "Hujan lebat",
        80: "Hujan lokal", 95: "Badai"
    }

    def __init__(self, latitude=-6.5, longitude=106.7):
        self.telegram_uri = os.getenv("TELEGRAM_URI")
        self.params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,apparent_temperature,weathercode,precipitation,cloudcover,windspeed_10m",
            "timezone": "Asia/Jakarta"
        }

    def get_weather(self):
        r = requests.get("https://api.open-meteo.com/v1/forecast", params=self.params).json()
        c = r["current"]
        msg = f"""Cuaca saat ini {self.weather_codes.get(c["weathercode"], "?")} | 🌡️ {c["temperature_2m"]}°C (Feels {c["apparent_temperature"]}°C) | 🌧️ {c["precipitation"]} mm | ☁️ {c["cloudcover"]}% | 💨 {c["windspeed_10m"]} km/j"""
        return msg
        
    def send_to_telegram(self):
        msg = self.get_weather()
        res = requests.post(self.telegram_uri, json={"msg": msg})
        res.raise_for_status()  # Optional: biar ketahuan kalau error

if __name__=="__main__":
    cuaca=WeatherClient()
    cuaca.send_to_telegram()
