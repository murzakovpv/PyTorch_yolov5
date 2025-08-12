# import cv2
# import time
# import logging
# import os
# # from yolo_wrapper import YOLODetector
# # from models import PeopleCountRecord
# # from database import Database
# from ultralytics.utils.plotting import Annotator

# from src.yolo_wrapper import YOLODetector
# from src.models import PeopleCountRecord
# from src.database import Database

# # Настройка логирования
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler("app.log"),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)

# class VideoProcessor:
#     def __init__(self, camera_config, show_video=False):
#         self.camera_id = camera_config.id
#         self.scene_id = camera_config.scene_id
#         self.rtmp_url = camera_config.rtmp_url
#         self.frame_rate = camera_config.frame_rate
#         self.detector = YOLODetector()
#         self.db = Database()
#         self.last_save_time = time.time()
#         self.show_video = show_video
#         self.window_name = f"Camera {self.camera_id}"

#     def process_stream(self):
#         attempts = 0
#         max_attempts = 5
        
#         while attempts < max_attempts:
#             try:
#                 logger.info(f"⌛ Подключаюсь к камере {self.camera_id}: {self.rtmp_url}")
#                 cap = cv2.VideoCapture(self.rtmp_url)
                
#                 if not cap.isOpened():
#                     logger.warning(f"⚠️ Ошибка подключения, попытка {attempts+1}/{max_attempts}")
#                     attempts += 1
#                     time.sleep(2)
#                     continue
                
#                 logger.info(f"✅ Подключение к камере {self.camera_id} успешно!")
#                 frame_counter = 0
#                 people_counts = []
#                 frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#                 frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#                 fps = cap.get(cv2.CAP_PROP_FPS)
                
#                 logger.info(f"📺 Параметры видео: {frame_width}x{frame_height} @ {fps:.1f} FPS")
                
#                 if self.show_video:
#                     cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
#                     cv2.resizeWindow(self.window_name, frame_width // 2, frame_height // 2)
                
#                 while cap.isOpened():
#                     ret, frame = cap.read()
#                     if not ret:
#                         logger.warning(f"🚨 Ошибка чтения кадра с камеры {self.camera_id}")
#                         break
                    
#                     frame_counter += 1
                    
#                     # Обработка 1 кадра в секунду
#                     if frame_counter % int(fps / self.frame_rate) == 0:
#                         # Детекция людей
#                         results = self.detector.detect(frame)
#                         people_count = 0
                        
#                         # Визуализация результатов
#                         if self.show_video or results:
#                             annotator = Annotator(frame)
                            
#                             for result in results:
#                                 boxes = result.boxes
#                                 for box in boxes:
#                                     cls = int(box.cls)
#                                     conf = float(box.conf)
#                                     if cls == 0:  # Класс 0 - человек
#                                         people_count += 1
#                                         if self.show_video:
#                                             annotator.box_label(box.xyxy[0], f"Person {conf:.2f}", color=(0, 255, 0))
                                    
#                                     # Дополнительно: отображение других объектов
#                                     elif self.show_video:
#                                         label = self.detector.model.names[cls]
#                                         annotator.box_label(box.xyxy[0], f"{label} {conf:.2f}", color=(0, 0, 255))
                        
#                         people_counts.append(people_count)
#                         logger.info(f"Камера {self.camera_id}: Обнаружено людей - {people_count}")
                        
#                         # Отображение кадра
#                         if self.show_video:
#                             # Добавление информации о FPS и количестве людей
#                             fps_text = f"FPS: {1/(time.time() - self.last_frame_time):.1f}" if hasattr(self, 'last_frame_time') else "FPS: -"
#                             cv2.putText(frame, fps_text, (10, 30), 
#                                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
#                             cv2.putText(frame, f"People: {people_count}", (10, 70), 
#                                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            
#                             cv2.imshow(self.window_name, frame)
#                             if cv2.waitKey(1) & 0xFF == ord('q'):
#                                 logger.info("👋 Пользователь запросил выход")
#                                 break
                        
#                         self.last_frame_time = time.time()
                    
#                     # Сохранение статистики каждые 10 секунд
#                     current_time = time.time()
#                     if current_time - self.last_save_time >= 10 and people_counts:
#                         avg_count = sum(people_counts) / len(people_counts)
#                         record = PeopleCountRecord(
#                             camera_id=self.camera_id,
#                             scene_id=self.scene_id,
#                             count=round(avg_count)
#                         )
                        
#                         try:
#                             self.db.insert_record(record)
#                             logger.info(f"💾 Сохранено в БД: Камера {self.camera_id}, среднее людей: {avg_count:.1f}")
#                         except Exception as e:
#                             logger.error(f"❌ Ошибка сохранения в БД: {str(e)}")
                        
#                         people_counts = []
#                         self.last_save_time = current_time
                
#                 # Выход из цикла подключения
#                 break
                
#             except Exception as e:
#                 logger.error(f"🔥 Критическая ошибка при обработке камеры {self.camera_id}: {str(e)}")
#                 attempts += 1
#                 time.sleep(3)
        
#         # Завершение работы
#         if attempts >= max_attempts:
#             logger.error(f"🚫 Не удалось подключиться к камере {self.camera_id} после {max_attempts} попыток")
        
#         try:
#             cap.release()
#             if self.show_video:
#                 cv2.destroyWindow(self.window_name)
#         except:
#             pass






import cv2
import time

from src.yolo_wrapper import YOLODetector
from src.models import PeopleCountRecord
from src.database import Database

class VideoProcessor:    
    def __init__(self, camera_config):
        self.camera_id = camera_config.id
        self.scene_id = camera_config.scene_id
        self.rtmp_url = camera_config.rtmp_url
        self.frame_rate = camera_config.frame_rate
        self.detector = YOLODetector()
        self.db = Database()
        self.last_save_time = time.time()

    def process_stream(self):
        cap = cv2.VideoCapture(self.rtmp_url)
        if not cap.isOpened():
            raise ConnectionError(f"Не удалось подключиться к потоку: {self.rtmp_url}")

        frame_counter = 0
        people_counts = []

        while True:
            ret, frame = cap.read()
            if not ret:
                # Логирование ошибки
                continue

            frame_counter += 1
            
            # Обработка 1 кадра в секунду
            if frame_counter % int(cap.get(cv2.CAP_PROP_FPS) / self.frame_rate) == 0:
                count = self.detector.detect_people(frame)
                people_counts.append(count)
                print(f"Камера {self.camera_id}: Обнаружено людей - {count}")

            # Сохранение каждые 60 секунд
            current_time = time.time()
            # if current_time - self.last_save_time >= 60:
            #     avg_count = sum(people_counts) // len(people_counts) if people_counts else 0
            #     record = PeopleCountRecord(
            #         camera_id=self.camera_id,
            #         scene_id=self.scene_id,
            #         count=avg_count
            #     )
            #     self.db.insert_record(record)
                
            #     people_counts = []
            #     self.last_save_time = current_time
            #     print(f"Сохранено в БД: Камера {self.camera_id}, Людей: {avg_count}")

            # # В методе process_stream, в блоке сохранения каждые 20 секунд:
            if current_time - self.last_save_time >= 20:
                avg_count = sum(people_counts) // len(people_counts) if people_counts else 0
                record = PeopleCountRecord(
                    camera_id=self.camera_id,
                    scene_id=self.scene_id,
                    count=avg_count
                )
                try:
                    self.db.insert_record(record)
                    print(f"Сохранено в БД: Камера {self.camera_id}, Людей: {avg_count}")
                except Exception as e:
                    print(f"Ошибка сохранения в БД: {str(e)}")
                
                people_counts = []
                self.last_save_time = current_time    
                