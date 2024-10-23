import streamlit as st
from PIL import Image
import time

def display_model_analysis():
    # st.subheader("Model Module")
    
    # Check if the session state has the result of the analysis to avoid clearing it after rerun
    if 'analysis_complete' not in st.session_state:
        st.session_state['analysis_complete'] = False

    # Create a placeholder for the file uploader
    upload_placeholder = st.empty()

    # Display file uploader only if a file has not been uploaded yet
    if 'uploaded_file' not in st.session_state:
        uploaded_file = upload_placeholder.file_uploader("Upload here", type=["jpg", "jpeg", "png", "mp4", "mov"])
        if uploaded_file is not None:
            st.session_state['uploaded_file'] = uploaded_file  # Store the file in session state
            upload_placeholder.empty()  # Clear the file uploader after upload
    else:
        uploaded_file = st.session_state['uploaded_file']  # Retrieve the uploaded file from session state

    if uploaded_file is not None:
        col1, col2, col3 = st.columns([2, 2, 1])  # Adjust column widths as needed

        # Display the uploaded image/video in col1
        with col1:
            if uploaded_file.type.startswith("image"):
                image = Image.open(uploaded_file)
                st.image(image, caption="uploaded image", use_column_width=True)
            elif uploaded_file.type.startswith("video"):
                st.video(uploaded_file)
                st.caption("uploaded video")

        # Button to trigger the display in col2
        button_clicked = st.button("Analyze")
        if button_clicked or st.session_state['analysis_complete']:
            st.session_state['analysis_complete'] = True

            with col2:
                if uploaded_file.type.startswith("image"):
                    st.image(image, caption="First visual analysis", use_column_width=True)
                elif uploaded_file.type.startswith("video"):
                    st.video('demo/demo_visual.mp4')
                    st.caption("First visual analysis")

            # In col3, display the analysis phases
            with col3:
                # Phase 1: Accident detecting
                if 'phase1_complete' not in st.session_state:
                    st.write("🔍 Accident detecting:")
                    progress_bar1 = st.progress(0)
                    for percent in range(100):
                        time.sleep(0.05)
                        progress_bar1.progress(percent + 1)
                    time.sleep(2)
                    st.session_state['phase1_complete'] = True  # Mark phase 1 as done
                else:
                    st.write("🔍 Accident detecting completed ✔️")

                # Phase 2: Severity analyzing
                if 'phase2_complete' not in st.session_state:
                    st.write("🧠 Severity analyzing:")
                    progress_bar2 = st.progress(0)
                    for percent in range(100):
                        time.sleep(0.05)
                        progress_bar2.progress(percent + 1)
                    time.sleep(2)
                    st.session_state['phase2_complete'] = True  # Mark phase 2 as done
                else:
                    st.write("🧠 Severity analyzing completed ✔️")

                # Phase 3: Generating the notification
                if 'phase3_complete' not in st.session_state:
                    st.write("✅ Generating the notification")
                    progress_bar3 = st.progress(0)
                    for percent in range(100):
                        time.sleep(0.05)
                        progress_bar3.progress(percent + 1)
                    time.sleep(2)
                    st.session_state['notification_ready'] = True
                    st.session_state['phase3_complete'] = True  # Mark phase 3 as done
                    st.write("Analyzing completed ✔️")
                else:
                    st.write("✅ Notification generated ✔️")