import requests

def fetch_weather_data(city):
    API_KEY = "306a3c740319b380defc4ba64cd24b37"  # Replace with your actual API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    # Print the raw response for debugging
    print(data)

    if response.status_code == 200:
        return data  # Return the weather data if the request was successful
    else:
        return {"error": data.get("message", "An error occurred")}