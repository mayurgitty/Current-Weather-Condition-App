#used customtkinter instead of tkinter.
import requests
import customtkinter as ctk
from tkinter import messagebox
from geopy.geocoders import Nominatim

def get_coordinates(city):
    """Convert city name to latitude & longitude."""
    geolocator = Nominatim(user_agent="weather_assistant")
    location = geolocator.geocode(city)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    lat, lon = get_coordinates(city)
    if lat is None or lon is None:
        messagebox.showerror("Error", "City not found. Please check the name.")
        return

    API_URL = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(API_URL)

    if response.status_code == 200:
        data = response.json()
        weather = data["current_weather"]
        temp = weather["temperature"]
        wind_speed = weather["windspeed"]
        conditions = weather["weathercode"]

        result_text.set(f"Weather in {city}:\n 🌡️\tTemperature: {temp}°C\n🍃\t Wind Speed: {wind_speed} km/h\n🔢\t Condition Code: {conditions}")
    else:
        messagebox.showerror("Error", "Error fetching weather data.")

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Mayur's Weather App")
root.geometry("600x400")

city_label = ctk.CTkLabel(root, text="Enter City Name:", font=("Arial", 20))
city_label.pack(pady=10)

city_entry = ctk.CTkEntry(root, font=("Arial", 20), width=350)
city_entry.pack(pady=5)

fetch_button = ctk.CTkButton(root, text="Get Weather", font=("Arial", 20), command=get_weather)
fetch_button.pack(pady=10)

result_text = ctk.StringVar()
result_label = ctk.CTkLabel(root, textvariable=result_text, font=("Arial", 20), wraplength=350, justify="left")
result_label.pack(pady=10)

root.mainloop()
