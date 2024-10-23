import streamlit as st
from modules.utils import StreamProcess
import time

def display_video_input():
    # Check if the NYSDOT API Key is available before proceeding
    if 'nysdot_api_key' in st.session_state['api_keys'] and st.session_state['api_keys']['nysdot_api_key']:
        # Use the stored API key to initialize StreamProcess
        stream_process = StreamProcess(api_key=st.session_state['api_keys']['nysdot_api_key'])

        # Initialize session state variables
        if 'available_cameras' not in st.session_state:
            st.session_state['available_cameras'] = []
        if 'selected_camera' not in st.session_state:
            st.session_state['selected_camera'] = None

        # Create a three-column layout
        col1, col2, col3 = st.columns([1, 1, 1])

        # Left column: DoT camera selection and search
        with col1:
            st.title("DoT Camera Selection")
            dot_city = st.selectbox(
                "Select DoT State:",
                ["", "New York State DoT"],  # Currently, only New York State DoT is available
                index=0
            )

            # Ensure the user has selected a valid option before proceeding
            if dot_city:
                # Input for road name to search for cameras
                road_name = st.text_input("Enter Area to Search for Cameras:")

                # Search and display available cameras when the button is pressed
                if st.button("Search Cameras"):
                    st.session_state['available_cameras'] = stream_process.search_camera_by_road(road_name)

                if st.session_state['available_cameras']:
                    # Dropdown to select a camera from the available options
                    camera_options = {f"{cam.__dict__['name']} (ID: {cam.__dict__['id']})": idx for idx, cam in enumerate(st.session_state['available_cameras'])}
                    selected_camera_option = st.selectbox("Select a Camera", list(camera_options.keys()))

                    # Retrieve the selected camera
                    st.session_state['selected_camera'] = st.session_state['available_cameras'][camera_options[selected_camera_option]]

                    # Set the selected camera in the StreamProcess object
                    stream_process.selected_camera = st.session_state['selected_camera']

        # Middle column: display selected camera details
        with col2:
            if 'selected_camera' in st.session_state and st.session_state['selected_camera']:
                selected_camera = st.session_state['selected_camera']
                st.subheader("Camera Details")
                st.write(f"**Camera ID:** {selected_camera.__dict__['id']}")
                st.write(f"**Name:** {selected_camera.__dict__['name']}")
                st.write(f"**Roadway:** {selected_camera.__dict__.get('roadway', 'Unknown')}")
                st.write(f"**Direction:** {selected_camera.__dict__.get('direction', 'Unknown')}")
                st.write(f"**Lat./Long.:** {selected_camera.__dict__['latitude']}, {selected_camera.__dict__['longitude']}")
                # Placeholder for live camera image
                image_placeholder = st.empty()
                # Display the image from the Image URL
                image_placeholder.image(selected_camera.__dict__['image_url'], caption="Live Camera Image")

        # Right column: action buttons
        with col3:
            if 'selected_camera' in st.session_state and st.session_state['selected_camera']:
                st.subheader("Actions")

                # Button to preview the live stream
                if st.button("Preview Live Stream"):
                    # Clear the live camera image
                    image_placeholder.empty()

                    # Preview live stream
                    preview_result = stream_process.preview_live_stream()
                    st.write(preview_result)

                # Button to list associated signs (if any)
                if st.button("List Associated Signs"):
                    signs_info = stream_process.list_associated_signs()
                    st.write(signs_info)

                # Button to start video stream and save the video
                if st.button("Start Video Stream and Save"):
                    # recording_info = stream_process.save_video_from_stream(duration_seconds=20)
                    recording_info = fake_save_video_stream(duration_seconds=10)  # for the demo purpose
                    st.write(recording_info)
                    st.success("Frames extracted and Metadata saved (simulated)")

    # Handle case where the API key is missing
    else:
        st.warning("Please submit the NYSDoT API Key first in the 'API Keys' section.")

# A fake function to simulate saving the video stream
def fake_save_video_stream(duration_seconds=10):
    # Simulate some time delay with a progress bar for the demo
    progress_bar = st.progress(0)
    
    for i in range(100):
        time.sleep(duration_seconds / 100)  # Simulate progress over the duration
        progress_bar.progress(i + 1)
    
    # Simulate a successful operation after the delay
    return " "