import time
import cv2
import numpy as np
from src.utils.custom_logger import get_custom_logger

logger = get_custom_logger(__name__)

class VideoProcessing:
    def __init__(self, CONFIG, read_camera, frame_processing, count_bag, tracker):
        # dependencies injection here
        self.interval_result_limit = CONFIG.get('INTERVAL_RESULT_LIMIT', 10)  # Limit for interval results, prevents memory bloating
        self.read_camera = read_camera
        self.frame_processing = frame_processing
        self.tracker = tracker 
        self.count_bag = count_bag

        self.interval_results = []     # caching: To store interval results
        self.last_counted_type = None  # displaying: Track the last counted type for overlay
        self.tracking_times = []       # performance: To store tracking times
        self.display_times = []        # performance: To store dispaly times

    def run(self):
        frame_counter = 0
        for df, frame in self.read_camera.run():
            frame_counter += 1
            if frame is None:
                break
            self.__process_frame(df, frame)
            logger.info(f"Processing tracker on frame {frame_counter}")
            start_time = time.time()    # Start measuring display_time
            self.__display_frame(frame, df)  
            display_time = time.time() - start_time
            self.display_times.append(display_time) 
            logger.debug(f"display_time time: {display_time:.4f} seconds")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.count_bag.save_results()
                cv2.destroyAllWindows()
                return

    def __process_frame(self, df, frame):
        # for tracking, use only bag bdbox
        detections = df[df['class'] == 0][['bdbox']].to_dict('records')
        
        start_tracking_time = time.time()   # Start measuring tracking time
        dead_tracks = self.tracker.update(detections)
        tracking_time = time.time() - start_tracking_time
        self.tracking_times.append(tracking_time) 
        logger.debug(f"tracking time: {tracking_time:.4f} seconds")

        for track in self.tracker.tracks:
            track_id = track['id']
            track_df = df[df['class'] == 0].copy()
            track_df['track_id'] = track_id
            self.interval_results.append(track_df)

            # Apply caching limit
            if len(self.interval_results) > self.interval_result_limit:
                self.interval_results.pop(0)  # Remove the oldest frame to maintain the limit

        # Check if any track has exceeded max_age and trigger counting logic
        if dead_tracks:
            self.__process_interval_results()

    def __process_interval_results(self):
        if self.interval_results:
            best_frame = self.count_bag.select_best_frame(self.interval_results)
            if best_frame is not None:
                self.last_counted_type = best_frame['result'].iloc[0]
                self.count_bag.update_count(best_frame)
            else:
                logger.warning("No best frame found in interval results.")
        self.interval_results.clear()

    def __display_frame(self, frame, df):
        # Manages the overall video processing workflow.

        # use tracker data for drawing in frame processing
        # provides the tracking data needed by frame_processing.py.
        self.frame_processing.draw_tracks(self.tracker.tracks, frame, df)

        # Overlay for bag counts    
        overlay_text = "Current Counts:\n"
        y_offset = 30
        for bag_type, count in self.count_bag.bag_counts.items():
            if bag_type == "bag":  # Skip the "bag" category
                continue

            # Separate each count with a new line
            color = (0, 255, 0) if bag_type != self.last_counted_type else (50, 205, 50)  # Light green for the last counted
            overlay_text += f"{bag_type}: {count}\n"
            cv2.putText(frame, f"{bag_type}: {count}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            y_offset += 30  # Increment offset for each line

        # Display total counted bags
        total_counted_bags = sum(self.count_bag.bag_counts.values())
        cv2.putText(frame, f"Counted Bags: {total_counted_bags}", (frame.shape[1] - 300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Resize the frame to 1080x720
        # Calculate the original aspect ratio
        if frame.shape[0] > 0 and frame.shape[1] > 0:
            original_ratio = frame.shape[1] / frame.shape[0]
        else:
            logger.warning("Invalid frame dimensions. Skipping resizing.")
            return
        
        # Resize the frame while maintaining the original aspect ratio
        target_height = 720
        target_width = int(target_height * original_ratio)
        # logger.debug(f"target_width: {target_width:.4f}")
        resized_frame = cv2.resize(frame, (target_width, target_height))
        cv2.imshow('Frame', resized_frame)
    
        
    def log_performance_metrics(self):  # public method: used in main.py
        self.frame_processing.log_performance_metrics()
        
        # Log performance metrics for tracking time
        avg_tracking_time = np.mean(self.tracking_times)
        q95_tracking_time = np.percentile(self.tracking_times, 95)
        logger.info(f"Average Tracking Time: {avg_tracking_time:.4f} seconds")
        logger.info(f"95th Percentile Tracking Time: {q95_tracking_time:.4f} seconds")

        # Log performance metrics for display time
        avg_display_times = np.mean(self.display_times)
        q95_display_times = np.percentile(self.display_times, 95)
        logger.info(f"Average display_time Runtime: {avg_display_times:.4f} seconds")
        logger.info(f"95th Percentile display_time Runtime: {q95_display_times:.4f} seconds")