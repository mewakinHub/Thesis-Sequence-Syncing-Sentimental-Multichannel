from ultralytics import YOLO
import torch
from src.utils.custom_logger import get_custom_logger
from deepface import DeepFace

logger = get_custom_logger(__name__)

class YoloV8Inference:
    def __init__(self, CONFIG) -> None:
        self.model_path = CONFIG['MODEL_PATH']
        
        # Set device to GPU if available
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {self.device}")
        print("CUDA Available:", torch.cuda.is_available())
        if torch.cuda.is_available():
            print("Device Count:", torch.cuda.device_count())
            print("Current Device:", torch.cuda.current_device())
            print("Device Name:", torch.cuda.get_device_name(torch.cuda.current_device()))
        else:
            logger.warning("CUDA is not available. Please check your CUDA installation.")
        
        # Load model to device using the YOLO library
        # self.model = YOLO(self.model_path)
        # self.model.to(self.device)

        # for mapping class to names and type
        self.names = self.model.names
        self.type_bag = {
            0: 'bag', 1: 'pig_9', 2: 'pig_9', 3: 'pig_9', 
            4: 'pig_1L', 5: 'pig_1L', 6: 'pig_1L', 7: 'pig_2', 
            8: 'pig_2', 9: 'pig_2', 10: 'pig_6', 11: 'pig_6', 
            12: 'pig_6', 13: '7501', 14: '7501', 15: '7502', 
            16: '7502', 17: '7503', 18: '7503', 19: '7509', 
            20: '7509', 21: 'pig_3', 22: 'pig_3', 23: 'pig_3'
        }

    def run(self, image):
        # results = self.model.predict(image)           # GPU   
        result = DeepFace.analyze(image, actions=['emotion']) # CPU
        print(result)
        # results = self.__process_result_list(results) # cpu
        # return results

    def __process_result_list(self, results):
        processed_results = []
        for output in results:
            output = output.cpu() # Move to CPU for processing (not require GPU acceleration.)
            processed_results.append({
                "class": output.boxes.cls.to(int).tolist(),
                "conf": output.boxes.conf.tolist(),
                "bdbox": output.boxes.xyxy.to(int).tolist()
            })
        return processed_results
