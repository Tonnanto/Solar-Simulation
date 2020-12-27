from datetime import timedelta

from main import Main
from satellite import *
from settings import Settings

# x_axis = curve(pos=[vec(0, 0, 0), vec(200_000_000, 0, 0)], color=color.white)
# y_axis = curve(pos=[vec(0, 0, 0), vec(0, 200_000_000, 0)], color=color.yellow)
# z_axis = curve(pos=[vec(0, 0, 0), vec(0, 0, 200_000_000)], color=color.orange)
from util import calc_date

timestamp: float = datetime.timestamp(datetime.now())
update_day_timestamp: float = datetime.timestamp(datetime.now())


def run():
    global timestamp, update_day_timestamp
    Main.setup()

    while True:

        if Settings.play:
            now = datetime.timestamp(datetime.now())

            if now - timestamp > 0.00025:
                Settings.days = Settings.days + (datetime.timestamp(
                    datetime.now()) - timestamp) / 60 / 60 / 24 * Settings.time_factor
                # Main.set_date(Settings.date + timedelta(
                #     seconds=(datetime.timestamp(datetime.now()) - Settings.timestamp) * Settings.time_factor))
                for planet in Main.planets:
                    planet.move(Settings.days)

                timestamp = now

            if now - update_day_timestamp > 0.25:
                Main.set_date(calc_date(Settings.days))
                update_day_timestamp = now


run()
