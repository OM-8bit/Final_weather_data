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

    if response.status_code == 200 and 'error' not in data:
        # Generate mock hourly temperature and humidity trends
        hourly_trend = []
        hourly_humidity_trend = []
        base_temp = data['current']['temp_c']
        base_humidity = data['current']['humidity']
        
        for hour in range(24):  # 24 hours for the current day
            temp_variation = random.uniform(-2, 2)  # Simulate small temperature changes
            humidity_variation = random.uniform(-5, 5)  # Simulate small humidity changes
            
            hourly_trend.append(base_temp + temp_variation)
            hourly_humidity_trend.append(max(0, min(100, base_humidity + humidity_variation)))  # Keep within 0-100%
        
        data['hourly_trend'] = hourly_trend  # Add temperature trend
        data['hourly_humidity_trend'] = hourly_humidity_trend  # Add humidity trend
        return data  # Return the weather data if the request was successful
    else:
        return {"error": data.get("error", {}).get("message", "An error occurred")}
