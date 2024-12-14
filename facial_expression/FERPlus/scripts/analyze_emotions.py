import torch
from torchvision import transforms
from PIL import Image
import os
import argparse
import csv

def preprocess_image(image_path):
    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    img = Image.open(image_path)
    return preprocess(img).unsqueeze(0)

def analyze_emotions(input_folder, model_path, output_csv):
    model = torch.load(model_path)
    model.eval()

    results = []
    for img_file in sorted(os.listdir(input_folder)):
        img_path = os.path.join(input_folder, img_file)
        input_tensor = preprocess_image(img_path)
        
        with torch.no_grad():
            output = model(input_tensor)
            emotion_scores = output.numpy().tolist()[0]
            results.append([img_file] + emotion_scores)

    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Frame"] + [f"Emotion_{i}" for i in range(len(emotion_scores))])
        writer.writerows(results)
    print(f"Emotion analysis results saved to {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to folder with input images")
    parser.add_argument("--model", required=True, help="Path to FER+ model (.pt)")
    parser.add_argument("--output", required=True, help="Path to output CSV")
    args = parser.parse_args()

    analyze_emotions(args.input, args.model, args.output)
