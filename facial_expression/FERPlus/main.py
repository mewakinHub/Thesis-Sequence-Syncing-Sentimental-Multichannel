from scripts.extract_frames import extract_frames
from scripts.analyze_emotions import analyze_video_frames
from utils.config import INPUT_VIDEO_PATH, OUTPUT_FOLDER

if __name__ == "__main__":
    # Step 1: Extract frames
    extract_frames(INPUT_VIDEO_PATH, OUTPUT_FOLDER)
    
    # Step 2: Analyze emotions
    results = analyze_video_frames(OUTPUT_FOLDER)
    print("Emotion analysis completed.")
