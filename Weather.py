import tkinter as tk
from tkinter import messagebox
import requests

# Replace this with your OpenCage Geocoder API Key
OPENCAGE_API_KEY = 'a82a45d95d414a319a10f2459f203616'


# Function to get the coordinates of a town using OpenCage Geocoder API
def get_coordinates(town):
    url = f'https://api.opencagedata.com/geocode/v1/json?q={town}&key={OPENCAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()

    if data['results']:
        # Extract latitude and longitude
        latitude = data['results'][0]['geometry']['lat']
        longitude = data['results'][0]['geometry']['lng']
        return latitude, longitude
    else:
        messagebox.showerror("Error", f"Couldn't find coordinates for {town}")
        return None, None


# Function to get weather data from Open Meteo API
def get_weather(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    response = requests.get(url)
    data = response.json()

    if 'current' in data:
        current_temp = data['current']['temperature_2m']
        wind_speed = data['current']['wind_speed_10m']
        weather_info = f"Current temperature: {current_temp}°C\nWind speed: {wind_speed} km/h"
        return weather_info
    else:
        return "Failed to retrieve weather data"


# Function to handle the user input and display weather info
def on_submit():
    town = town_entry.get()
    if town:
        latitude, longitude = get_coordinates(town)
        if latitude and longitude:
            weather_info = get_weather(latitude, longitude)
            weather_label.config(text=weather_info)
    else:
        messagebox.showerror("Error", "Please enter a town name")


# Create the main window
window = tk.Tk()
window.title("Weather App")
window.geometry("500x400")  # Set the window size
window.config(bg="#2E2E2E")  # Set background color to dark gray

# Create and place the widgets with improved styling
town_label = tk.Label(window, text="Enter Town Name:", font=("Helvetica", 16), fg="#FFFFFF", bg="#2E2E2E")
town_label.pack(pady=15)

town_entry = tk.Entry(window, width=40, font=("Helvetica", 14), bg="#404040", fg="#FFFFFF", bd=2, relief="solid")
town_entry.pack(pady=10)

submit_button = tk.Button(window, text="Get Weather", command=on_submit, font=("Helvetica", 14), bg="#4CAF50", fg="#FFFFFF", width=20, height=2, relief="solid", bd=2)
submit_button.pack(pady=15)

weather_label = tk.Label(window, text="", font=("Helvetica", 16), fg="#FFFFFF", bg="#2E2E2E", wraplength=450, justify="center")
weather_label.pack(pady=20)

# Run the application
window.mainloop()
