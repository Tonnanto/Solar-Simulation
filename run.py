from datetime import timedelta

from main import Main
from planet import *
from settings import Settings


# x_axis = curve(pos=[vec(0, 0, 0), vec(200_000_000, 0, 0)], color=color.white)
# y_axis = curve(pos=[vec(0, 0, 0), vec(0, 200_000_000, 0)], color=color.yellow)
# z_axis = curve(pos=[vec(0, 0, 0), vec(0, 0, 200_000_000)], color=color.orange)

def run():
    Main.setup()

    while True:

        if Settings.play:
            if datetime.timestamp(datetime.now()) - Settings.timestamp > 0.1:
                Main.set_date(Settings.date + timedelta(
                    seconds=(datetime.timestamp(datetime.now()) - Settings.timestamp) * Settings.time_factor))
                for planet in Main.planets:
                    planet.move(Settings.date)

                Settings.timestamp = datetime.timestamp(datetime.now())


run()
