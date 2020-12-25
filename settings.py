from datetime import datetime


class Settings:
    center_object = None
    play: bool = True
    time_factor: int = 1
    date: datetime = datetime.now()
    timestamp: int = datetime.timestamp(datetime.now())
    scrollToZoom = False
