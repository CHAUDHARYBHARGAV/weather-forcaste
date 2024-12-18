import tkinter as tk
from tkinter import ttk, messagebox
import requests

# OpenWeatherMap API key
API_KEY = "1030cd7d6373448a281ef0b5befe5618"

# Function to fetch weather data
def get_weather():
    city = city_entry.get()
    if not city.strip():
        messagebox.showerror("Error", "Please enter a city name.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        weather = {
            "City": data["name"],
            "Temperature": f"{data['main']['temp']}°C",
            "Feels Like": f"{data['main']['feels_like']}°C",
            "Weather": data["weather"][0]["description"].capitalize(),
            "Humidity": f"{data['main']['humidity']}%",
            "Wind Speed": f"{data['wind']['speed']} m/s"
        }

        # Display the weather data
        display_weather(weather)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch weather data:\n{e}")
    except KeyError:
        messagebox.showerror("Error", "City not found. Please try again.")

# Function to display weather data in the same window
def display_weather(weather):
    for widget in result_frame.winfo_children():
        widget.destroy()

    for key, value in weather.items():
        ttk.Label(result_frame, text=f"{key}: {value}", font=("Arial", 12)).pack(anchor="w", pady=2)

# Main App Window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")
root.configure(bg="#f0f4f7")

# Title
title_label = tk.Label(root, text="Weather App", font=("Helvetica", 20, "bold"), bg="#5cb85c", fg="white", pady=10)
title_label.pack(fill=tk.X)

# Input Frame
input_frame = ttk.Frame(root, padding=20)
input_frame.pack(fill=tk.X, pady=10)

city_label = ttk.Label(input_frame, text="Enter City Name:", font=("Arial", 12))
city_label.grid(row=0, column=0, sticky="w", padx=5)
city_entry = ttk.Entry(input_frame, font=("Arial", 12))
city_entry.grid(row=0, column=1, sticky="ew", padx=5)
input_frame.columnconfigure(1, weight=1)

get_weather_button = ttk.Button(input_frame, text="Get Weather", command=get_weather)
get_weather_button.grid(row=0, column=2, padx=5)

# Result Frame
result_frame = ttk.Frame(root, padding=20)
result_frame.pack(fill=tk.BOTH, expand=True)

# Footer
footer_label = tk.Label(root, text="Powered by OpenWeatherMap API", font=("Arial", 10), bg="#f0f4f7", fg="gray")
footer_label.pack(side=tk.BOTTOM, pady=10)

# Key Bindings
city_entry.bind("<Return>", lambda event: get_weather())

# Run the App
root.mainloop()
