# data_of_weather.py

import requests

def fetch_weather_data(city=None, lat=None, lon=None):
    """
    Fetch weather data for a given city or coordinates (latitude and longitude).
    """
    API_KEY = "306a3c740319b380defc4ba64cd24b37"

    # Determine the API URL based on input (city or coordinates)
    if lat is not None and lon is not None:
        current_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    elif city:
        current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    else:
        return {"error": "Please provide either a city name or latitude and longitude."}

    try:
        # Get current weather data
        current_response = requests.get(current_url)
        current_data = current_response.json()
        print("Current Weather Data (Raw):", current_data)  # Debugging statement

        # Get forecast data
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()
        print("Forecast Data (Raw):", forecast_data)  # Debugging statement

        if current_response.status_code == 200 and forecast_response.status_code == 200:
            # Generate mock hourly data for trends using forecast data
            hourly_trend = [forecast['main']['temp'] for forecast in forecast_data['list'][:8]]
            hourly_humidity_trend = [forecast['main']['humidity'] for forecast in forecast_data['list'][:8]]

            # Combine current data and additional trends
            current_data['hourly_trend'] = hourly_trend
            current_data['hourly_humidity_trend'] = hourly_humidity_trend
            current_data['forecast'] = forecast_data['list']  # Add full forecast data if needed

            return current_data
        else:
            # Return error message from API
            return {"error": current_data.get("message", "An error occurred")}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
