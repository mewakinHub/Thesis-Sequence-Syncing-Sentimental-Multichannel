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

def analyze_folder(folder_path, model, output_file):
    """Analyze all images in a folder and save results."""
    results = []
    for img_name in sorted(os.listdir(folder_path)):
        if img_name.endswith(".jpg"):
            img_path = os.path.join(folder_path, img_name)
            emotion = predict_emotion(img_path, model)
            results.append((img_name, emotion))

    with open(output_file, "w") as f:
        for img_name, emotion in results:
            f.write(f"{img_name}: {emotion}\n")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Facial Expression Analysis")
    parser.add_argument("--input", required=True, help="Path to input image or folder")
    parser.add_argument("--output", required=True, help="Path to save the results")
    parser.add_argument("--model", required=True, help="Path to the pre-trained model")
    args = parser.parse_args()

    model = load_model(args.model)

    if os.path.isdir(args.input):
        analyze_folder(args.input, model, args.output)
    else:
        emotion = predict_emotion(args.input, model)
        print(f"Predicted Emotion: {emotion}")
