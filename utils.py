import os
import cv2
import time
import datetime
import pytz
import boto3
import csv
from PIL import Image
import streamlit as st
from traffic import API

bucket_name = "capstone-mids-datasets"
bucket_buffer_directory = "capstone-inference/buffer/"
bucket_inference_directory = "capstone-inference/inference/"
cache_directory = "capstone-cache/"
video_recording_output_path = "./temp/"
if not os.path.exists(video_recording_output_path):
    os.makedirs(video_recording_output_path)


class StreamProcess:
    def __init__(self, api_key, local_timezone="America/New_York"):
        """
        Initializes the CameraStreamer class with API key and timezone.
        """
        self.local_timezone = pytz.timezone(local_timezone)
        self.api = API(api_key)
        self.s3_client = boto3.client("s3")
        self.selected_camera = None

    def search_camera_by_road(self, road_name):
        """
        Searches for cameras by road name.
        """
        cameras = self.api.get_cameras()
        available_cameras = [
            cam for cam in cameras if road_name in cam.__dict__.get("name", "")
        ]

        if available_cameras:
            return available_cameras
        else:
            return []

    def select_camera(self, available_cameras, camera_choice):
        """
        Selects a camera from the list of available cameras by index.
        """
        if 0 <= camera_choice < len(available_cameras):
            self.selected_camera = available_cameras[camera_choice]
            camera_info = f"\nYou have selected the following camera:\n"
            camera_info += f"**Camera ID:** {self.selected_camera.__dict__['id']}\n"
            camera_info += f"**Name:** {self.selected_camera.__dict__['name']}\n"
            camera_info += f"**Roadway:** {self.selected_camera.__dict__.get('roadway', 'Unknown Roadway')}\n"
            camera_info += f"**Direction:** {self.selected_camera.__dict__.get('direction', 'Unknown Direction')}\n"
            camera_info += f"**Latitude:** {self.selected_camera.__dict__['latitude']}, Longitude: {self.selected_camera.__dict__['longitude']}\n"
            camera_info += f"**Image URL:** {self.selected_camera.__dict__['image_url']}\n"
            camera_info += f"**Video URL:** {self.selected_camera.__dict__['video_url']}\n"
            return camera_info
        else:
            return "Invalid selection. Please try again."

    def list_associated_signs(self):
        """
        Lists the associated signs for the selected camera's roadway.
        """
        if not self.selected_camera:
            return "No camera selected."

        signs = self.api.get_signs()
        camera_roadway = self.selected_camera.__dict__.get("roadway", "")
        associated_signs = [
            sign for sign in signs if sign.__dict__.get("roadway", "") == camera_roadway
        ]

        if associated_signs:
            signs_info = f"Camera on {camera_roadway} has the following associated signs:\n"
            for sign in associated_signs:
                signs_info += f"  Sign ID: {sign.__dict__.get('id', 'Unknown')}\n"
                signs_info += f"  Name: {sign.__dict__.get('name', 'Unknown')}\n"
                signs_info += f"  Messages: {sign.__dict__.get('messages', 'No messages')}\n"
                signs_info += "-" * 40 + "\n"
            return signs_info
        else:
            return f"No signs associated with {camera_roadway}"

    def preview_live_stream(self, duration_seconds=5, fps=10):
        """
        Captures a preview of the video stream by extracting frames for a few seconds.
        """
        if not self.selected_camera:
            return "No camera selected."

        video_url = self.selected_camera.__dict__["video_url"]
        cap = cv2.VideoCapture(video_url)

        if not cap.isOpened():
            return "Failed to open video stream."

        frame_display = st.empty()  # Placeholder for displaying frames
        max_frames = int(fps * duration_seconds)
        frame_count = 0

        while frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to RGB (since OpenCV loads images in BGR format)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert frame to a PIL image
            pil_img = Image.fromarray(frame_rgb)

            # Display the frame using Streamlit
            frame_display.image(pil_img, caption=f"Frame {frame_count + 1}", use_column_width=True)

            frame_count += 1
            time.sleep(1 / fps)  # Delay to simulate frame rate

        cap.release()
        # return "Video preview complete."
        return ""

    def save_video_from_stream(self, duration_seconds=20):
        """
        Saves a video stream from the selected camera for the specified duration and extracts frames.
        """
        if not self.selected_camera:
            return "No camera selected."

        timezone = self.local_timezone
        video_url = self.selected_camera.__dict__["video_url"]
        cap = cv2.VideoCapture(video_url)

        if not cap.isOpened():
            return "Failed to open video stream."

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 20.0  # Default FPS
        max_frames = int(fps * duration_seconds)
        current_time = datetime.datetime.now(timezone).strftime("%Y-%m-%d_%H-%M-%S")
        camera_id = self.selected_camera.__dict__["id"]
        output_filename = f"{camera_id}_{current_time}.mp4"
        output_file_path = f"{video_recording_output_path}{output_filename}"

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(
            output_file_path, fourcc, fps, (frame_width, frame_height)
        )

        frame_count = 0
        while frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                continue
            out.write(frame)
            frame_count += 1

        cap.release()
        out.release()

        self.upload_video_to_s3(output_file_path, bucket_name, f"{cache_directory}{output_filename}")

        # After video is saved, extract frames and upload them
        csv_filename = f"{camera_id}_{current_time}_frames_metadata.csv"
        output_csv_path = f"{video_recording_output_path}{csv_filename}"
        self.extract_frames_and_upload(
            output_file_path, output_csv_path, frames_per_second=4
        )

        return f"Recording complete. Video saved as {output_filename}"
        # return " "

    def extract_frames_and_upload(self, video_file_path, output_csv_path, frames_per_second=4, duration_seconds=20):
        """
        Extracts frames from the video at a specific frame rate and uploads both frames and metadata to S3.
        """
        video_capture = cv2.VideoCapture(video_file_path)

        if not video_capture.isOpened():
            print(f"Failed to open video file: {video_file_path}")
            return

        # Get video properties
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        video_duration = total_frames / fps

        # Calculate the time intervals where we want to extract frames
        target_times = [
            i / frames_per_second for i in range(frames_per_second * duration_seconds)
        ]

        # Metadata from camera
        camera_id = self.selected_camera.__dict__["id"]
        latitude = self.selected_camera.__dict__["latitude"]
        longitude = self.selected_camera.__dict__["longitude"]
        name = self.selected_camera.__dict__["name"]

        # Extract timestamp from video filename
        video_filename = os.path.basename(video_file_path)
        timestamp = (
            video_filename.split(".")[0].split("_")[1]
            + "_"
            + video_filename.split(".")[0].split("_")[2]
        )

        frame_count = 0
        image_count = 0
        csv_data = []

        for time_sec in target_times:
            video_capture.set(cv2.CAP_PROP_POS_MSEC, time_sec * 1000)
            ret, frame = video_capture.read()
            if not ret:
                print(f"Warning: Failed to grab frame at {time_sec} seconds, skipping...")
                continue

            image_count += 1
            image_filename = f"{camera_id}_{timestamp}_im{image_count}.jpg"
            image_filepath = f"{video_recording_output_path}{image_filename}"

            # Save frame as a .jpg image
            cv2.imwrite(image_filepath, frame)

            # Upload frame to S3
            self.s3_client.upload_file(
                image_filepath,
                bucket_name,
                f"{bucket_buffer_directory}{image_filename}",
            )
            self.s3_client.upload_file(
                image_filepath,
                bucket_name,
                f"{bucket_inference_directory}{image_filename}",
            )
            print(f"Frame {image_count} uploaded: {image_filename}")

            # Save metadata for the CSV
            csv_data.append([image_filename.split(".")[0], name, latitude, longitude, timestamp])

        video_capture.release()

        # Write CSV file with metadata
        with open(output_csv_path, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(
                ["Frame Name", "Camera Name", "Latitude", "Longitude", "Timestamp"]
            )
            csvwriter.writerows(csv_data)

        # Upload CSV to S3
        self.s3_client.upload_file(
            output_csv_path,
            bucket_name,
            f"{bucket_inference_directory}frames_metadata.csv",
        )
        print(f"CSV file uploaded to s3://{bucket_name}/{bucket_inference_directory}frames_metadata.csv")

    def upload_video_to_s3(self, file_path, s3_bucket, s3_key):
        """
        Uploads a file to an S3 bucket.
        """
        if not os.path.exists(file_path):
            return f"Error: {file_path} does not exist."

        try:
            self.s3_client.upload_file(file_path, s3_bucket, s3_key)
            return f"File uploaded successfully to s3://{s3_bucket}/{s3_key}"
        except Exception as e:
            return f"Error uploading file to S3: {str(e)}"


