import streamlit as st
from Data.data_of_weather import fetch_weather_data
import matplotlib.pyplot as plt
import pandas as pd
import geocoder
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

# **Generate Forecast Data**
def generate_forecast_data(weather_data):
    if "forecast" in weather_data:
        forecast = weather_data["forecast"]
        # Adjusted keys based on API response
        forecast_data = {
            "DateTime": [entry.get("dt_txt", "N/A") for entry in forecast],
            "Temperature": [entry.get("main", {}).get("temp", 0) for entry in forecast],
            "Humidity": [entry.get("main", {}).get("humidity", 0) for entry in forecast],
        }
        return pd.DataFrame(forecast_data)
    else:
        # Simulated data if forecast is unavailable
        st.warning("Forecast data unavailable. Using simulated data.")
        simulated_data = {
            "DateTime": pd.date_range(start=pd.Timestamp.now(), periods=10, freq="6H"),
            "Temperature": [30 + i % 5 for i in range(10)],
            "Humidity": [60 + i % 10 for i in range(10)],
        }
        return pd.DataFrame(simulated_data)

if weather_data and "error" not in weather_data:
    # **Current Weather Section**
    st.subheader(f"Current Weather in {city_name or 'your location'}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature (°C)", f"{weather_data['main']['temp']}°C")
    col2.metric("Humidity", f"{weather_data['main']['humidity']}%")
    col3.metric("Wind Speed (m/s)", f"{weather_data['wind']['speed']}")

    st.write(f"**Condition**: {weather_data['weather'][0]['description'].capitalize()}")

    # **Forecast Section**
    forecast_df = generate_forecast_data(weather_data)

    # **Today's Weather Trend**
    st.subheader("Today's Weather Trend")
    today_data = forecast_df[
        pd.to_datetime(forecast_df["DateTime"]).dt.date == pd.Timestamp.now().date()
    ]

    if not today_data.empty:
        col1, col2 = st.columns(2)
        # Temperature trend for today
        col1.subheader("Temperature Trend")
        col1.line_chart(data=today_data, x="DateTime", y="Temperature", use_container_width=True)

        # Humidity trend for today
        col2.subheader("Humidity Trend")
        col2.line_chart(data=today_data, x="DateTime", y="Humidity", use_container_width=True)
    else:
        st.warning("No data available for today's trend.")

    # **5-Day Weather Forecast**
    st.subheader("5-Day Weather Forecast")
    col1, col2 = st.columns(2)

    # **Temperature Trend for Next 5 Days**
    col1.subheader("Temperature Trend")
    col1.line_chart(data=forecast_df, x="DateTime", y="Temperature", use_container_width=True)

    # **Humidity Trend for Next 5 Days**
    col2.subheader("Humidity Trend")
    col2.line_chart(data=forecast_df, x="DateTime", y="Humidity", use_container_width=True)

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

elif weather_data and "error" in weather_data:
    st.error(weather_data["error"])
