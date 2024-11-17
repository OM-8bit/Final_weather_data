# webapp.py

import streamlit as st
from Data.data_of_weather import fetch_weather_data
import matplotlib.pyplot as plt
import pandas as pd

# Streamlit Page Configuration
st.set_page_config(
    page_title="Weather Data Visualization",
    layout="wide",
    page_icon="Assets/cloudy.png"
)

# Title and Input
st.title("🌤️ Weather Data Visualization")
st.markdown("Enter the name of city/state/country to get the current weather details!")

city_name = st.text_input("Enter city name", "")

if city_name:
    weather_data = fetch_weather_data(city_name)

    if "error" not in weather_data:
        # **Current Weather Section**
        st.subheader(f"Current Weather in {city_name}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature (°C)", f"{weather_data['main']['temp']}°C")
        col2.metric("Humidity", f"{weather_data['main']['humidity']}%")
        col3.metric("Wind Speed (m/s)", f"{weather_data['wind']['speed']}")

        st.write(f"**Condition**: {weather_data['weather'][0]['description'].capitalize()}")

        # **Temperature Trend Plot for Current Day**
        st.subheader("Simulated Temperature Trend for Today")
        plt.style.use("ggplot")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(weather_data['hourly_trend'], marker='o', color='dodgerblue', linestyle='-', linewidth=2, markersize=5)
        ax.set_xlabel("Hour")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Simulated Hourly Temperature Trend", fontsize=14)
        ax.grid(color='gray', linestyle='--', linewidth=0.5)
        st.pyplot(fig)

        # **Humidity Trend Plot for Current Day**
        st.subheader("Simulated Humidity Trend for Today")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(weather_data['hourly_humidity_trend'], marker='o', color='green', linestyle='-', linewidth=2, markersize=5)
        ax.set_xlabel("Hour")
        ax.set_ylabel("Humidity (%)")
        ax.set_title("Simulated Hourly Humidity Trend", fontsize=14)
        ax.grid(color='gray', linestyle='--', linewidth=0.5)
        st.pyplot(fig)

        # **Forecast Section**
        st.subheader("5-Day Weather Forecast")

        # Process forecast data into a DataFrame
        def process_forecast_data(forecast):
            return pd.DataFrame([
                {
                    "DateTime": item["dt_txt"],
                    "Temperature": item["main"]["temp"],
                    "Humidity": item["main"]["humidity"]
                }
                for item in forecast
            ])

        forecast_df = process_forecast_data(weather_data["forecast"])

        # **Temperature Trend for Next 5 Days**
        st.subheader("5-Day Temperature Trend (3-hour intervals)")
        st.line_chart(data=forecast_df, x="DateTime", y="Temperature", use_container_width=True)

        # **Daily Max & Min Temperatures**
        st.subheader("Daily Max & Min Temperatures")
        forecast_df["Date"] = pd.to_datetime(forecast_df["DateTime"]).dt.date
        daily_stats = forecast_df.groupby("Date").agg({"Temperature": ["max", "min"]})
        daily_stats.columns = ["Max Temp", "Min Temp"]

        fig, ax = plt.subplots(figsize=(10, 6))
        daily_stats.plot(kind="bar", ax=ax, color=["red", "blue"], alpha=0.8)
        ax.set_xlabel("Date")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Daily Max & Min Temperatures")
        ax.grid(color="gray", linestyle="--", linewidth=0.5)
        st.pyplot(fig)

        # **Humidity Trend for Next 5 Days**
        st.subheader("5-Day Humidity Trend (3-hour intervals)")
        st.line_chart(data=forecast_df, x="DateTime", y="Humidity", use_container_width=True)

    else:
        st.error(weather_data["error"])
