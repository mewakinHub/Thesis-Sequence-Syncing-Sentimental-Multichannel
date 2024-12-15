To set up OpenFace for video analysis and test it with video input using **CMD on Windows**, here is the complete step-by-step guide:

---

## **Step 1: Download and Set Up OpenFace**

1. **Clone OpenFace Repository**:
   Open CMD and run:
   ```cmd
   git clone https://github.com/TadasBaltrusaitis/OpenFace.git
   cd OpenFace
   ```

2. **Download Models**:
   Download the pre-trained models required for OpenFace:
   ```cmd
   download_models.bat
   ```
   This will place the necessary model files in the `OpenFace/models` directory.

3. **Install Dependencies**:
   - Ensure you have the following installed:
     - Python 3.7 or higher
     - OpenCV (installed via pip)
     - DLIB (installed via pip)

   Install dependencies in your virtual environment:
   ```cmd
   pip install -r requirements.txt
   ```

4. **Build OpenFace**:
   If you have Visual Studio installed (required for building OpenFace binaries), open the `OpenFace.sln` solution in the root directory and build it. Alternatively, use:
   ```cmd
   build_openface.bat
   ```

---

## **Step 2: Test OpenFace Installation**

1. **Run OpenFace on a Sample Video**:
   Use the following CMD command to process a sample video:
   ```cmd
   OpenFace/build/bin/FaceLandmarkVid.exe -f path/to/video.mp4 -out_dir path/to/output/
   ```

2. **Check Outputs**:
   - OpenFace will generate the following files in the `path/to/output/`:
     - `output.csv`: Contains frame-by-frame facial Action Units (AUs) and other features.
     - `output_features.csv`: Features derived from AU analysis.

---

## **Step 3: Create Validation Code for OpenFace**

Here’s how to modify the validation code to process video inputs and match results with ground truth labels in JSON format.

---

### **Script: `validate_openface_results.py`**
```python
import os
import argparse
import pandas as pd
import json

def validate_openface_results(results_csv, json_labels, output_file):
    """Validate OpenFace results against ground truth labels."""
    # Load ground truth labels
    with open(json_labels, "r") as f:
        labels = json.load(f)
    label_mapping = {entry["frame"]: entry["label"] for entry in labels["ImageLabels"]}

    # Load OpenFace results
    try:
        results = pd.read_csv(results_csv)
    except FileNotFoundError:
        print(f"Error: Results CSV file not found at {results_csv}")
        return

    correct = 0
    total = 0
    validation_results = []

    for _, row in results.iterrows():
        frame_name = f"frame_{int(row['frame']):04d}.jpg"  # Ensure frame name matches
        ground_truth = label_mapping.get(frame_name, "Unknown")
        predicted_emotion = "Neutral"  # Placeholder: Replace with AU-based prediction logic

        is_correct = (ground_truth == predicted_emotion)
        validation_results.append((frame_name, ground_truth, predicted_emotion, is_correct))
        correct += is_correct
        total += 1

    accuracy = (correct / total) * 100 if total > 0 else 0

    # Write validation results to a file
    with open(output_file, "w") as f:
        f.write(f"Accuracy: {accuracy:.2f}%\n")
        f.write("Frame, Ground Truth, Prediction, Correct\n")
        for frame_name, ground_truth, predicted_emotion, is_correct in validation_results:
            f.write(f"{frame_name}, {ground_truth}, {predicted_emotion}, {is_correct}\n")

    print(f"Validation completed. Results saved to {output_file}. Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate OpenFace results against ground truth")
    parser.add_argument("--results", required=True, help="Path to OpenFace results CSV file")
    parser.add_argument("--labels", required=True, help="Path to JSON file containing ground truth labels")
    parser.add_argument("--output", required=True, help="Path to save validation results")
    args = parser.parse_args()

    validate_openface_results(args.results, args.labels, args.output)
```

---

## **Step 4: Test OpenFace with Video Input**

1. **Run OpenFace**:
   Process the video using OpenFace’s `FaceLandmarkVid.exe`:
   ```cmd
   OpenFace/build/bin/FaceLandmarkVid.exe -f input_sample_video/video.mp4 -out_dir data/output/video_analysis/
   ```

2. **Validate Results**:
   Run the validation script using the generated `output.csv`:
   ```cmd
   python validate_openface_results.py --results data/output/video_analysis/output.csv --labels data/labels/video.json --output data/output/video_validation.txt
   ```

---

## **Expected Outputs**

1. **Processed Video Output**:
   - OpenFace will generate:
     - `output.csv`: Frame-wise AUs and features.
     - `landmarks.csv`: Landmark positions for each frame.

2. **Validation Results**:
   - The `video_validation.txt` file will include:
     ```plaintext
     Accuracy: 85.71%
     Frame, Ground Truth, Prediction, Correct
     frame_0000.jpg, Angry, Neutral, False
     frame_0001.jpg, Neutral, Neutral, True
     ...
     ```

---

### Key Notes

- **DeepFace Integration (Optional)**:
  If you want to combine OpenFace with **DeepFace** for emotion prediction, modify the `predicted_emotion` logic to use DeepFace instead of placeholder AU mappings.

- **Error Handling**:
  The script gracefully handles missing labels or frames by defaulting to "Unknown."

- **Adapt for JSON Labels**:
  Ensure JSON files have the structure:
  ```json
  {
      "ImageLabels": [
          {"frame": "frame_0000.jpg", "label": "Angry"},
          {"frame": "frame_0001.jpg", "label": "Neutral"}
      ]
  }
  ```

Let me know if you need further guidance!