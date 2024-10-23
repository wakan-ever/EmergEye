import streamlit as st
from streamlit_option_menu import option_menu
import pydeck as pdk
from modules import model_module
from modules import video_input_module
from modules import accident_report_module

# Enable wide mode for full-screen layout
st.set_page_config(layout="wide")

# Use the option menu for sidebar navigation with icons
with st.sidebar:
    selected = option_menu(
        "",
        ["Home", "About",  "API Keys", "Our Product", "Contact Us"],
        icons=["house", "briefcase", "key", "rocket",  "envelope"],
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


################## Home Page Section ##################
if selected == "Home":
    st.image("media/Logo.png", width=200)
    st.write("## **EmergEye** – Revolutionizing Emergency Response through Real-Time Traffic Monitoring")
    
    # Embed the video with custom width and height
    video_html = """
    <iframe width="800" height="450" src="https://www.youtube.com/embed/_vUcdeFFPQU" 
    frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; 
    gyroscope; picture-in-picture" allowfullscreen></iframe>
    """
    st.markdown(video_html, unsafe_allow_html=True)
    
    st.markdown("""
Every second counts in emergency response, but traditional methods often rely on bystanders to report accidents, resulting in critical delays.

**EmergEye** harnesses the power of live video stream analysis to detect traffic accidents the moment they happen. By identifying accidents in real-time, we ensure that first responders are notified instantly, drastically reducing response times and saving lives.

With our advanced detection algorithms, EmergEye not only captures the occurrence of accidents but also evaluates their severity, providing responders with the critical information they need to prioritize their efforts.

**Key Benefits:**
- **Real-time detection** of traffic accidents from live streams.
- **Instant alerts** to first responders, minimizing delays.
- **Accurate severity assessment** to prioritize critical cases.
    
Join us in our mission to enhance traffic safety and revolutionize emergency response times with state-of-the-art technology.
""")


################## About Page Section ##################  
elif selected == "About":
    st.title("About Us")
    st.markdown("""
    **EmergEye** is the result of a collaborative effort by students in the Master of Information and Data Science (MIDS) program at the School of Information, UC Berkeley. Our team is united by a shared mission to harness technology in reducing emergency response times and improving road safety through real-time video analytics.
    """)

    st.image("media/Team badge white.png", width=150, caption="Our Team")
    
    st.markdown("""
    **Our Vision**  
    We envision a world where traffic accidents are identified instantly, and first responders can act without delay. By utilizing cutting-edge technology, we aim to transform the future of emergency response and save lives.

    **Our Team**  
    Our diverse team brings together expertise from various cities across the globe. With backgrounds in data science, machine learning, and software development, we are passionate about solving complex problems with innovative solutions.
    """)
    
    # Pydeck Map showing team member locations
    st.subheader("Team Locations")

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
            longitude=0,  # Adjust longitude for better initial focus
            zoom=0.75,
            pitch=50,  # Set pitch to 0 for a flat view
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

    st.markdown("""
    **Team Members**  
    - Seattle, WA: Focused on data integration and cloud infrastructure.  
    - Portland, OR: Leading front-end development and user experience design. 
    - Shanghai, China: Specializing in machine learning and video analytics.
    
    Together, we are proud to bring **EmergEye** to life and contribute to a safer, more responsive world.
    """)

################## API Keys Page Section ##################
elif selected == "API Keys":
    st.title("Submit API Keys")

    # Create input fields for various API keys
    nysdot_api_key = st.text_input("NYSDOT API Key", type="password")
    llm_api_key = st.text_input("LLM API Key (no need for demo)", type="password")
    
    # Store API keys in session state upon submission
    if st.button("Submit API Keys"):
        st.session_state['api_keys']['nysdot_api_key'] = nysdot_api_key
        st.session_state['api_keys']['llm_api_key'] = llm_api_key
        st.success("API Keys have been stored for this session.")

################## Contact Us Page Section ################## 
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

################## MVP Page Section ##################
elif selected == "Our Product":
    # st.title("MVP")

    # Add tabs navigation for MVP
    tabs = st.tabs(["💼 How it works", "🚀 MVP Demo", ])

    with tabs[0]:
        st.header("MVP Diagram")
        st.write("This section will allow you to explore how our product works.")
        st.image("media/diagram.png", width=1000)

    with tabs[1]:         
        # Custom CSS for borders
        st.markdown("""
            <style>
            .module-container {
                border: 2px solid #f0f0f5;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
                background-color: #fafafa;
            }
            .module-title {
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Ensure session state is initialized for analysis and notification flag
        if 'analysis_complete' not in st.session_state:
            st.session_state['analysis_complete'] = False
        
        if 'notification_ready' not in st.session_state:
            st.session_state['notification_ready'] = False

        # Create a container for the entire UI
        with st.container(height=1010, border=True):
            
            # Create two columns: one for the left (video input and model) and one for the right (accident report)
            col_left, col_right = st.columns([2, 1])  # Adjust ratio as needed
        
            # Left Column: Video Input and Model Module
            with col_left:
                # Top section: Video Input Module
                with st.container(height=580, border=True):
                    # st.markdown('<div class="module-container">', unsafe_allow_html=True)
                    st.markdown('<div class="module-title">Live Stream Input</div>', unsafe_allow_html=True)
                    video_input_module.display_video_input()  # Call the video input module
                    st.markdown('</div>', unsafe_allow_html=True)
        
                # Bottom section: Model Module
                with st.container(height=380, border=True):
                    # st.markdown('<div class="module-container">', unsafe_allow_html=True)
                    st.markdown('<div class="module-title">Accident Detection (demo) </div>', unsafe_allow_html=True)
                    model_module.display_model_analysis()  # Call the model analysis module
                    st.markdown('</div>', unsafe_allow_html=True)
        
            # Right Column: Accident Report Module
            with col_right:
                with st.container(height=975, border=True):
                    # st.markdown('<div class="module-container">', unsafe_allow_html=True)
                    # st.markdown('<div class="module-title">Severe Accident Notification</div>', unsafe_allow_html=True)
                    accident_report_module.display_accident_report()  # Call the accident report module
                    st.markdown('</div>', unsafe_allow_html=True)