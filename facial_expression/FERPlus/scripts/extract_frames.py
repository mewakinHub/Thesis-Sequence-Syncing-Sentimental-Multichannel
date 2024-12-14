import cv2
import os

def extract_frames(video_path, output_folder, frame_rate=10):
    os.makedirs(output_folder, exist_ok=True)
    video = cv2.VideoCapture(video_path)
    count = 0
    success, frame = video.read()

    while success:
        if count % frame_rate == 0:  # Extract every nth frame (adjust frame_rate)
            frame_filename = os.path.join(output_folder, f"frame_{count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
        success, frame = video.read()
        count += 1

    video.release()
    print(f"Frames extracted to {output_folder}")

# Example usage
if __name__ == "__main__":
    video_path = "../data/input/video.mp4"  # Path to your video
    output_folder = "../data/input/frames/"  # Folder to store frames
    extract_frames(video_path, output_folder, frame_rate=10)

# TODO: label time stamp and do post processing to have the form like OpenFace library output for do syncing with other channels