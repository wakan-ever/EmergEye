import streamlit as st
from PIL import Image
import time

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

        # Display brief notification
        st.subheader("Notification (demo):")
        st.markdown("""
        A severe accident has been detected at the intersection at Waterford Lakes, Orange County, FL on 2024-10-13 at 04:36:59. Emergency services are urgently needed. Please divert traffic to ensure safety.  
        """)

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
