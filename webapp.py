import streamlit as st
from Data.data_of_weather import fetch_weather_data  # Import your function to fetch weather data

# Set up your Streamlit app
st.set_page_config(page_title="Weather Data Visualization", layout="wide")

# Title and description
st.title("Weather Data Visualization")
st.markdown("Enter a city name to get the current weather details!")

# Input from the user
city_name = st.text_input("Enter city name", "")

# Fetch weather data and display it
if city_name:
    weather_data = fetch_weather_data(city_name)

    # Check if the data was fetched successfully or if there was an error
    if "error" not in weather_data:
        # Display weather details
        st.subheader(f"Weather in {city_name}")
        st.write(f"Temperature: {weather_data['main']['temp']}°C")
        st.write(f"Weather: {weather_data['weather'][0]['description'].title()}")
        st.write(f"Humidity: {weather_data['main']['humidity']}%")
        st.write(f"Wind Speed: {weather_data['wind']['speed']} m/s")
    else:
        # Display error message if city is not found or there's an error
        st.error(weather_data["error"])
