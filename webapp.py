import streamlit as st
from Data.data_of_weather import fetch_weather_data  # API handled in data_of_weather.py
import matplotlib.pyplot as plt
import pandas as pd
import geocoder
from geopy.geocoders import Nominatim  # For reverse geocoding city names

# Streamlit Page Configuration
st.set_page_config(
    page_title="Weather Data Visualization",
    layout="wide",
    page_icon="Assets/rain.png"
)

# Light/Dark Mode Toggle
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

# Apply Matplotlib Style Based on Mode
mpl_style = "dark_background" if st.session_state.dark_mode else "default"
plt.style.use(mpl_style)

# Title and Input
st.title("🌤️ Weather Data Visualization")
st.markdown("Enter the name of city/state/country or allow location access to get weather details!")

# City Name Input
city_name = st.text_input("Enter city name", "")

# Initialize weather_data
weather_data = None

# Location-Based Input
st.markdown("OR")
if st.button("📍 Use My Location"):
    try:
        g = geocoder.ip('me')  # Get the user's approximate location via IP
        if g.latlng:
            latitude, longitude = g.latlng

            # Reverse Geocoding to Get Location Name
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.reverse((latitude, longitude), exactly_one=True)
            current_location = location.address if location else "Unknown Location"
            
            # Display location details
            st.success(f"Location Detected: {current_location}")
            st.write(f"**Latitude**: {latitude}, **Longitude**: {longitude}")
            
            # Fetch Weather Data
            weather_data = fetch_weather_data(lat=latitude, lon=longitude)
        else:
            st.error("Unable to detect location. Please enter a city name instead.")
    except Exception as e:
        st.error(f"Location access failed: {e}")
else:
    weather_data = fetch_weather_data(city_name) if city_name else None

# Generate Forecast Data
def generate_forecast_data(weather_data):
    if "forecast" in weather_data:
        forecast = weather_data["forecast"]
        forecast_data = {
            "DateTime": [entry.get("dt_txt", "N/A") for entry in forecast],
            "Temperature": [entry.get("main", {}).get("temp", 0) for entry in forecast],
            "Humidity": [entry.get("main", {}).get("humidity", 0) for entry in forecast],
            "Condition": [entry["weather"][0]["description"] for entry in forecast],
        }
        return pd.DataFrame(forecast_data)
    else:
        st.warning("Forecast data unavailable.")
        return pd.DataFrame()

if weather_data and "error" not in weather_data:
    # Current Weather Section
    st.subheader(f"Current Weather in {city_name or current_location}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature (°C)", f"{weather_data['main']['temp']}°C")
    col2.metric("Humidity", f"{weather_data['main']['humidity']}%")
    col3.metric("Wind Speed (km/h)", f"{weather_data['wind']['speed']} km/h")

    st.write(f"**Condition**: {weather_data['weather'][0]['description'].capitalize()}")

    # Forecast Section
    forecast_df = generate_forecast_data(weather_data)

    # Today's Weather Trend
    st.subheader("Today's Weather Trend")
    today_data = forecast_df[
        pd.to_datetime(forecast_df["DateTime"]).dt.date == pd.Timestamp.now().date()
    ]

    if not today_data.empty:
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Temperature trend
        axes[0].plot(
            pd.to_datetime(today_data["DateTime"]),
            today_data["Temperature"],
            label="Temperature (°C)",
            marker="o",
            color="red",
        )
        axes[0].set_title("Temperature Trend")
        axes[0].set_xlabel("Time")
        axes[0].set_ylabel("Temperature (°C)")
        axes[0].grid(color="gray", linestyle="--", linewidth=0.5)
        axes[0].legend()

        # Humidity trend
        axes[1].plot(
            pd.to_datetime(today_data["DateTime"]),
            today_data["Humidity"],
            label="Humidity (%)",
            marker="o",
            color="blue",
        )
        axes[1].set_title("Humidity Trend")
        axes[1].set_xlabel("Time")
        axes[1].set_ylabel("Humidity (%)")
        axes[1].grid(color="gray", linestyle="--", linewidth=0.5)
        axes[1].legend()

        st.pyplot(fig)
    else:
        st.warning("No data available for today's trend.")

    # 5-Day Weather Forecast
    st.subheader("5-Day Weather Forecast")
    col1, col2 = st.columns(2)

    # Temperature Trend for Next 5 Days
    col1.subheader("Temperature Trend")
    col1.line_chart(data=forecast_df, x="DateTime", y="Temperature", use_container_width=True)

    # Humidity Trend for Next 5 Days
    col2.subheader("Humidity Trend")
    col2.line_chart(data=forecast_df, x="DateTime", y="Humidity", use_container_width=True)

    # Daily Max & Min Temperatures
    st.subheader("Daily Max & Min Temperatures")
    daily_stats = forecast_df.groupby("DateTime").agg(
        Max_Temperature=("Temperature", "max"),
        Min_Temperature=("Temperature", "min")
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    daily_stats.plot(kind="bar", ax=ax, color=["red", "blue"], alpha=0.8)
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Daily Max & Min Temperatures")
    ax.grid(color="gray", linestyle="--", linewidth=0.5)
    st.pyplot(fig)

    # Multi-Day Weather Summary
    st.subheader("Multi-Day Weather Summary")
    forecast_df["Date"] = pd.to_datetime(forecast_df["DateTime"]).dt.date
    daily_summary = forecast_df.groupby("Date").agg(
        Avg_Temperature=("Temperature", "mean"),
        Avg_Humidity=("Humidity", "mean"),
        Conditions=("Condition", lambda x: x.mode()[0] if not x.empty else "N/A")
    )
    st.table(daily_summary)

else:
    st.error(weather_data["error"] if weather_data and "error" in weather_data else "Enter a city to get data.")
