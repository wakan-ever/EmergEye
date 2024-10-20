import streamlit as st
from PIL import Image
import time

def display_model_analysis():
    # st.subheader("Model Module")

    # Document upload
    uploaded_file = st.file_uploader("Upload here", type=["jpg", "jpeg", "png", "mp4", "mov"])

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
        if button_clicked:
            with col2:
                if uploaded_file.type.startswith("image"):
                    st.image(image, caption="First visual analysis", use_column_width=True)
                elif uploaded_file.type.startswith("video"):
                    st.video('demo/demo_visual.mp4')
                    st.caption("First visual analysis")

            # In col3, display the analysis phases
            with col3:
                st.write("🔍 Accident detecting:")
                progress_bar1 = st.progress(0)
                for percent in range(100):
                    time.sleep(0.05)
                    progress_bar1.progress(percent + 1)
                time.sleep(2)
                st.write("🧠 Severity analyzing:")
                progress_bar2 = st.progress(0)
                for percent in range(100):
                    time.sleep(0.05)
                    progress_bar2.progress(percent + 1)
                time.sleep(2)
                st.write("✅ Generating the notification")
                progress_bar3 = st.progress(0)
                for percent in range(100):
                    time.sleep(0.05)
                    progress_bar3.progress(percent + 1)
                time.sleep(2)                
                # Once the progress bar finishes, set the session state flag to True
                st.session_state['notification_ready'] = True
                st.write("Analyzing completed ✔️")


