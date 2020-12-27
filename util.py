from datetime import datetime, timedelta


def calc_days(d: datetime):
    delta = d - datetime(year=2000, month=1, day=1, hour=12)
    return delta.days


def calc_date(days: float):
    day = int(days)
    UT = days - day
    hour = int(UT * 24)
    return datetime(year=2000, month=1, day=1, hour=12) + timedelta(days=day, hours=hour)


def au_to_km(x):
    return x * 149_597_870
