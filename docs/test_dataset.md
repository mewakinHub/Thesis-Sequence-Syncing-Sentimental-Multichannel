#### Manually Labelled Video input:



#### Standard Individual Image input:
If **Facetorch** or any similar model is trained on datasets like FER2013 or FER+ (as is highly likely), then testing it on the same or closely related datasets may not provide a fair or robust evaluation. To ensure a meaningful comparison, it’s better to test Facetorch on **datasets that are independent of FER-like datasets**.

##### **Summary**
- Avoid using FER-related datasets (FER2013, FER+).
- Test on independent datasets like JAFFE, AffectNet, or Multi-PIE.
- This approach ensures unbiased, fair evaluation and demonstrates how well the models generalize to new data.

---

##### **Why Avoid FER-Related Datasets?**
1. **Bias and Overfitting**:
   - If Facetorch was trained on FER2013 or FER+, it will perform exceptionally well on similar data because it has "seen" those types of images during training.
   - This leads to inflated results and doesn’t reflect real-world generalization.

2. **Unfair Benchmarking**:
   - Comparing Facetorch to another model (like OpenFace) on a dataset it was potentially trained on is biased.
   - OpenFace may not have been trained on FER-like datasets, giving Facetorch an unfair advantage.

3. **Generalization**:
   - Testing on diverse, unrelated datasets ensures you evaluate how well the model generalizes to new data.

---

##### **Recommended Independent Datasets**

**1. JAFFE (Japanese Female Facial Expression)**
- **Description**: A dataset of Japanese women expressing 7 emotions.
- **Why Use It?**:
  - Small dataset with distinct features (Japanese subjects, non-FER data).
  - Controlled images with clear expressions.
  - It contains labeled images of facial expressions, ideal for individual image evaluation.
- **Link**: [JAFFE Dataset](https://zenodo.org/record/3451524)


---

### **Step 1: Download the Dataset**

#### **For JAFFE**:
1. Visit the JAFFE dataset link: [JAFFE Dataset on Zenodo](https://zenodo.org/record/3451524).
2. Download the dataset (`jaffe.zip`) to your machine.

#### **Extract the Dataset**:
- Extract the contents of the `jaffe.zip` file into your project directory, such as:
  ```
  data/jaffe/
  ```

---

### **Step 2: Preprocess the Dataset**

The JAFFE dataset consists of labeled images of expressions. You need to organize the dataset for testing.

1. **Ensure Folder Structure**:
   ```
   data/
   ├── jaffe/
   │   ├── KA.HA1.30.tiff  # Example file (Happy expression from person KA)
   │   ├── KB.SA2.30.tiff  # Example file (Sad expression from person KB)
   │   ├── ... (more .tiff files)
   ```

2. **Convert Images (Optional)**:
   If the images are not in `.jpg` format, convert them using the following script:
    [](./../facial_expression/FERPlus/scripts/convert_images.py)
    python scripts/convert_images.py

---

### **Step 3: Modify the `analyze_emotions.py` Script**

Update your script to test Facetorch on JAFFE images:

#### Add Command-Line Parsing for Dataset Evaluation
Update `analyze_emotions.py` to work with a dataset folder:
```python
import os
from facetorch.api import FacialExpressionRecognition
import argparse

def analyze_image(image_path, model):
    result = model.predict(image_path)
    print(f"Emotion for {image_path}: {result}")
    return result

def analyze_folder(folder_path, model, output_file):
    results = []
    for img_name in sorted(os.listdir(folder_path)):
        if img_name.endswith(".jpg"):
            img_path = os.path.join(folder_path, img_name)
            result = analyze_image(img_path, model)
            results.append((img_name, result))

    # Save results to a file
    with open(output_file, "w") as f:
        for img_name, result in results:
            f.write(f"{img_name}: {result}\n")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Facial Expression Analysis on Dataset")
    parser.add_argument("--input", required=True, help="Path to input image or folder")
    parser.add_argument("--output", required=True, help="Path to save the results")
    args = parser.parse_args()

    # Initialize the FER model
    fer_model = FacialExpressionRecognition()

    if os.path.isdir(args.input):
        # Analyze a folder of images
        analyze_folder(args.input, fer_model, args.output)
    else:
        # Analyze a single image
        analyze_image(args.input, fer_model)
```

---

### **Step 4: Run the Analysis**

1. **Single Image**:
   To analyze a single image:
   ```bash
   python scripts/analyze_emotions.py --input data/jaffe/KA.HA1.30.jpg --output results.txt
   ```

2. **Folder of Images**:
   To analyze the entire dataset:
   ```bash
   python scripts/analyze_emotions.py --input data/jaffe_converted/ --output data/output/jaffe_results.txt
   ```

---

### **Step 5: Evaluate and Compare**

1. **Analyze Results**:
   - Open `jaffe_results.txt` to check predictions.
   - Compare them with the ground truth labels (based on file names, e.g., `HA` = Happy, `SA` = Sad).

2. **Benchmark Against OpenFace**:
   - Follow a similar procedure to test JAFFE images with OpenFace.
   - Compare:
     - Accuracy of predictions.
     - Consistency across multiple test cases.

---

### **Step 6: Visualize Results (Optional)**

Use a confusion matrix or bar chart to compare results. Here's an example script to create a confusion matrix:

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Replace with your ground truth and predictions
true_labels = ["Happy", "Sad", "Angry", "Happy", ...]
predicted_labels = ["Happy", "Neutral", "Angry", "Happy", ...]

cm = confusion_matrix(true_labels, predicted_labels, labels=["Happy", "Sad", "Angry", "Neutral", "Surprise"])
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Happy", "Sad", "Angry", "Neutral", "Surprise"])
disp.plot(cmap=plt.cm.Blues)
plt.show()
```

---

### **Next Steps**
1. Download and prepare JAFFE or another independent dataset.
2. Run the updated scripts for both Facetorch and OpenFace.
3. Compare and document results for your advisor.

Let me know if you’d like help with any specific step!