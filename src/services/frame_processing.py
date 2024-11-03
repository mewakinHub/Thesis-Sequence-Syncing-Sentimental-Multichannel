import os
import cv2
import time
import pandas as pd
import numpy as np
from pathlib import Path
from src.utils.custom_logger import get_custom_logger

logger = get_custom_logger(__name__)

class FrameProcessing:
    def __init__(self, yolo_inference, post_process, config) -> None:
        self.yolo_inference = yolo_inference
        self.post_process = post_process
        self.conf_threshold = config['CONF_THRESHOLD']
        self.OUTPUT_DIR = 'outputs' # for saving detection results
        self.DETECTION_CSV = os.path.join(self.OUTPUT_DIR, 'detection_frame.csv')
        self.DETECTION_IMAGE_DIR = os.path.join(self.OUTPUT_DIR, 'detection_image')
        os.makedirs(self.DETECTION_IMAGE_DIR, exist_ok=True)  # Ensure the output image directory exists
        self.inference_times = []   # for performance metrics
        self.voting_times = []

    def process_frame(self, frame, frame_counter): # public method: used in VideoProcessing
        # Perform model inference (df has columns: bdbox, class, conf)
        start_time = time.time()
        results = self.yolo_inference.run(frame)
        inference_time = time.time() - start_time
        self.inference_times.append(inference_time)
        logger.debug(f"Inference time: {inference_time:.2f} seconds")

        # Process results (df has columns: bdbox, class, conf, label_name, type_bag)
        df = pd.DataFrame(results[0])
        df['label_name'] = df['class'].map(self.yolo_inference.names)
        df['type_bag'] = df['class'].map(self.yolo_inference.type_bag)
        
        # Perform voting in post_processing (df has columns: bdbox, class, conf, label_name, type_bag, result, sum_conf)
        start_voting_time = time.time()
        df = self.post_process.perform_voting(df)
        voting_time = time.time() - start_voting_time
        self.voting_times.append(voting_time)
        logger.debug(f"Voting time: {voting_time:.4f} seconds")
        
        # Filter out detections with confidence score below configured threshold
        df = df[df['conf'] >= self.conf_threshold] 

        # Filter out detections with result "empty"
        df = df[df['result'] != 'empty']    

        # Check if there are any valid detections
        if df.empty:
            logger.debug("No valid detections in this frame.")
            return df  # Return the empty DataFrame
        
        logger.debug(f"Results Dataframe: \n{df}")

        # Save the frame image if there are valid detections
        detection_image_path = os.path.join(self.DETECTION_IMAGE_DIR, f'frame_{frame_counter}.png')
        cv2.imwrite(detection_image_path, frame)
        logger.debug(f"Saved detection frame to: {detection_image_path}")
        
        # Collect results for CSV
        if not os.path.exists(self.DETECTION_CSV):
            df.to_csv(self.DETECTION_CSV, index=False)
        else:
            df.to_csv(self.DETECTION_CSV, mode='a', header=False, index=False)

        return df

    def draw_tracks(self, tracks, frame, df): # public method: used in VideoProcessing
        """Draws bdbox and text on bags and tags"""  
        for _, row in df.iterrows():
            box_color = (0, 255, 0)
            cv2.rectangle(
                frame,
                (row["bdbox"][0], row["bdbox"][1]),
                (row["bdbox"][2], row["bdbox"][3]),
                box_color,
                2,
            )
            label = f"{row['label_name']}, {row['conf']:.2f}"
            cv2.putText(
                frame,
                label,
                (row["bdbox"][0], row["bdbox"][1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                box_color,
                2,
            )
        """Draws the track IDs on the frame with track data from iou_tracker.py"""
        for track in tracks:
            x1, y1, x2, y2 = track["bdbox"]
            track_id = track["id"]

            # Draw the bounding box with a distinct color
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue box for tracking
        
            # Draw track ID on the top right of the bounding box
            id_text = f"Track ID: {track_id}"
            cv2.putText(frame, id_text, (x2 - 90, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    def log_performance_metrics(self): # public method: used in VideoProcessing
        avg_inference_time = np.mean(self.inference_times)
        q95_inference_time = np.percentile(self.inference_times, 95)
        avg_voting_time = np.mean(self.voting_times)
        q95_voting_time = np.percentile(self.voting_times, 95)

        logger.info(f"Average Inference Time: {avg_inference_time:.4f} seconds")
        logger.info(f"95th Percentile Inference Time: {q95_inference_time:.4f} seconds")
        logger.info(f"Average Voting Time: {avg_voting_time:.4f} seconds")
        logger.info(f"95th Percentile Voting Time: {q95_voting_time:.4f} seconds")