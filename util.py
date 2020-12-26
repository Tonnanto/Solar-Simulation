from datetime import datetime, timedelta


# TODO! These functions are very inaccurate when used in reverse

def calc_days(date: datetime):
    y: int = date.year
    m: int = date.month
    D: int = date.day
    UT: float = date.hour

    return (367 * y - 7 * (y + (m + 9) / 12) / 4 - 3 * (
            (y + (m - 9) / 7) / 100 + 1) / 4 + 275 * m / 9 + D - 730515) + UT / 24.0


def calc_date(days: float):
    day = int(days)
    UT = days - day
    hour = int(UT * 24)
    return datetime(year=1999, month=12, day=31) + timedelta(days=day, hours=hour)

# days = calc_days(datetime(year=6000, month=1, day=1, hour=0, minute=0))
# print(days)
# print(calc_date(days))
