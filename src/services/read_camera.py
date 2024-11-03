import cv2
import time
from src.utils.custom_logger import get_custom_logger

logger = get_custom_logger(__name__)

class ReadCamera:
    def __init__(self, CONFIG, process_frame_callback) -> None:
        self.RTSP_URL = CONFIG['RTSP_URL']
        self.SAMPLING_RATE = CONFIG['SAMPLING_RATE']
        self.INITIAL_SLEEP = CONFIG['INITIAL_SLEEP']
        self.FRAME_COUNT = CONFIG.get('FRAME_COUNT', None)
        self.process_frame_callback = process_frame_callback
  
    def run(self):
        logger.info(f"Waiting for {self.INITIAL_SLEEP} seconds for network stability.")
        time.sleep(self.INITIAL_SLEEP)

        logger.info(f"Starting reading the CCTV streaming image...")
        cap = cv2.VideoCapture(self.RTSP_URL)
        if not cap.isOpened():
            logger.error("Error opening video stream")
            return

        frame_counter = 1
        last_capture_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                logger.error("Failed to grab frame")
                break

            current_time = time.time()
            if current_time - last_capture_time >= self.SAMPLING_RATE:
                df = self.process_frame_callback(frame, frame_counter)
                yield df, frame     # <-- This is where yield is used, return will break the loop
                last_capture_time = current_time    # Update last capture time for sampling rate
                frame_counter += 1

            if self.FRAME_COUNT and frame_counter >= self.FRAME_COUNT:
                logger.warning("Remove FRAME_COUNT in client_config.yaml for manually stop")
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
