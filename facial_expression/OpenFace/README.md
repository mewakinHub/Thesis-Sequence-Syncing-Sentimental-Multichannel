### Step 1: **Instructions to Use the Script**
1. **Save the Script**:
   - Copy the content into a file named `extract_features.sh` in your working directory.

2. **Make the Script Executable**:
   Run this command to give the script execute permissions:
   ```bash
   chmod +x extract_features.sh
   ```

3. **Run the Script**:
   Execute the script in your terminal:
   ```bash
   ./extract_features.sh
   ```

---

### **What the Script Does**
- Changes to the `OpenFace/build` directory.
- Runs the `FeatureExtraction` tool for each video file, saving outputs to the respective output directories under `data/outputs/`.
- Prints a message when the extraction is complete.

---

### **Script: `extract_features.sh`**
```bash
#!/bin/bash

# Navigate to OpenFace build directory
cd OpenFace/build

# Run FeatureExtraction for each video
./bin/FeatureExtraction -f "../../../../input_sample_video/positive (sarcastic) - michael reeves/original clip.mp4" -out_dir "../../data/outputs/michael_reeves/"

./bin/FeatureExtraction -f "../../../../input_sample_video/positive (happy) - tommyinnit/original clip.mp4" -out_dir "../../data/outputs/tommyinnit/"

./bin/FeatureExtraction -f "../../../../input_sample_video/neutral - mrballen/original clip.mp4" -out_dir "../../data/outputs/mrballen/"

./bin/FeatureExtraction -f "../../../../input_sample_video/negative (sad) - markiplier part 1/original clip.mp4" -out_dir "../../data/outputs/markiplier_part1/"

./bin/FeatureExtraction -f "../../../../input_sample_video/negative (sad) - markiplier part 2/original clip.mp4" -out_dir "../../data/outputs/markiplier_part2/"

./bin/FeatureExtraction -f "../../../../input_sample_video/negative (sad) - logan paul/original clip.mp4" -out_dir "../../data/outputs/logan_paul/"

./bin/FeatureExtraction -f "../../../../input_sample_video/negative (angry) - penguinz0/original clip.mp4" -out_dir "../../data/outputs/penguinz0/"

echo "Feature extraction completed for all videos."
```

---

### Step 2: Organize Your Files
Create the following directory structure in your project:

```bash
project/
├── data/
│   ├── labels/               # FERPlus JSON labels
│   │   ├── penguinz0.json
│   │   ├── michael_reeves.json
│   │   ├── ...
│   ├── outputs/              # OpenFace CSV outputs
│   │   ├── penguinz0/
│   │   │   ├── original clip.csv
│   │   │   ├── original clip_of_details.txt
│   │   ├── michael_reeves/
│   │   │   ├── original clip.csv
│   │   │   ├── original clip_of_details.txt
│   │   ├── ... 
│   ├── results/ # Results directory (created automatically)
├── analyze_openface_ferplus.py  # Python script for processing
```
---

### Step 3: Install Required Dependencies
Ensure you have Python and necessary libraries installed:

```bash
pip install pandas numpy
```

---

### Step 4: Run the Script
Execute the script to analyze all videos:

```bash
python analyze_openface_ferplus.py
```

---

### Step 6: Review the Results
The results will be saved in `emotion_results.csv`:

| Video         | Frame        | Confidence | Predicted Emotion | Ground Truth | Correct |
|---------------|--------------|------------|-------------------|--------------|---------|
| penguinz0     | frame_0001   | 0.98       | Angry             | Angry        | True    |
| michael_reeves| frame_0005   | 0.92       | Happy             | Happy        | True    |

---


### Features of the Updated Script

1. **1-Second Interval Sampling:**
   - Uses `resample_to_seconds` to aggregate frames into 1-second intervals based on the video's FPS (assumed to be 30 fps).
   
2. **Ground Truth Integration:**
   - Reads 1-second interval labels from JSON files (like the example you provided).
   - Compares them with detected emotions to compute accuracy.

3. **Separate Results Files:**
   - Saves results for each input video as `results/{video_name}_results.csv`.
   - Overall accuracy for all videos is saved as `results/overall_accuracy.json`.

4. **Handles Missing Data:**
   - Ensures that missing ground truth labels or OpenFace frames don't crash the script.

---

4. Results:
   - Individual emotion results for each video will be saved in `results/{subject_name}_results.csv`.
   - Overall accuracy for all videos will be in `results/overall_accuracy.json`.

---

### Example Output

#### `results/logan_paul_results.csv`
| Second | DetectedEmotion | GroundTruth |
|--------|------------------|-------------|
| 0      | Sad              | Sad         |
| 1      | Neutral          | Neutral     |
| 2      | Angry            | Angry       |

#### `results/overall_accuracy.json`
```json
{
    "logan_paul": 0.85,
    "markiplier_part2": 0.91,
    "penguinz0": 0.87,
    "michael_reeves": 0.89,
    "mrballen": 0.92,
    "tommyinnit": 0.88
}
```