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



# import torch
# from torchvision.models.detection import fasterrcnn_resnet50_fpn
# import numpy as np

# class YOLODetector:
#     def __init__(self):
#         self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#         self.model = fasterrcnn_resnet50_fpn(pretrained=True).to(self.device)
#         self.model.eval()
        
#     def detect_people(self, frame):
#         # Преобразование кадра в тензор
#         image_tensor = torch.from_numpy(frame).permute(2, 0, 1).float().to(self.device) / 255.0
#         image_tensor = image_tensor.unsqueeze(0)
        
#         # Детекция
#         with torch.no_grad():
#             predictions = self.model(image_tensor)
        
#         # Фильтрация результатов (класс 1 - человек в COCO)
#         boxes = predictions[0]['boxes'].cpu().numpy()
#         labels = predictions[0]['labels'].cpu().numpy()
#         scores = predictions[0]['scores'].cpu().numpy()
        
#         people_count = 0
#         for label, score in zip(labels, scores):
#             if label == 1 and score > 0.5:  # Класс 1 - человек
#                 people_count += 1
                
#         return people_count



# import os
# import cv2
# import numpy as np

# class YOLODetector:
#     def __init__(self, weights_path=None, cfg_path=None):
#         # Определяем базовый путь
#         base_dir = os.path.dirname(os.path.abspath(__file__))
        
#         # Устанавливаем пути по умолчанию
#         # if weights_path is None:
#         #     weights_path = os.path.join(base_dir, 'yolov3.weights')
#         # if cfg_path is None:
#         #     cfg_path = os.path.join(base_dir, 'cfg', 'yolov3.cfg')

#         weights_path = os.path.join(base_dir, 'yolov3-tiny.weights')
#         cfg_path = os.path.join(base_dir, 'cfg', 'yolov3-tiny.cfg')
        
#         print(f"Loading YOLO from:\nWeights: {weights_path}\nConfig: {cfg_path}")
        
#         # Проверяем существование файлов
#         if not os.path.exists(weights_path):
#             raise FileNotFoundError(f"Weights file not found: {weights_path}")
#         if not os.path.exists(cfg_path):
#             raise FileNotFoundError(f"Config file not found: {cfg_path}")
        

#         self.net = cv2.dnn.readNetFromDarknet(cfg_path, weights_path)
#         # self.net = cv2.dnn.readNet(weights_path, cfg_path)
#         self.layer_names = self.net.getLayerNames()
#         self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
#         self.classes = ["person"]  # COCO class 0

#     def detect_people(self, frame):
#         # Остальной код без изменений
#         height, width = frame.shape[:2]
#         blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        
#         self.net.setInput(blob)
#         outs = self.net.forward(self.output_layers)
        
#         people_count = 0
#         for out in outs:
#             for detection in out:
#                 scores = detection[5:]
#                 class_id = np.argmax(scores)
#                 confidence = scores[class_id]
                
#                 if confidence > 0.5 and class_id == 0:  # Фильтр по классу person
#                     people_count += 1
                    
#         return people_count