import os
import argparse
import torch
from torchvision import transforms
from PIL import Image

LABELS = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

def load_model(model_path):
    """Load the pre-trained model."""
    model = torch.jit.load(model_path)
    model.eval()
    return model

def preprocess_image(image_path):
    """Preprocess the image for the model."""
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image = Image.open(image_path).convert("RGB")
    return transform(image).unsqueeze(0)

def predict_emotion(image_path, model):
    """Predict the emotion for a single image."""
    input_tensor = preprocess_image(image_path)
    with torch.no_grad():
        output = model(input_tensor)
    _, predicted_idx = torch.max(output, 1)
    return LABELS[predicted_idx.item()]

def parse_ground_truth(file_name):
    """Extract ground truth emotion from the file name."""
    label_code = file_name.split('.')[1][:2]
    mapping = {
        "AN": "Angry",
        "DI": "Disgust",
        "FE": "Fear",
        "HA": "Happy",
        "SA": "Sad",
        "SU": "Surprise",
        "NE": "Neutral",
    }
    return mapping.get(label_code, "Unknown")

def validate_folder(folder_path, model, output_file):
    """Validate predictions for all images in a folder."""
    total_images = 0
    correct_predictions = 0
    results = []

    for img_name in sorted(os.listdir(folder_path)):
        if img_name.endswith(".jpg"):
            img_path = os.path.join(folder_path, img_name)
            ground_truth = parse_ground_truth(img_name)
            predicted_emotion = predict_emotion(img_path, model)

            is_correct = (predicted_emotion == ground_truth)
            correct_predictions += int(is_correct)
            total_images += 1
            results.append((img_name, ground_truth, predicted_emotion, is_correct))

    accuracy = (correct_predictions / total_images) * 100 if total_images > 0 else 0
    with open(output_file, "w") as f:
        f.write(f"Accuracy: {accuracy:.2f}%\n")
        f.write("Image, Ground Truth, Prediction, Correct\n")
        for img_name, ground_truth, predicted_emotion, is_correct in results:
            f.write(f"{img_name}, {ground_truth}, {predicted_emotion}, {is_correct}\n")
    print(f"Results saved to {output_file}")
    print(f"Validation Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate Facial Expression Recognition")
    parser.add_argument("--input", required=True, help="Path to the folder of images")
    parser.add_argument("--output", required=True, help="Path to save validation results")
    parser.add_argument("--model", required=True, help="Path to the pre-trained model")
    args = parser.parse_args()

    model = load_model(args.model)
    validate_folder(args.input, model, args.output)
