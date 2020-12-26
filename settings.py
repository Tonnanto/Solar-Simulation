from datetime import datetime

from util import calc_days


class Settings:
    center_object = None
    zoomed_in: bool = False
    play: bool = True
    time_factor: int = 1
    days: float = calc_days(datetime.now())

    scrollToZoom = False
