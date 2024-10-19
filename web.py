import streamlit as st
from utils import StreamProcess
from streamlit_option_menu import option_menu
import pydeck as pdk

# Use the option menu for sidebar navigation with icons
with st.sidebar:
    selected = option_menu(
        "",
        ["Home", "About", "MVP", "API Keys", "Contact Us"],
        icons=["house", "briefcase", "rocket", "key", "envelope"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#f0f0f5"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#ADD8E6"},
        }
    )

# A dictionary to hold API keys in session state (this will persist for the session)
if 'api_keys' not in st.session_state:
    st.session_state['api_keys'] = {}

# Home Page
if selected == "Home":
    st.title("EmergEye")
    st.write("--Reducing Emergency Response Time by Analyzing Real-Time Video")
    st.video("https://www.youtube.com/watch?v=_vUcdeFFPQU")
    st.markdown("""
The major issue in fatal traffic accident response is the delay caused by the dependence on witnesses or passersby to report accidents. Accidents often go unnoticed for critical minutes.

Traditional methods of accident detection often fail to provide accurate data on the severity of the incident, leading to further delays in medical response and decreasing the accident survival rate.

We create a product that detects fatal accidents by analyzing live stream videos and notifies the first responders immediately. 

""")

# About Page    
elif selected == "About":
    st.title("About Us")
    st.write("EmergEye is built by MIDS students from the School of Information, UC Berkeley.")
    st.image("Team badge white.png", width=150, caption="Our Team")    

    # Pydeck Map showing team member locations
    # st.subheader("Team Locations")

    # Define the coordinates of the three cities
    team_locations = [
        {"lng": -122.3321, "lat": 47.6062, "city": "Seattle, WA"},  # Seattle, WA
        {"lng": -122.6765, "lat": 45.5152, "city": "Portland, OR"},  # Portland, OR
        {"lng": 121.4737, "lat": 31.2304, "city": "Shanghai, China"},  # Shanghai, China
    ]

    # Create the Pydeck chart with the team locations
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=30,  # Approximate center of the map (between the cities)
            longitude=0,  # Adjust longitude to have a better initial focus
            zoom=0.75,
            pitch=50, # Set pitch to 0 for a flat view
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=team_locations,
                get_position='[lng, lat]',
                get_color='[200, 30, 0, 160]',  # Red with some transparency
                get_radius=150000,  # Adjust the radius to 150,000 meters
            ),
        ],
    ))

# API Keys Page
elif selected == "API Keys":
    st.title("Submit API Keys")

    # Create input fields for various API keys
    nysdot_api_key = st.text_input("NYSDOT API Key", type="password")
    llm_api_key = st.text_input("LLM API Key", type="password")
    
    # Store API keys in session state upon submission
    if st.button("Submit API Keys"):
        st.session_state['api_keys']['nysdot_api_key'] = nysdot_api_key
        st.session_state['api_keys']['llm_api_key'] = llm_api_key
        st.success("API Keys have been stored for this session.")

# Contact Us Page    
elif selected == "Contact Us":
    st.title("Contact Us")
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
    
        # Submit button
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write(f"Thanks {name}! We have received your message.")

# MVP Page
elif selected == "MVP":
    # st.title("MVP")
    st.image("logo.png", width=200)
    
    # Check if the NYSDOT API Key is available before proceeding
    if 'nysdot_api_key' in st.session_state['api_keys'] and st.session_state['api_keys']['nysdot_api_key']:
        # Use the stored API key to initialize StreamProcess
        stream_process = StreamProcess(api_key=st.session_state['api_keys']['nysdot_api_key'])

    # Initialize session state variables
    if 'available_cameras' not in st.session_state:
        st.session_state['available_cameras'] = []
    if 'selected_camera' not in st.session_state:
        st.session_state['selected_camera'] = None
    
    # Dropdown for selecting Department of Transportation (DoT)
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
    
            # Display details of the selected camera
            selected_camera = st.session_state['selected_camera']
            st.subheader("Selected Camera Details")
            st.write(f"**Camera ID:** {selected_camera.__dict__['id']}")
            st.write(f"**Name:** {selected_camera.__dict__['name']}")
            st.write(f"**Roadway:** {selected_camera.__dict__.get('roadway', 'Unknown')}")
            st.write(f"**Direction:** {selected_camera.__dict__.get('direction', 'Unknown')}")
            st.write(f"**Latitude:** {selected_camera.__dict__['latitude']}")
            st.write(f"**Longitude:** {selected_camera.__dict__['longitude']}")
            # st.write(f"**Image URL:** {selected_camera.__dict__['image_url']}")
    
            # Placeholder for live camera image
            image_placeholder = st.empty()
    
            # Display the image from the Image URL
            image_placeholder.image(selected_camera.__dict__['image_url'], caption="Live Camera Image")
            
            # Button to preview the live stream
            if st.button("Preview Live Stream"):
                # Clear the live camera image
                image_placeholder.empty()
    
                # Preview live stream
                preview_result = stream_process.preview_live_stream()
                st.write(preview_result)
                # Show a greenish success message
                # st.success("Video preview complete.")
    
            # Button to list associated signs (if any)
            if st.button("List Associated Signs"):
                signs_info = stream_process.list_associated_signs()
                st.write(signs_info)
    
            # Button to start video stream and save the video
            if st.button("Start Video Stream and Save"):
                recording_info = stream_process.save_video_from_stream(duration_seconds=20)
                st.write(recording_info)
                st.success("Frames extracted and Metadata saved")
    else:
        st.warning("Please submit the NYSDOT API Key first in the 'API Keys' section.")






