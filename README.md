# VisionFlow
# Vehicle Counting Solution - Vehant Research Labs Hackathon

## 📌 Overview
This project is a computer vision solution designed to estimate the total number of vehicles in a traffic video moving away from a static camera. 

* **Challenge Compliance:**
* **Approach:** 100% Classical Image Processing (No Deep Learning/YOLO/CNNs).
* **Technique:** Background Subtraction (MOG2), Morphological Filtering, and Centroid Tracking.
* **Input:** Static camera footage.
* **Output:** Integer count of vehicles.

## ⚙️ Methodology & Pipeline

The solution implements a robust pipeline designed to isolate moving foreground objects (vehicles) from the static background. The process is broken down into five distinct stages:

### 1. Frame Standardization
* **Resizing:** Every input frame is resized to a fixed width of **640px** (maintaining aspect ratio).
* **Reasoning:** This ensures that area-based filtering thresholds (e.g., `area > 1200`) remain consistent regardless of the source video's resolution.

### 2. Pre-processing & Background Modeling
* **Gaussian Blur:** Applied to smooth image noise before processing.
* **MOG2 Background Subtractor:** We utilize `cv2.createBackgroundSubtractorMOG2`. This algorithm models each pixel as a mixture of Gaussians. It adapts to gradual lighting changes and effectively separates moving objects from the static road.
* **Shadow Detection:** The subtractor is configured to detect shadows (`detectShadows=True`). Since shadows can be misclassified as part of the vehicle (distorting the shape), we apply a binary threshold `(250, 255)` to the mask to strictly remove semi-transparent shadow pixels.

### 3. Morphological Operations
Raw background subtraction often produces noisy, fragmented blobs. We apply specific morphological transformations to clean the mask:
* **Erosion:** Removes small white noise (salt noise) from the background.
* **Dilation:** Uses a `15x15` kernel to expand the remaining white pixels. This "heals" the vehicle mask, connecting separated parts (e.g., merging a car's headlights and rear bumper into a single solid blob).

### 4. Contour Filtering (Visual Reasoning)
Once contours are extracted, we apply logical filters to discriminate vehicles from other moving objects (like pedestrians or swaying trees):
* **Area Filter:** We ignore contours with an area `< 1200`. This filters out pedestrians, bikes, or birds.
* **Aspect Ratio Filter:** We ignore objects with an aspect ratio (Width/Height) `< 0.5`. Vehicles moving away generally have a square or horizontal rectangular profile; extremely thin vertical objects are likely noise or pedestrians.

### 5. Centroid Tracking & Counting
* **Virtual Line:** A counting line is established at **50% of the screen height**.
* **Tracking:** The algorithm calculates the centroid (center point) of every valid contour. It compares the current centroids with centroids from the previous frame using Euclidean distance (threshold: `< 60px`) to track the same object.
* **Crossing Logic:** A vehicle is incremented **only if**:
    1.  Its previous Y-position was *below* the line.
    2.  Its current Y-position is *above or on* the line.
    3.  This confirms the direction of motion is **Bottom-to-Top (Moving Away)**.

---

## 🚀 Installation & Setup

### Prerequisites
* Python 3.7+
* Standard libraries listed in `requirements.txt`.

### Installation
1.  Unzip the submission file.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## 💻 How to Run

As per the hackathon guidelines, the `Solution` class is self-contained. However, to test the implementation manually, you can use the following wrapper script:

```python
from main import Solution

# Initialize the solution
solver = Solution()

# Run on a video file
video_path = "path/to/your/traffic_video.mp4"
count = solver.forward(video_path)

print(f"{count}")

