# Facial Expression Analysis Using Facetorch

This project uses the Facetorch library for analyzing facial expressions in both:
1. Individual images (e.g., JPG files).
2. Consecutive video frames (extracted from a video).

---

## **Setup**
1. Clone the repository:
   ```bash
   cd facial_expression/FERPlus
   git clone https://github.com/tomas-gajarsky/facetorch.git
    ```

# TODO:
// 1. locate model file, then update code

2. Set up the environment:
   ```bash
   conda create -n facial_expression python=3.9 -y
   conda activate facial_expression
   <!-- /mnt/c/Users/<username>/miniconda3/Scripts/conda.exe activate <environment_name> -->
   /mnt/c/Users/mew/miniconda3/Scripts/conda.exe activate facial_expression
   conda install pytorch torchvision opencv -c pytorch -y
   pip install pillow matplotlib opencv-python
   pip install torchaudio==2.3.1
   pip install "numpy<2"


   <!-- cd /path/to/facetorch -->
    cd facial_expression/FERPlus/facetorch
    pip install -e .
   ```
    This installs Facetorch in editable mode, making it usable as a Python module in your scripts.
   ```

3. Download the Pre-Trained Models
provided configuration files (efficientnet_b2_8.yaml and efficientnet_b0_7.yaml
.\facial_expression\FERPlus\facetorch\conf\analyzer\predictor\fer
```bash
# Create the directory to store models
cd facial_expression/FERPlus
pip install gdown

mkdir data\models\1
mkdir data\models\2

# Download EfficientNet-B0 Model
gdown --id 1i5f8vy1dZv_u8vsJsj9CHEzHwsokIknr -O data\models\1\model.pt

# Download EfficientNet-B2 Model
gdown --id 1xoB5VYOd0XLjb-rQqqHWCkQvma4NytEd -O data\models\2\model.pt
```

---

## **Use Cases**
[](../../docs/test_dataset.md)
### **1. Single Image Analysis**
Run the `analyze_emotions.py` script for a single image:

```bash
python scripts/analyze_emotions.py --input ../data/input/image.jpg
```

**Input**:
- `../data/input/image.jpg` (path to your image).

**Output**:
- The emotion prediction is printed to the console.

---

### **2. Video Analysis - Consecutive Frames**
#### Step 1: Extract Frames from Video
Use `extract_frames.py` to extract frames from the video:
```bash
python scripts/extract_frames.py --input ../data/input/video.mp4 --output ../data/input/frames/
```

**Input**:
- `../data/input/video.mp4` (path to your video file).

**Output**:
- Extracted frames are saved in `../data/input/frames/`.

#### Step 2: Analyze the Frames
Run the `analyze_emotions.py` script for the folder of frames:
```bash
python scripts/analyze_emotions.py --input ../data/input/frames/ --output ../data/output/video_results.txt
```

**Input**:
- Folder containing extracted frames (`../data/input/frames/`).

**Output**:
- Results are saved in `../data/output/video_results.txt`.

---

## **Outputs**
1. **Extracted Frames**:
   - Located in: `../data/input/frames/`.
   - Example: `frame_0000.jpg`, `frame_0001.jpg`, etc.

2. **Emotion Scores**:
   - For single images: Printed to the console.
   - For videos: Saved to a file (`../data/output/video_results.txt`).

---

## **Example Commands**
1. Activate your Conda environment in **Command Prompt**:
   ```cmd
   conda activate facial_expression
   ```

2. Run the script for EfficientNet-B0:
   ```cmd
   python scripts\analyze_emotions_with_validation.py --input data\jaffe_converted\ --config conf\analyzer\predictor\fer\efficientnet_b0_7.yaml --output data\output\results_b0.txt
   ```

3. Run the script for EfficientNet-B2:
   ```cmd
   python scripts\analyze_emotions_with_validation.py --input data\jaffe_converted\ --config conf\analyzer\predictor\fer\efficientnet_b2_8.yaml --output data\output\results_b2.txt
   ```

### Single Image:
```bash
python scripts/analyze_emotions.py --input ../data/input/image.jpg

# Single Image:
python scripts/analyze_emotions.py --input data/input/KA.AN1.39.jpg --output data/output/results.txt --model data/models/1/model.pt

# Validate Folder:
python scripts/analyze_emotions_with_validation.py --input data/jaffe_converted/ --output data/output/validation_results.txt --model data/models/1/model.pt
```

---

**Command Without Labels File**
If you don’t have JSON labels, run the following commands:

```cmd
python scripts\analyze_emotions_with_validation.py --input data\video_frames\penguinz0 --output data\output\penguinz0_validation.txt --model data\models\1\model.pt
python scripts\analyze_emotions_with_validation.py --input data\video_frames\michael_reeves --output data\output\michael_reeves_validation.txt --model data\models\1\model.pt
python scripts\analyze_emotions_with_validation.py --input data\video_frames\tommyinnit --output data\output\tommyinnit_validation.txt --model data\models\1\model.pt
python scripts\analyze_emotions_with_validation.py --input data\video_frames\mrballen --output data\output\mrballen_validation.txt --model data\models\1\model.pt
python scripts\analyze_emotions_with_validation.py --input data\video_frames\markiplier_part1 --output data\output\markiplier_part1_validation.txt --model data\models\1\model.pt
python scripts\analyze_emotions_with_validation.py --input data\video_frames\markiplier_part2 --output data\output\markiplier_part2_validation.txt --model data\models\1\model.pt
python scripts\analyze_emotions_with_validation.py --input data\video_frames\logan_paul --output data\output\logan_paul_validation.txt --model data\models\1\model.pt
```

---
**Explanation of Command Components**
- `--input`: Path to the folder containing extracted frames for the specific dataset.
- `--output`: File to save the validation results (per dataset).
- `--model`: Path to the pre-trained model (`model.pt`).
- `--labels`: Optional parameter pointing to a JSON file containing ground truth labels for the dataset.

---

#### Automating for All Datasets
If you have a lot of datasets and want to automate this in **Command Prompt**, you can create a batch script (`validate_all.bat`):

Run it in Command Prompt:
   ```cmd
   validate_all.bat
   ```

---
**Expected Output**
- Extracted frames will be saved in the `data/video_frames/` directory.
- Validation results (predicted emotions for each frame) will be saved in `data/output/video_validation_results.txt`.
---

**Step 5: Inspect Results**
1. Check `results_b0.txt` and `results_b2.txt` in the `data\output\` directory to see predictions.
2. If you want to include ground truth validation (e.g., matching predictions with the labeled emotions from filenames like `KA.HA1.30.jpg`), let me know, and I can further enhance the script.

---

### **Summary**
- You don’t need to use `pip install -e .` for Facetorch.
- Run the script using the provided configurations and downloaded models.
- Use Command Prompt to activate your Conda environment and execute the script.

```
FERPlus/
├── data/
│   ├── label/
│   │   │   ├── penguinz0.json
│   │   │   ├── tommyinnit.json
│   ├── video_frames/
│   │   ├── michael_reeves/
│   │   ├── tommyinnit/
│   │   ├── mrballen/
│   │   ├── markiplier_part1/
│   │   ├── markiplier_part2/
│   │   ├── logan_paul/
│   │   └── penguinz0/
│   └── output/
│       ├── michael_reeves_validation.txt
│       ├── tommyinnit_validation.txt
│       ├── mrballen_validation.txt
│       ├── markiplier_part1_validation.txt
│       ├── markiplier_part2_validation.txt
│       ├── logan_paul_validation.txt
│       └── penguinz0_validation.txt
```
Here’s the command adapted for Windows **Command Prompt (CMD)** and applied to all 7 datasets:

---