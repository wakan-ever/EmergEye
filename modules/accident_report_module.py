import streamlit as st
from PIL import Image
import time
import pandas as pd
from datetime import datetime

# Function to convert lat/long into location (optional, with external API)
def get_location_from_lat_long(latitude, longitude):
    # Placeholder for actual geolocation conversion
    return f"{latitude}, {longitude} (Approximate Location)"

# Function to generate brief notification from CSV
def generate_notification_from_csv(csv_path):
    # Load CSV data
    df = pd.read_csv(csv_path)

    # Extract relevant data from the first row
    frame_name = df.loc[0, 'Frame Name']
    camera_area = df.loc[0, 'Camera Area']
    latitude = df.loc[0, 'Latitude']
    longitude = df.loc[0, 'Longitude']
    timestamp = df.loc[0, 'Timestamp']

    # Extract the camera ID from the Frame Name (before the first underscore)
    camera_id = frame_name.split('_')[0]

    # Convert the timestamp to date and time
    date_part, time_part = timestamp.split('_')
    formatted_date = datetime.strptime(date_part, "%Y-%m-%d").strftime("%Y-%m-%d")
    formatted_time = time_part

    # Get location based on lat/long (can be replaced with a real geolocation API)
    location = get_location_from_lat_long(latitude, longitude)

    # Generate the message
    message = f"""
    A severe accident has been detected at {camera_area}, {location}, on {formatted_date} at {formatted_time} from Camera ID: {camera_id}. 
    Emergency services are urgently needed. Please divert traffic to ensure safety.
    """
    return message

def display_accident_report():
    st.subheader("RESPONDER UI")

    # Check if the notification_ready flag is True
    if 'notification_ready' in st.session_state and st.session_state['notification_ready']:
        # Simulate a push notification animation
        notification_placeholder = st.empty()
        for i in range(5):
            notification_placeholder.info("New accident report incoming...")
            time.sleep(0.5)
            notification_placeholder.empty()
            time.sleep(0.5)

        # Reset the notification flag after the animation
        st.session_state['notification_ready'] = False

    # Check if the brief notification has been fetched
    if 'brief_fetched' not in st.session_state:
        st.session_state['brief_fetched'] = False

    # Button to fetch brief notification
    if st.button("Fetch Brief Notification"):
        # Load and display the accident image
        image_path = "demo/demo.jpg"
        image = Image.open(image_path)
        st.image(image, caption="Accident Image", use_column_width=True)
        
        # Generate the brief notification using the CSV data
        csv_path = "demo/demo.csv"
        brief_notification = generate_notification_from_csv(csv_path)

        # Display brief notification
        st.subheader("Notification (demo):")
        st.markdown(brief_notification)

        # Set session state to indicate the brief notification has been fetched
        st.session_state['brief_fetched'] = True

    # Show the "Fetch Detailed Report" button only after fetching the brief notification
    if st.session_state['brief_fetched']:
        if st.button("Fetch Detailed Report (under development...)"):
            # Display detailed accident report
            st.subheader("Accident Report (demo):")
            st.markdown("""
            - **Location**: Intersection at Waterford Lakes, Orange County, FL
            - **Date and Time**: 2024-10-13 04:36:59
            - **Vehicles Involved**: A large black SUV involved in a rollover incident, with multiple other vehicles (including a white van and a black sedan) nearby but not visibly damaged.
            - **Severity**: The accident appears to be of **severe** severity, as indicated by the overturned SUV, suggesting a high likelihood of significant vehicle damage and potential injuries.
            - **Road Conditions**: The road was dry, and traffic density was moderate at the time of the accident, with no apparent weather-related issues.
            - **Recommendations**: Given the severity of the accident, it is strongly recommended to immediately dispatch emergency services (paramedics, fire rescue, and law enforcement) to the scene. Traffic at the intersection should be temporarily diverted to ensure safety while the scene is cleared and an investigation is conducted.
            """)
