import yaml
import threading

from src.models import CameraConfig
from src.video_processor import VideoProcessor

def main():
    # Загрузка конфигурации камер
    with open("config/cameras.yaml", "r") as f:  # Изменён путь
        config = yaml.safe_load(f)
    
    cameras = [CameraConfig(**cam) for cam in config["cameras"]]
    
    # Запуск обработчика для каждой камеры в отдельном потоке
    threads = []
    for camera in cameras:
        # # Для включения визуализации
        # processor = VideoProcessor(camera, show_video=True)

        # # Для выключения визуализации (серверный режим)
        # # processor = VideoProcessor(camera, show_video=False)
        processor = VideoProcessor(camera)
        thread = threading.Thread(target=processor.process_stream)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    # Бесконечное ожидание
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
    