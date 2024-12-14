import os
import argparse
from facetorch.core import FaceAnalyzer

def analyze_image(image_path, analyzer):
    """
    Analyze a single image and print the predicted emotion.
    """
    image_data = analyzer.run(path_image=image_path)
    if len(image_data.faces) > 0:
        predicted_emotion = image_data.faces[0].preds["emotion"].label
        print(f"Emotion for {image_path}: {predicted_emotion}")
    else:
        print(f"No face detected in {image_path}")
        predicted_emotion = "No face detected"
    return predicted_emotion

def analyze_folder(folder_path, analyzer, output_file):
    """
    Analyze all images in a folder and save results to a file.
    """
    results = []
    for img_name in sorted(os.listdir(folder_path)):
        if img_name.endswith(".jpg"):
            img_path = os.path.join(folder_path, img_name)
            predicted_emotion = analyze_image(img_path, analyzer)
            results.append((img_name, predicted_emotion))

    with open(output_file, "w") as f:
        for img_name, predicted_emotion in results:
            f.write(f"{img_name}: {predicted_emotion}\n")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Facial Expression Analysis")
    parser.add_argument("--input", required=True, help="Path to input image or folder")
    parser.add_argument("--output", required=True, help="Path to save the results")
    parser.add_argument("--config", required=True, help="Path to configuration YAML file")
    args = parser.parse_args()

    # Initialize analyzer
    analyzer = FaceAnalyzer(cfg=args.config)

    if os.path.isdir(args.input):
        analyze_folder(args.input, analyzer, args.output)
    else:
        analyze_image(args.input, analyzer)
