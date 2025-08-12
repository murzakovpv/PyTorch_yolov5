import cv2

def test_stream(url):
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        print(f"Ошибка подключения к {url}")
        return
        
    print(f"Успешное подключение к {url}")
    print("Параметры потока:")
    print(f" - Ширина: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}")
    print(f" - Высота: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
    print(f" - FPS: {cap.get(cv2.CAP_PROP_FPS)}")
    
    cap.release()

# Тестируем разные источники
test_stream("test_video.mp4")  # Видеофайл
test_stream(0)                 # Веб-камера
test_stream("rtmp://real-server.com/live/stream")  # Реальный RTMP