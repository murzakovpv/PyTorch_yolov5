import cv2
import time
from datetime import datetime
from src.yolo_wrapper import YOLODetector
from src.models import PeopleCountRecord
from src.database import Database

class VideoProcessor:
    def __init__(self, camera_config, db):
        self.camera_config = camera_config
        self.db = db
        self.yolo_detector = YOLODetector()
        self.capture = cv2.VideoCapture(camera_config.source)
        self.camera_id = camera_config.id
        self.scene_id = camera_config.scene_id
        self.rtmp_url = camera_config.rtmp_url
        self.frame_rate = camera_config.frame_rate
        self.last_save_time = time.time()

    def process_stream(self):
        if not self.capture.isOpened():
            raise ConnectionError(f"Не удалось подключиться к источнику видео: {self.rtmp_url}")
        
        frame_counter = 0
        people_counts = []

        while True:
            ret, frame = self.capture.read()
            if not ret:
                print(f"Не удалось получить кадр с камеры {self.camera_id}")
                break
                
            frame_counter += 1
            
            # Обработка 1 кадра в секунду
            if frame_counter % int(self.capture.get(cv2.CAP_PROP_FPS) / self.frame_rate) == 0:
                people_count = self.yolo_detector.detect_people(frame)
                people_counts.append(people_count)
                print(f"Камера {self.camera_id}: Обнаружено людей - {people_count}")

            # Сохранение статистики каждые 3 секунд
            current_time = time.time()
            if current_time - self.last_save_time >= 3:
                avg_count = sum(people_counts) // len(people_counts) if people_counts else 0
                record = PeopleCountRecord(
                    timestamp=datetime.now(),
                    camera_id=self.camera_id,
                    scene_id=self.scene_id,
                    count=avg_count
                )
                try:
                    self.db.insert_record(record)
                    print(f"Сохранено в БД: Камера {self.camera_id}, среднее количество людей: {avg_count}")
                except Exception as e:
                    print(f"Ошибка сохранения в БД: {str(e)}")

                people_counts = []
                self.last_save_time = current_time

        # Освобождение ресурсов
        self.capture.release()
                
