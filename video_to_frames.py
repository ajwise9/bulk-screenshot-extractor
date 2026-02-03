import cv2
import os
import sys

# --- CONFIGURATION ---
# How many screenshots to extract per second of video
SCREENSHOTS_PER_SECOND = 1

# Name of the folder where results will be stored (created in the same directory as this script)
OUTPUT_FOLDER_NAME = "outputfolder"
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
        print("Error: Could not open video.")
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
    print(f"Target: {SCREENSHOTS_PER_SECOND} screenshot(s) per second")
    
    saved_count = 0
    current_sec = 0.0
    step_sec = 1.0 / SCREENSHOTS_PER_SECOND
    
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
