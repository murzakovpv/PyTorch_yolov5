from ultralytics import YOLO
import cv2

class YOLODetector:
    def __init__(self, model_path='yolov5s.pt'):
        self.model = YOLO(model_path)
        
    def detect_people(self, frame):
        results = self.model(frame)
        people_count = 0
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls)
                if cls == 0:  # class 0 is person in COCO
                    people_count += 1
        return people_count
