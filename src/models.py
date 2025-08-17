from pydantic import BaseModel
from datetime import datetime

class CameraConfig:
    def __init__(self, id, scene_id, source, rtmp_url, frame_rate):
        self.id = id
        self.scene_id = scene_id
        self.source = source
        self.rtmp_url = rtmp_url
        self.frame_rate = frame_rate

class PeopleCountRecord(BaseModel):
    timestamp: datetime
    camera_id: int
    scene_id: int
    count: int
    