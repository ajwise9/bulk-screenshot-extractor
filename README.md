# 🎥 bulk-screenshot-extractor 

> **Extract perfect image sequences from multiple videos at once.**

**bulk-screenshot-extractor** is a high-speed tool that processes entire folders of videos, capturing frames at precise intervals and organizing them into clean, numerical sequences.

---

## 🚀 Quick Start

### 1. Setup
Make sure you have Python installed. It is recommended to use a virtual environment:
```bash
# Create a virtual environment
python -m venv .venv

# Activate it (Mac/Linux)
source .venv/bin/activate
# Or on Windows:
# .venv\Scripts\activate

# Install the required libraries
pip install -r requirements.txt
```

> **Note on `.mkv` files:** If you are processing `.mkv` files and OpenCV fails to read them natively, the script will automatically invoke `ffmpeg` to transparently convert them to `.mp4` using a lossless stream copy. Make sure you have `ffmpeg` installed on your system if you plan to process these formats.

### 2. Prepare Videos
Place all your video files (`.mp4`, `.mov`, `.avi`, `.mkv`, etc.) inside the **`videos`** folder.

### 3. Run
Execute the script:
```bash
python video_to_frames.py
```

### 4. Results
Check the **`outputfolder`**. You will find a folder for each video containing its extracted frames, numbered sequentially (e.g., `1.jpg`, `2.jpg`, `3.jpg`...).

---

## ⚙️ Configuration

Want more or fewer screenshots? You can configure the exact output logic by opening the `config.json` file (which will be created automatically on first run):

```json
{
    "INTERVAL_MINUTES": 0,
    "INTERVAL_SECONDS": 3,
    "SCREENSHOTS_PER_INTERVAL": 1,
    "OUTPUT_FOLDER_NAME": "outputfolder"
}
```

Example configurations:
- **1 screenshot every 3 seconds**: Set `INTERVAL_SECONDS` to `3` and `SCREENSHOTS_PER_INTERVAL` to `1`
- **10 screenshots per minute**: Set `INTERVAL_MINUTES` to `1` and `SCREENSHOTS_PER_INTERVAL` to `10`


---

## 📂 Project Structure

```
bulk-screenshot-extractor/
├── video_to_frames.py    # The magic script
├── config.json           # Stores your interval settings
├── requirements.txt      # Python dependencies
├── videos/               # PUT YOUR VIDEOS HERE
└── outputfolder/         # GET YOUR IMAGES HERE
    ├── video1/
    │   ├── 1.jpg
    │   └── 2.jpg
    └── video2/
        ├── ...
```

---

## 🎯 Perfect for AI & ML Training

This tool is specifically designed to streamline data collection for:
- **LLM & Vision Model Training**: Quickly generate large datasets of images from raw video.
- **Dataset Labeling**: Compatible with tools like Label Studio or CVAT (images are pre-sorted and numerically named).
- **Fine-tuning**: Extract specific temporal samples for training gesture recognition, object detection, or scene understanding models.
- **Preprocessing**: Handles the heavy lifting of video decoding so you can focus on training.
