import requests
import json
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import numpy as np


class WeatherWatchAI:
    def __init__(self, api_key):
        """
        Initialize the WeatherWatchAI class with the OpenWeatherMap API key.
        """
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast"

    def fetch_weather_data(self, location):
        """
        Fetch real-time weather data for a given location (city name or zip code).
        """
        params = {
            'q': location,
            'appid': self.api_key,
            'units': 'metric'  # Use metric units for temperature (Celsius)
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def predict_next_hour_weather(self, current_weather):
        """
        Predict the weather for the next hour using a simple linear regression model.
        """
        # Extract relevant data
        current_temp = current_weather['main']['temp']
        humidity = current_weather['main']['humidity']
        wind_speed = current_weather['wind']['speed']

        # Dummy data for demonstration (in a real app, use historical data)
        X = np.array([[current_temp, humidity, wind_speed]])
        y = np.array([current_temp + 1])  # Simulate a slight temperature increase

        # Train a simple linear regression model
        model = LinearRegression()
        model.fit(X, y)

        # Predict next hour's temperature
        predicted_temp = model.predict(X)[0]
        return predicted_temp

    def check_severe_weather(self, weather_data):
        """
        Check for severe weather conditions and return alerts if any.
        """
        alerts = []
        weather_id = weather_data['weather'][0]['id']
        temperature = weather_data['main']['temp']

        # Check for severe weather conditions
        if weather_id < 600:  # IDs below 600 indicate rain, snow, or storms
            alerts.append(f"Severe weather alert: {weather_data['weather'][0]['description']}")
        if temperature > 35 or temperature < 0:
            alerts.append(f"Extreme temperature alert: {temperature}°C")

        return alerts

    def display_weather(self, weather_data):
        """
        Display the current weather information.
        """
        if not weather_data:
            print("No weather data available.")
            return

        print("\n--- Current Weather ---")
        print(f"Location: {weather_data['name']}")
        print(f"Temperature: {weather_data['main']['temp']}°C")
        print(f"Humidity: {weather_data['main']['humidity']}%")
        print(f"Wind Speed: {weather_data['wind']['speed']} m/s")
        print(f"Weather Description: {weather_data['weather'][0]['description']}")

    def run(self, location):
        """
        Main function to fetch, predict, and display weather data.
        """
        # Fetch current weather data
        weather_data = self.fetch_weather_data(location)
        if not weather_data:
            return

        # Display current weather
        self.display_weather(weather_data)

        # Predict next hour's weather
        predicted_temp = self.predict_next_hour_weather(weather_data)
        print(f"\n--- Next Hour Prediction ---")
        print(f"Predicted Temperature: {predicted_temp:.2f}°C")

        # Check for severe weather alerts
        alerts = self.check_severe_weather(weather_data)
        if alerts:
            print("\n--- Weather Alerts ---")
            for alert in alerts:
                print(alert)
        else:
            print("\nNo severe weather alerts.")

# Example usage
if __name__ == "__main__":
    api_key = 837d08568e825e3c386d635fc8ee3389
    weather_app = WeatherWatchAI(api_key)

    # Get user input for location
    location = input("Enter a city name or zip code: ")
    weather_app.run(location)

# WeatherWatchAI/
# │
# ├── WeatherWatchAI.py       # Main Python file
# ├── requirements.txt        # List of dependencies
# └── README.md               # Project documentation
