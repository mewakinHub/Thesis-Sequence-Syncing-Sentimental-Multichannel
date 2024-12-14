from src.providers.inference import YoloV8Inference
from src.utils.app_setting import AppSettings
from src.services.read_camera import ReadCamera
from src.services.frame_processing import FrameProcessing
from src.services.post_process import PostProcess
from src.services.video_processing import VideoProcessing
from src.providers.iou_tracker import IOUTracker
from src.services.count_bag import CountBag
from src.utils.custom_logger import get_custom_logger

# Configure custom logger
logger = get_custom_logger(__name__)

# for video processing
if __name__ == "__main__":
    CONFIG = AppSettings.get_settings()

    logger.info("Initialize all dependencies...")
    yolo_inference = YoloV8Inference(CONFIG)
    post_process = PostProcess(yolo_inference.type_bag) # voting based on type_bag
    frame_processing  = FrameProcessing(yolo_inference, post_process, CONFIG) 
    count_bag = CountBag(yolo_inference.type_bag) # count bag based on type_bag
    iou_tracker = IOUTracker(CONFIG)
    read_camera = ReadCamera(CONFIG, frame_processing.process_frame) # RC.run() # frame processing every 200ms

    logger.info("Initialize VideoProcessing w/ dependencies...")
    video_processing = VideoProcessing(CONFIG, read_camera, frame_processing, count_bag, iou_tracker)

    logger.info("Start processing...")
    video_processing.run() # Start the entire video processing workflow

    logger.info("Logging performance metrics & save results...")
    video_processing.log_performance_metrics()