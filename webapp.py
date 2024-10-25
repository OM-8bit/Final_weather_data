import streamlit as st
from Data.data_of_weather import fetch_weather_data  # Import your function to fetch weather data

# Title of the app
st.title("Weather Data Visualization")

# User input for city name
city = st.text_input("Enter the city name:", "Delhi")

# Fetch and display weather data
if city:
    weather_data = fetch_weather_data(city)
    st.write(weather_data)  # Display the fetched weather data
