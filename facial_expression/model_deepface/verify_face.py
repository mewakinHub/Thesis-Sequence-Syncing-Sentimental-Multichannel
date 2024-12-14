# verify_face.py

from deepface import DeepFace
import cv2

def verify_faces(img1_path, img2_path):
    # Load images
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    # Convert BGR to RGB (OpenCV loads images in BGR format)
    img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

    # Perform face verification
    result = DeepFace.verify(img1_rgb, img2_rgb, model_name="VGG-Face", detector_backend="opencv")
    print(f"Are they the same person? {'Yes' if result['verified'] else 'No'}")
    print(f"Confidence Score: {result['distance']}")

def detect_emotion(img_path):
    # Load the image
    img = cv2.imread(img_path)

    # Convert BGR to RGB (DeepFace requires RGB format)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Perform emotion analysis
    analysis = DeepFace.analyze(img_rgb, actions=['emotion'])

    # Get the dominant emotion
    emotion = analysis['dominant_emotion']
    print(f"Detected Emotion: {emotion}")
    print(f"Emotion Scores: {analysis['emotion']}")

if __name__ == "__main__":
    # Paths to images
    # img1_path = "images/img1.jpg"
    # img2_path = "images/img2.jpg"

    # verify_faces(img1_path, img2_path)

    img_path = "images/img1.jpg"
    detect_emotion(img_path)
