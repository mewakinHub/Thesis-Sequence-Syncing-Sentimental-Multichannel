import cv2
import os
import argparse

def extract_frames(video_path, output_folder, sampling_rate):
    """
    Extract frames from a video at a specific sampling rate.

    Args:
        video_path (str): Path to the input video.
        output_folder (str): Path to save extracted frames.
        sampling_rate (int): Sampling rate in seconds.
    """
    os.makedirs(output_folder, exist_ok=True)
    video = cv2.VideoCapture(video_path)
    frame_rate = int(video.get(cv2.CAP_PROP_FPS))
    frame_count = 0
    extracted_count = 0

    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Save frame at every `sampling_rate` seconds
        if frame_count % (frame_rate * sampling_rate) == 0:
            frame_path = os.path.join(output_folder, f"frame_{extracted_count:04d}.jpg")
            cv2.imwrite(frame_path, frame)
            extracted_count += 1

        frame_count += 1

    video.release()
    print(f"Extracted {extracted_count} frames to {output_folder}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from video.")
    parser.add_argument("--input", required=True, help="Path to input video file.")
    parser.add_argument("--output", required=True, help="Path to output folder for frames.")
    parser.add_argument("--rate", type=int, default=1, help="Frame sampling rate in seconds.")
    args = parser.parse_args()

    extract_frames(args.input, args.output, args.rate)
