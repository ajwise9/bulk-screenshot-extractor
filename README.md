# 🎥 bulk-screenshot-extractor 

> **Extract perfect image sequences from multiple videos at once.**

**bulk-screenshot-extractor** is a high-speed tool that processes entire folders of videos, capturing frames at precise intervals and organizing them into clean, numerical sequences.

---

## 🚀 Quick Start

### 1. Setup
Make sure you have Python installed, then install the required library:
```bash
pip install opencv-python
```

### 2. Prepare Videos
Place all your video files (`.mp4`, `.mov`, `.avi`, etc.) inside the **`videos`** folder.

### 3. Run
Execute the script:
```bash
python video_to_frames.py
```

### 4. Results
Check the **`outputfolder`**. You will find a folder for each video containing its extracted frames, numbered sequentially (e.g., `1.jpg`, `2.jpg`, `3.jpg`...).

---

## ⚙️ Configuration

Want more or fewer screenshots? Open `video_to_frames.py` and adjust the configuration at the top:

```python
# --- CONFIGURATION ---
# How many screenshots to extract per second of video
SCREENSHOTS_PER_SECOND = 1  # Change this number! (e.g. 0.5 for every 2 seconds, 2 for twice a second)
```

---

## 📂 Project Structure

```
bulk-screenshot-extractor/
├── video_to_frames.py    # The magic script
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
