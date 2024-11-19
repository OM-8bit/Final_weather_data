import streamlit as st
from Data.data_of_weather import fetch_weather_data
import matplotlib.pyplot as plt
import pandas as pd
from geopy.geocoders import Nominatim  # To reverse geocode coordinates into city names

# Streamlit Page Configuration
st.set_page_config(
    page_title="Weather Data Visualization",
    layout="wide",
    page_icon="Assets/rain.png"
)

# **Light/Dark Mode Toggle**
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False  # Default mode: Light

# Toggle Button
toggle_label = "🌙 Dark Mode" if not st.session_state.dark_mode else "☀️ Light Mode"
if st.button(toggle_label):
    st.session_state.dark_mode = not st.session_state.dark_mode

# Apply CSS Based on Mode
css_file = "dark_mode.css" if st.session_state.dark_mode else "light_mode.css"
with open(f"Styling_files/{css_file}") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Title and Input
st.title("🌤️ Weather Data Visualization")
st.markdown("Enter the name of city/state/country or allow location access to get weather details!")

# **City Name Input**
city_name = st.text_input("Enter city name", "")

# **Location-Based Input**
st.markdown("OR")
if st.button("📍 Use My Location"):
    try:
        # Use Streamlit's location permissions and Geopy for reverse geocoding
        import geocoder
        g = geocoder.ip('me')  # Get the user's approximate location via IP
        if g.latlng:
            latitude, longitude = g.latlng
            st.success(f"Location Detected: Latitude {latitude}, Longitude {longitude}")
            weather_data = fetch_weather_data(lat=latitude, lon=longitude)
        else:
            st.error("Unable to detect location. Please enter a city name instead.")
    except Exception as e:
        st.error(f"Location access failed: {e}")
else:
    weather_data = fetch_weather_data(city_name) if city_name else None

if weather_data and "error" not in weather_data:
    # **Current Weather Section**
    st.subheader(f"Current Weather in {city_name or 'your location'}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature (°C)", f"{weather_data['main']['temp']}°C")
    col2.metric("Humidity", f"{weather_data['main']['humidity']}%")
    col3.metric("Wind Speed (m/s)", f"{weather_data['wind']['speed']}")

    st.write(f"**Condition**: {weather_data['weather'][0]['description'].capitalize()}")

    # **Temperature Trend Plot for Current Day**
    st.subheader("Simulated Temperature Trend for Today")
    plt.style.use("ggplot" if not st.session_state.dark_mode else "dark_background")
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

elif weather_data and "error" in weather_data:
    st.error(weather_data["error"])
