# webapp.py

import streamlit as st
from Data.data_of_weather import fetch_weather_data
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Weather Data Visualization",
    layout="wide",
    page_icon="Assets/cloudy.png"
)

st.title("🌤️ Weather Data Visualization")
st.markdown("Enter the name of city/state/country to get the current weather details!")

city_name = st.text_input("Enter city name", "")

if city_name:
    weather_data = fetch_weather_data(city_name)

    if "error" not in weather_data:
        st.subheader(f"Weather in {city_name}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature (°C)", f"{weather_data['main']['temp']}°C")
        col2.metric("Humidity", f"{weather_data['main']['humidity']}%")
        col3.metric("Wind Speed (m/s)", f"{weather_data['wind']['speed']}")

        st.write(f"**Condition**: {weather_data['weather'][0]['description'].capitalize()}")

        # Temperature Trend Plot
        st.subheader("Temperature Trend for Today")
        plt.style.use("ggplot")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(weather_data['hourly_trend'], marker='o', color='dodgerblue', linestyle='-', linewidth=2, markersize=5)
        ax.set_xlabel("Hour")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Simulated Hourly Temperature Trend", fontsize=14)
        ax.grid(color='gray', linestyle='--', linewidth=0.5)
        st.pyplot(fig)

        # Humidity Trend Plot
        st.subheader("Humidity Trend for Today")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(weather_data['hourly_humidity_trend'], marker='o', color='green', linestyle='-', linewidth=2, markersize=5)
        ax.set_xlabel("Hour")
        ax.set_ylabel("Humidity (%)")
        ax.set_title("Simulated Hourly Humidity Trend", fontsize=14)
        ax.grid(color='gray', linestyle='--', linewidth=0.5)
        st.pyplot(fig)

        # Forecast Display
        st.subheader("5-Day Forecast (Every 3 hours)")
        forecast_days = []
        for i in range(0, len(weather_data['forecast']), 8):  # Display data every 24 hours (8 * 3 = 24 hours)
            forecast = weather_data['forecast'][i]
            forecast_days.append({
                "Date": forecast['dt_txt'],
                "Temp": forecast['main']['temp'],
                "Condition": forecast['weather'][0]['description'].capitalize()
            })

        for forecast in forecast_days:
            st.write(f"**{forecast['Date']}**: {forecast['Temp']}°C, {forecast['Condition']}")

    else:
        st.error(weather_data["error"])
