import yaml
import threading

from src.models import CameraConfig
from src.video_processor import VideoProcessor
from src.database import Database

def main():
    db = Database()  # Создание объекта базы данных
    # Загрузка конфигурации камер
    with open("config/cameras.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    cameras = [CameraConfig(**cam) for cam in config["cameras"]]
    print(cameras)

    
    # Запуск обработчика для каждой камеры в отдельном потоке
    threads = []
    for camera in cameras:
        # Передайте db как второй аргумент
        processor = VideoProcessor(camera, db)
        thread = threading.Thread(target=processor.process_stream)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    # Бесконечное ожидание
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()