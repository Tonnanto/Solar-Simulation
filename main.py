from datetime import timedelta

from orbit import Orbit
from planet import *
from settings import Settings

scene.title = "Solar System"
scene.width = 2400
scene.height = 1100

# x_axis = curve(pos=[vec(0, 0, 0), vec(200_000_000, 0, 0)], color=color.white)
# y_axis = curve(pos=[vec(0, 0, 0), vec(0, 200_000_000, 0)], color=color.yellow)
# z_axis = curve(pos=[vec(0, 0, 0), vec(0, 0, 200_000_000)], color=color.orange)

scrollToZoom = False

sun = Astro_Object(name="Sun", radius=696340, color=color.yellow)
Settings.center_object = sun

planets = []


def draw_planets():
    planets.append(Planet(name="Mercury", radius=2_439.7, color=color.orange, home=sun,
                          orbit=Orbit(N=48.3313, i=7.0047, w=29.1241, a=0.387098, e=0.205635, M=168.6562,
                                      m=4.0923344368)))
    planets.append(Planet(name="Venus", radius=6_051.8, color=color.cyan, home=sun,
                          orbit=Orbit(N=76.6799, i=3.3946, w=54.8910, a=0.723330, e=0.006773, M=48.0052,
                                      m=1.6021302244)))
    planets.append(Planet(name="Earth", radius=6_371, color=color.blue, home=sun,
                          orbit=Orbit(N=-11.26064, i=0, w=102.94719, a=1.00000011, e=0.01671022, M=100.46435,
                                      m=1)))  # m is guessed
    planets.append(Planet(name="Mars", radius=3_389.5, color=color.red, home=sun,
                          orbit=Orbit(N=49.5574, i=1.8497, w=286.5016, a=1.523688, e=0.093405, M=18.6021,
                                      m=0.5240207766)))
    planets.append(Planet(name="Jupiter", radius=69_911, color=color.white, home=sun,
                          orbit=Orbit(N=100.4542, i=1.3030, w=273.8777, a=5.20256, e=0.048498, M=19.8950,
                                      m=0.0830853001)))
    planets.append(Planet(name="Saturn", radius=58_232, color=color.orange, home=sun,
                          orbit=Orbit(N=113.6634, i=2.4886, w=339.3939, a=9.55475, e=0.055546, M=316.9670,
                                      m=0.0334442282)))
    planets.append(Planet(name="Uranus", radius=25_362, color=color.blue, home=sun,
                          orbit=Orbit(N=74.0005, i=0.7733, w=96.6612, a=19.18171, e=0.047318, M=142.5905,
                                      m=0.011725806)))
    planets.append(Planet(name="Neptune", radius=24_622, color=color.cyan, home=sun,
                          orbit=Orbit(N=131.7806, i=1.7700, w=272.8461, a=30.05826, e=0.008606, M=260.2471,
                                      m=0.005995147)))
    planets.append(Planet(name="Pluto", radius=1_188.3, color=color.white, home=sun,
                          orbit=Orbit(N=110.30, i=17.14001, w=113.76, a=39.4821, e=0.24883, M=14.53,
                                      m=0.003973966)))

    return


def run():
    while Settings.play:
        if datetime.timestamp(datetime.now()) - Settings.timestamp > 0.1:
            set_date(Settings.date + timedelta(
                seconds=(datetime.timestamp(datetime.now()) - Settings.timestamp) * Settings.time_factor))
            for planet in planets:
                planet.move(Settings.date)

            Settings.timestamp = datetime.timestamp(datetime.now())


def date_submitted(b: button):
    try:
        day = int(day_text.text)
        month = int(month_text.text)
        year = int(year_text.text)
        hour = int(hour_text.text)
        minute = int(minute_text.text)
        Settings.date = datetime(day=day, month=month, year=year, hour=hour, minute=minute)

        print(Settings.date.strftime("%d.%m.%Y  %H:%M"))

        for planet in planets:
            planet.move(Settings.date)

    except ValueError:
        print("Invalid number!")


def day_text_changed(t: winput):
    print(t.text)


def month_text_changed(t: winput):
    print(t.text)


def year_text_changed(t: winput):
    print(t.text)


def focus_object(b: button):
    if b.text == "Sun":
        Settings.center_object = sun
        scene.center = sun.sphere.pos
        return

    for planet in planets:
        if planet.name == b.text:
            Settings.center_object = planet
            scene.center = planet.sphere.pos


def play_button_clicked(b: button):
    Settings.play = not Settings.play
    if Settings.play:
        play_button.text = "⏸"
        run()
    else:
        play_button.text = "⏵"


def timescale_changed(s: slider):
    value = s.value * 28.0
    time_scale_text.text = " * 2 ^ " + str(value)
    Settings.time_factor = 2 ** value


def scroll_to_zoom_clicked(r):
    scrollToZoom = r.checked


def set_date(date: datetime):
    Settings.date = date
    day_text.text = date.strftime("%d")
    month_text.text = date.strftime("%m")
    year_text.text = date.strftime("%Y")
    hour_text.text = date.strftime("%H")
    minute_text.text = date.strftime("%M")


def slider_moved(s):
    date = datetime.now() + timedelta(days=int(s.value * 10000))
    set_date(date)
    for planet in planets:
        planet.move(date)


draw_planets()
box()

# Focus Object Buttons
scene.append_to_caption('\n')
wtext(text="Focus:  ")
button(bind=focus_object, text="Sun")
button(bind=focus_object, text="Mercury")
button(bind=focus_object, text="Venus")
button(bind=focus_object, text="Earth")
button(bind=focus_object, text="Mars")
button(bind=focus_object, text="Jupiter")
button(bind=focus_object, text="Saturn")
button(bind=focus_object, text="Uranus")
button(bind=focus_object, text="Neptune")
button(bind=focus_object, text="Pluto")

# Date input and display
scene.append_to_caption('\n\n')
play_button = button(bind=play_button_clicked, text="⏸")
day_text = winput(bind=day_text_changed, width=40, text=datetime.now().day)
month_text = winput(bind=month_text_changed, width=40, text=datetime.now().month)
year_text = winput(bind=year_text_changed, width=80, text=datetime.now().year)
hour_text = winput(bind=day_text_changed, width=40, text=datetime.now().hour)
minute_text = winput(bind=month_text_changed, width=40, text=datetime.now().minute)
scene.append_to_caption('   ')
button(bind=date_submitted, text="OK")

# Time Options
scene.append_to_caption('\n\n')
wtext(text="Time Factor:  ")
slider(bind=timescale_changed, length=400, text="time")
time_scale_text = wtext(text=" * 2 ^ 0")

# Scroll Options
scene.append_to_caption('\n\n')
checkbox(bind=scroll_to_zoom_clicked, text='Scroll to zoom')
scene.append_to_caption('\n\n')

# Slider
slider(bind=slider_moved, length=2000)
scene.append_to_caption('\n\n')
