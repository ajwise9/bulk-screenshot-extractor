import cv2
import os
import sys
import subprocess
import json

# --- CONFIGURATION ---
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def load_config():
    default_config = {
        "INTERVAL_MINUTES": 0,
        "INTERVAL_SECONDS": 3,
        "SCREENSHOTS_PER_INTERVAL": 1,
        "OUTPUT_FOLDER_NAME": "outputfolder"
    }
    if not os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(default_config, f, indent=4)
            print(f"Created default configuration file at {CONFIG_FILE}")
        except Exception as e:
            print(f"Warning: Could not create config file: {e}")
        return default_config
        
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config.json: {e}. Using defaults.")
        return default_config

config = load_config()

INTERVAL_MINUTES = config.get("INTERVAL_MINUTES", 0)
INTERVAL_SECONDS = config.get("INTERVAL_SECONDS", 3)
SCREENSHOTS_PER_INTERVAL = config.get("SCREENSHOTS_PER_INTERVAL", 1)
OUTPUT_FOLDER_NAME = config.get("OUTPUT_FOLDER_NAME", "outputfolder")
# ---------------------

def extract_frames(video_path):
    # Verify file existence
    if not os.path.exists(video_path):
        print(f"Error: File '{video_path}' not found.")
        return

    file_name = os.path.basename(video_path)
    base_name, _ = os.path.splitext(file_name)
    
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the root output directory
    output_root = os.path.join(script_dir, OUTPUT_FOLDER_NAME)
    
    # Define the specific folder for this video: "outputfolder/{base_name}"
    video_output_dir = os.path.join(output_root, base_name)
    
    if not os.path.exists(video_output_dir):
        os.makedirs(video_output_dir)
        print(f"Created directory: {video_output_dir}")
    else:
        print(f"Output directory already exists: {video_output_dir}")

    # Open video
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Warning: '{file_name}'. Using alternative method to extract frames...")
        
        interval_total_seconds = (INTERVAL_MINUTES * 60) + INTERVAL_SECONDS
        if interval_total_seconds <= 0 or SCREENSHOTS_PER_INTERVAL <= 0:
            print("Error: Invalid configuration for interval or screenshots. Must be greater than 0.")
            return

        screenshots_per_second_rate = SCREENSHOTS_PER_INTERVAL / interval_total_seconds
        
        output_pattern = os.path.join(video_output_dir, "%d.jpg")
        
        try:
            # Native direct ffmpeg frame extraction. -q:v 2 yields high quality jpeg. 
            subprocess.run(
                ["ffmpeg", "-i", video_path, "-vf", f"fps={screenshots_per_second_rate}", "-q:v", "2", "-y", output_pattern],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"✅ FFMPEG Direct Extraction Complete! Saved naturally to '{video_output_dir}'.")
        except subprocess.CalledProcessError:
            print(f"Error: ffmpeg extraction failed for '{file_name}'.")
        except FileNotFoundError:
            print("Error: ffmpeg is not installed on your system. Please install ffmpeg to process this file format.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print("Error: FPS is 0, cannot process.")
        return

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = frame_count / fps
    
    print(f"Processing '{file_name}'")
    print(f"FPS: {fps}")
    print(f"Total Frames: {frame_count}")
    print(f"Duration: {duration_sec:.2f} seconds")
    
    interval_total_seconds = (INTERVAL_MINUTES * 60) + INTERVAL_SECONDS
    if interval_total_seconds <= 0 or SCREENSHOTS_PER_INTERVAL <= 0:
        print("Error: Invalid configuration for interval or screenshots. Must be greater than 0.")
        return

    screenshots_per_second_rate = SCREENSHOTS_PER_INTERVAL / interval_total_seconds

    print(f"Target: {SCREENSHOTS_PER_INTERVAL} screenshot(s) every {INTERVAL_MINUTES} minute(s) and {INTERVAL_SECONDS} second(s)")
    
    saved_count = 0
    current_sec = 0.0
    step_sec = 1.0 / screenshots_per_second_rate
    
    while True:
        # Calculate which frame corresponds to the current second timestamp
        frame_id = int(round(current_sec * fps))
        
        # If we go past the total frames, stop
        if frame_id >= frame_count:
            break
            
        # Set position
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        
        ret, frame = cap.read()
        if not ret:
            # Reached end of video or read error
            break
            
        # Save frame with numerical name starting from 1
        output_filename = os.path.join(video_output_dir, f"{saved_count + 1}.jpg")
        cv2.imwrite(output_filename, frame)
        saved_count += 1
        
        # Move to next timestamp
        current_sec += step_sec

    cap.release()
    print(f"Done! Saved {saved_count} images to '{video_output_dir}'.")

def process_directory():
    # Directory containing the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Target video directory - "videos" subfolder
    video_dir = os.path.join(script_dir, "videos")
    
    if not os.path.exists(video_dir):
        print(f"Error: Could not find 'videos' directory in {script_dir}")
        print("Please place your videos in a 'videos' folder next to this script.")
        return

    # Supported video extensions
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm')
    
    files = [f for f in os.listdir(video_dir) if f.lower().endswith(video_extensions)]
    
    if not files:
        print(f"No video files found in '{video_dir}'.")
        return

    print(f"Found {len(files)} videos in '{video_dir}'. Starting batch processing...")
    
    for video_file in files:
        video_path = os.path.join(video_dir, video_file)
        print("-" * 40)
        try:
            extract_frames(video_path)
        except Exception as e:
            print(f"Failed to process {video_file}: {e}")

if __name__ == "__main__":
    # If arguments are provided, use them, otherwise batch process the "videos" folder
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
        extract_frames(video_path)
    else:
        process_directory()
