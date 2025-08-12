from pydantic import BaseModel
from datetime import datetime

class CameraConfig(BaseModel):
    id: int
    rtmp_url: str
    scene_id: int
    frame_rate: int

class PeopleCountRecord(BaseModel):
    timestamp: datetime
    camera_id: int
    scene_id: int
    count: int
    