import requests

def fetch_weather_data(city=None, lat=None, lon=None):
    """
    Fetch weather data for a given city or coordinates (latitude and longitude).
    """
    API_KEY = "306a3c740319b380defc4ba64cd24b37"

    if lat is not None and lon is not None:
        current_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    elif city:
        current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    else:
        return {"error": "Please provide either a city name or latitude and longitude."}

    try:
        current_response = requests.get(current_url)
        forecast_response = requests.get(forecast_url)

        current_data = current_response.json()
        forecast_data = forecast_response.json()

        if current_response.status_code == 200 and forecast_response.status_code == 200:
            current_data["forecast"] = forecast_data.get("list", [])
            return current_data
        else:
            return {"error": current_data.get("message", "An error occurred.")}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
