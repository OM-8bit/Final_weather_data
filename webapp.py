import streamlit as st
from Data.data_of_weather import fetch_weather_data  # Import your function to fetch weather data

# Set up your Streamlit app
st.set_page_config(page_title="Weather Data Visualization", layout="wide")

# Initialize session state for dark mode if it doesn't exist
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Function to toggle dark mode
def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

# Add toggle icon in the top right corner
icon = "🌙" if st.session_state.dark_mode else "🌞"
toggle_button = st.button(icon, key="toggle_mode", on_click=toggle_dark_mode, help="Toggle Light/Dark Mode")

# Apply CSS for dark mode if enabled
if st.session_state.dark_mode:
    st.markdown("""
        <style>
            body {
                background-color: black;
                color: white;
            }
            .stButton > button {
                background-color: #444;
                color: white;
            }
            .stTextInput input {
                background-color: #444;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            body {
                background-color: white;
                color: black;
            }
            .stButton > button {
                background-color: #f0f0f0;
                color: black;
            }
            .stTextInput input {
                background-color: white;
                color: black;
            }
        </style>
    """, unsafe_allow_html=True)

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
