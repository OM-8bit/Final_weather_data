# webapp.py

import streamlit as st
from Data.data_of_weather import fetch_weather_data
import matplotlib.pyplot as plt

# Set up Streamlit app with a theme and wide layout and add animated favicon
st.set_page_config(
    page_title="Weather Data Visualization",
    layout="wide",
    page_icon="Assets\cloudy.png"  # Add the path to your animated icon
)

# Title with Emoji
st.title("🌤️ Weather Data Visualization")
st.markdown("Enter a city name to get the current weather details!")

# Input from the user
city_name = st.text_input("Enter city name", "")

# Fetch weather data and display it
if city_name:
    weather_data = fetch_weather_data(city_name)

    # Check if the data was fetched successfully or if there was an error
    if "error" not in weather_data:
        # Display weather details in a visually appealing layout
        st.subheader(f"Weather in {city_name}")

        # Create three columns for better layout
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature (°C)", f"{weather_data['current']['temp_c']}°C")
        col2.metric("Humidity", f"{weather_data['current']['humidity']}%")
        col3.metric("Wind Speed (km/h)", f"{weather_data['current']['wind_kph']}")

        st.write(f"**Condition**: {weather_data['current']['condition']['text']}")
        
        # Temperature Trend Plot with Enhanced Styling
        st.subheader("Temperature Trend for Today")
        plt.style.use("ggplot")  # Updated style
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # Plot hourly temperature trend
        ax.plot(weather_data['hourly_trend'], marker='o', color='dodgerblue', linestyle='-', linewidth=2, markersize=5)
        ax.set_xlabel("Hour")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Simulated Hourly Temperature Trend", fontsize=14)
        ax.grid(color='gray', linestyle='--', linewidth=0.5)
        st.pyplot(fig)
        
        # Humidity Trend Plot
        st.subheader("Humidity Trend for Today")
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # Plot hourly humidity trend
        ax.plot(weather_data['hourly_humidity_trend'], marker='o', color='green', linestyle='-', linewidth=2, markersize=5)
        ax.set_xlabel("Hour")
        ax.set_ylabel("Humidity (%)")
        ax.set_title("Simulated Hourly Humidity Trend", fontsize=14)
        ax.grid(color='gray', linestyle='--', linewidth=0.5)
        st.pyplot(fig)

        # Optional: Minor styling adjustments for visual consistency
        st.markdown(
            """
            <style>
            .css-18e3th9 {
                background-color: #f5f5f5;
                color: #333;
                font-family: Arial, sans-serif;
            }
            </style>
            """, unsafe_allow_html=True
        )

    else:
        # Display error message if city is not found or there's an error
        st.error(weather_data["error"])
