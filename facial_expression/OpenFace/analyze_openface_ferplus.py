import pandas as pd
import os
import json

# Universal Emotion Labels
LABELS = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

# AU to Emotion Mapping
AU_MAPPING = {
    "Happy": [("AU06_c", 1), ("AU12_c", 1)],
    "Sad": [("AU01_c", 1), ("AU04_c", 1), ("AU15_c", 1)],
    "Angry": [("AU04_c", 1), ("AU05_c", 1), ("AU07_c", 1)],
    "Surprise": [("AU01_c", 1), ("AU02_c", 1), ("AU05_c", 1)],
    "Fear": [("AU01_c", 1), ("AU02_c", 1), ("AU04_c", 1), ("AU05_c", 1)],
    "Disgust": [("AU09_c", 1), ("AU10_c", 1)],
    "Neutral": [],
}

# Function to determine emotion based on AUs
def determine_emotion(row):
    for emotion, rules in AU_MAPPING.items():
        if all(row.get(au, 0) == val for au, val in rules):
            return emotion
    return "Unknown"

# Process a single video folder
def process_video(folder_path, label_json, result_dir):
    csv_path = os.path.join(folder_path, "original clip.csv")
    labels = json.load(open(label_json))["ImageLabels"]

    # Load OpenFace CSV
    df = pd.read_csv(csv_path)
    results = []

    # Process rows at 1-second intervals
    for i, label in enumerate(labels):
        frame_number = i
        row = df.iloc[min(frame_number * 30, len(df) - 1)]  # Assuming 30 FPS
        prediction = determine_emotion(row)
        confidence = row['confidence']
        
        results.append({
            "Image": label["frame"],
            "Ground Truth": label["label"],
            "Prediction": prediction,
            "Confidence": confidence,
            "Correct": prediction == label["label"]
        })

    # Calculate accuracy
    correct_predictions = sum(1 for r in results if r["Correct"])
    total_predictions = len(results)
    accuracy = correct_predictions / total_predictions if total_predictions else 0

    # Add accuracy as the header
    result_file = os.path.join(result_dir, f"{os.path.basename(folder_path)}_results.csv")
    with open(result_file, "w") as f:
        f.write(f"Accuracy: {accuracy:.2%}\n")
    pd.DataFrame(results).to_csv(result_file, index=False, mode='a')

    print(f"Results saved to {result_file} with Accuracy: {accuracy:.2%}")

# Main function to process all outputs
def process_all_outputs(outputs_dir, labels_dir, results_dir):
    os.makedirs(results_dir, exist_ok=True)

    for folder in os.listdir(outputs_dir):
        folder_path = os.path.join(outputs_dir, folder)
        label_json = os.path.join(labels_dir, f"{folder}.json")
        if os.path.isdir(folder_path) and os.path.exists(label_json):
            print(f"Processing: {folder}")
            process_video(folder_path, label_json, results_dir)

# Paths
OUTPUTS_DIR = "./data/outputs"
LABELS_DIR = "./data/labels"
RESULTS_DIR = "./data/results"

# Run script
if __name__ == "__main__":
    process_all_outputs(OUTPUTS_DIR, LABELS_DIR, RESULTS_DIR)
