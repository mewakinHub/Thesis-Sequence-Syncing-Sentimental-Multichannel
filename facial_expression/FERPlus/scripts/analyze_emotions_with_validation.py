import os
import argparse
from facetorch.core import FaceAnalyzer

LABEL_MAP = {
    "AN": "Angry",
    "DI": "Disgust",
    "FE": "Fear",
    "HA": "Happy",
    "SA": "Sad",
    "SU": "Surprise",
    "NE": "Neutral"
}

def parse_ground_truth(file_name):
    """
    Extract ground truth emotion from the file name.
    """
    label_code = file_name.split('.')[1][:2]
    return LABEL_MAP.get(label_code, "Unknown")

def validate_folder(folder_path, analyzer):
    """
    Validate all images in a folder and calculate accuracy.
    """
    total_images = 0
    correct_predictions = 0
    results = []

    for img_name in sorted(os.listdir(folder_path)):
        if img_name.endswith(".jpg"):
            img_path = os.path.join(folder_path, img_name)
            ground_truth = parse_ground_truth(img_name)
            image_data = analyzer.run(path_image=img_path)
            if len(image_data.faces) > 0:
                predicted_emotion = image_data.faces[0].preds["emotion"].label
            else:
                predicted_emotion = "No face detected"

            is_correct = (predicted_emotion == ground_truth)
            correct_predictions += int(is_correct)
            total_images += 1
            results.append((img_name, ground_truth, predicted_emotion, is_correct))

    accuracy = (correct_predictions / total_images) * 100 if total_images > 0 else 0
    return results, accuracy

def save_results(results, output_file, accuracy):
    """
    Save validation results to a file.
    """
    with open(output_file, "w") as f:
        f.write(f"Accuracy: {accuracy:.2f}%\n")
        f.write("Image, Ground Truth, Prediction, Correct\n")
        for img_name, ground_truth, predicted_emotion, is_correct in results:
            f.write(f"{img_name}, {ground_truth}, {predicted_emotion}, {is_correct}\n")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Facial Expression Validation")
    parser.add_argument("--input", required=True, help="Path to input folder")
    parser.add_argument("--output", required=True, help="Path to save the validation results")
    parser.add_argument("--config", required=True, help="Path to configuration YAML file")
    args = parser.parse_args()

    # Initialize analyzer
    analyzer = FaceAnalyzer(cfg=args.config)

    # Validate folder
    results, accuracy = validate_folder(args.input, analyzer)
    save_results(results, args.output, accuracy)
    print(f"Validation Accuracy: {accuracy:.2f}%")
