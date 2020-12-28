import json
from datetime import datetime

from vpython import *

from astroobject import AstroObject
from satellite import Satellite
from settings import Settings
from util import calc_days, calc_date, au_to_km


class Main:
    sun: AstroObject
    planets = []

    @staticmethod
    def setup():
        Main.sun = AstroObject(name="Sun", radius=696340, color=color.yellow)
        Settings.center_object = Main.sun

        background = sphere(pos=vec(0, 0, 0), texture="resources/stars_texture.jpg", radius=au_to_km(400), shininess=0)
        scene.range = au_to_km(80)

        Main.draw_planets()

        Main.setup_widgets()

    @staticmethod
    def draw_planets():

        resources = [
            ("mercury", color.orange),
            ("venus", color.cyan),
            ("earth", color.blue),
            ("mars", color.red),
            ("jupiter", color.white),
            ("saturn", color.orange),
            ("uranus", color.cyan),
            ("neptune", color.blue),
            ("pluto", color.white)
        ]

        for res in resources:
            with open('resources/' + res[0] + '.json') as json_file:
                dic = json.load(json_file)
                Main.planets.append(Satellite(dic, home=Main.sun, clr=res[1]))

        # Main.planets.append(Satellite(name="Mercury", radius=2_439.7, color=color.orange, home=Main.sun,
        #                               orbit=Orbit(N=48.3313, i=7.0047, w=29.1241, a=0.387098, e=0.205635, M=168.6562,
        #                                           m=4.0923344368)))
        # Main.planets.append(Satellite(name="Venus", radius=6_051.8, color=color.cyan, home=Main.sun,
        #                               orbit=Orbit(N=76.6799, i=3.3946, w=54.8910, a=0.723330, e=0.006773, M=48.0052,
        #                                           m=1.6021302244)))
        # Main.planets.append(Satellite(name="Earth", radius=6_371, color=color.blue, home=Main.sun,
        #                               orbit=Orbit(N=-11.26064, i=0, w=102.94719, a=1.00000011, e=0.01671022,
        #                                           M=100.46435,
        #                                           m=0.9856091020)))
        # Main.planets.append(Satellite(name="Mars", radius=3_389.5, color=color.red, home=Main.sun,
        #                               orbit=Orbit(N=49.5574, i=1.8497, w=286.5016, a=1.523688, e=0.093405, M=18.6021,
        #                                           m=0.5240207766)))
        # Main.planets.append(Satellite(name="Jupiter", radius=69_911, color=color.white, home=Main.sun,
        #                               orbit=Orbit(N=100.4542, i=1.3030, w=273.8777, a=5.20256, e=0.048498, M=19.8950,
        #                                           m=0.0830853001)))
        # Main.planets.append(Satellite(name="Saturn", radius=58_232, color=color.orange, home=Main.sun,
        #                               orbit=Orbit(N=113.6634, i=2.4886, w=339.3939, a=9.55475, e=0.055546, M=316.9670,
        #                                           m=0.0334442282)))
        # Main.planets.append(Satellite(name="Uranus", radius=25_362, color=color.blue, home=Main.sun,
        #                               orbit=Orbit(N=74.0005, i=0.7733, w=96.6612, a=19.18171, e=0.047318, M=142.5905,
        #                                           m=0.011725806)))
        # Main.planets.append(Satellite(name="Neptune", radius=24_622, color=color.cyan, home=Main.sun,
        #                               orbit=Orbit(N=131.7806, i=1.7700, w=272.8461, a=30.05826, e=0.008606, M=260.2471,
        #                                           m=0.005995147)))
        # Main.planets.append(Satellite(name="Pluto", radius=1_188.3, color=color.white, home=Main.sun,
        #                               orbit=Orbit(N=110.30, i=17.14001, w=113.76, a=39.4821, e=0.24883, M=14.53,
        #                                           m=0.003973966)))

        return

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++                                                  WIDGETS                                                   ++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Date Controls
    play_button: button
    day_text: winput
    month_text: winput
    year_text: winput
    hour_text: winput

    time_scale_text: wtext

    @staticmethod
    def setup_widgets():
        # Scene Attributes
        scene.title = "Solar System"
        scene.width = 2400
        scene.height = 1100

        box()

        Main.setup_focus_object_controls()
        Main.setup_date_controls()
        Main.setup_time_controls()

    @staticmethod
    def setup_focus_object_controls():
        scene.append_to_caption('\n')
        wtext(text="Focus:  ")
        button(bind=Main.focus_object, text="Sun")
        button(bind=Main.focus_object, text="Mercury")
        button(bind=Main.focus_object, text="Venus")
        button(bind=Main.focus_object, text="Earth")
        button(bind=Main.focus_object, text="Mars")
        button(bind=Main.focus_object, text="Jupiter")
        button(bind=Main.focus_object, text="Saturn")
        button(bind=Main.focus_object, text="Uranus")
        button(bind=Main.focus_object, text="Neptune")
        button(bind=Main.focus_object, text="Pluto")
        scene.append_to_caption('   ')
        button(bind=Main.zoom_in, text="Zoom in")
        button(bind=Main.zoom_out, text="Zoom out")

    @staticmethod
    def setup_date_controls():
        scene.append_to_caption('\n\n')
        Main.play_button = button(bind=Main.play_button_clicked, text="⏸")
        Main.day_text = winput(bind=None, width=40, text=datetime.now().day)
        Main.month_text = winput(bind=None, width=40, text=datetime.now().month)
        Main.year_text = winput(bind=None, width=80, text=datetime.now().year)
        Main.hour_text = winput(bind=None, width=40, text=datetime.now().hour)
        scene.append_to_caption('   ')
        button(bind=Main.date_submitted, text="OK")

    @staticmethod
    def setup_time_controls():
        scene.append_to_caption('\n\n')
        wtext(text="Time Factor:  ")
        slider(bind=Main.timescale_changed, length=400, text="time")
        Main.time_scale_text = wtext(text=" * 2 ^ 0")

    @staticmethod
    def setup_scroll_options():
        scene.append_to_caption('\n\n')
        checkbox(bind=Main.scroll_to_zoom_clicked, text='Scroll to zoom')
        scene.append_to_caption('\n\n')

    @staticmethod
    def date_submitted(b: button):
        try:
            day = int(Main.day_text.text)
            month = int(Main.month_text.text)
            year = int(Main.year_text.text)
            hour = int(Main.hour_text.text)
            date = datetime(day=day, month=month, year=year, hour=hour)
            Settings.days = calc_days(date)

            print(date.strftime("%d.%m.%Y  %H"))

            for planet in Main.planets:
                planet.move(Settings.days)

        except ValueError:
            print("Invalid number!")

    @staticmethod
    def focus_object(b: button):
        if b.text == "Sun":
            Settings.center_object = Main.sun
            scene.center = Main.sun.sphere.pos

        else:
            for planet in Main.planets:
                if planet.name == b.text:
                    Settings.center_object = planet
                    scene.center = planet.sphere.pos

        if Settings.zoomed_in:
            Main.zoom_in()

    @staticmethod
    def zoom_in():
        d = Settings.center_object.radius * 5
        move = abs(scene.range - d) / 100

        while scene.range > d:
            rate(500)
            scene.range -= move

        scene.range = d
        Settings.zoomed_in = True

    @staticmethod
    def zoom_out():
        d = 8809032837
        move = abs(scene.range - d) / 100

        while scene.range < d:
            rate(500)
            scene.range += move

        scene.range = d
        Settings.zoomed_in = False

    @staticmethod
    def play_button_clicked(b: button):
        Settings.play = not Settings.play
        if Settings.play:
            Main.play_button.text = "⏸"
        else:
            Main.play_button.text = "⏵"
            Main.set_date(calc_date(Settings.days))

    @staticmethod
    def timescale_changed(s: slider):
        value = s.value * 28.0
        Main.time_scale_text.text = " * 2 ^ " + str(value)
        Settings.time_factor = 2 ** value

    @staticmethod
    def scroll_to_zoom_clicked(r):
        scrollToZoom = r.checked

    @staticmethod
    def set_date(date: datetime):
        Main.day_text.text = date.strftime("%d")
        Main.month_text.text = date.strftime("%m")
        Main.year_text.text = date.strftime("%Y")
        Main.hour_text.text = date.strftime("%H")

# Main.setup()
# for p in Main.planets:
#     for i in range(500):
#         p.orbit.get_loc_by_day(i*3)
