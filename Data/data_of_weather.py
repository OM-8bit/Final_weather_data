# data_of_weather.py

import requests
import random  # For creating sample trend data

def fetch_weather_data(city):
    API_KEY = "538a3b8c371640cca4944944242610"  # Replace with your actual API key
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"

    response = requests.get(url)
    data = response.json()

    # Print the raw response for debugging
    print(data)

    if response.status_code == 200:
        # Access the current temperature from the API data
        base_temp = data['current']['temp_c']

        # Generate a mock hourly temperature trend for visualization
        hourly_trend = []
        for hour in range(24):  # 24 hours for the current day
            temp_variation = random.uniform(-2, 2)  # Simulate small temperature changes
            hourly_trend.append(base_temp + temp_variation)
        
        data['hourly_trend'] = hourly_trend  # Add to main data object for easy access
        return data  # Return the weather data if the request was successful
    else:
        return {"error": data.get("error", {}).get("message", "An error occurred")}
