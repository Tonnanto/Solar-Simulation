from datetime import timedelta

from orbit import Orbit
from planet import *

scene.title = "Solar System"
scene.width = 2400
scene.height = 1100

# x_axis = curve(pos=[vec(0, 0, 0), vec(200_000_000, 0, 0)], color=color.white)
# y_axis = curve(pos=[vec(0, 0, 0), vec(0, 200_000_000, 0)], color=color.yellow)
# z_axis = curve(pos=[vec(0, 0, 0), vec(0, 0, 200_000_000)], color=color.orange)

scrollToZoom = False

sun = Astro_Object(name="Sun", radius=696340, color=color.yellow)

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


# merc_orbit = Orbit(N = 48.33167, i = 7.00487, w = 77.45645, a = 0.38709893, e = 0.20563069, M = 252.25084)
# merc_orbit.draw(100)
# venus_orbit = Orbit(N = 76.68069, i = 3.39471, w = 131.53298, a = 0.72333199, e = 0.00677323, M = 181.97973)
# venus_orbit.draw(100)
# earth_orbit = Orbit(N = -11.26064, i = 0, w = 102.94719, a = 1.00000011, e = 0.01671022, M = 100.46435)
# earth_orbit.draw(100)
# mars_orbit = Orbit(N = 49.57854, i = 1.85061, w = 336.04084, a = 1.52366231, e = 0.09341233, M = 355.45332)
# mars_orbit.draw(100)

def date_submitted(b: button):
    try:
        day = int(day_text.text)
        month = int(month_text.text)
        year = int(year_text.text)
        date = datetime(day=day, month=month, year=year)

        print(date.strftime("%d.%m.%Y"))

        for planet in planets:
            planet.move(date)

    except ValueError:
        print("Invalid number!")


def day_text_changed(t: winput):
    print(t.text)


def month_text_changed(t: winput):
    print(t.text)


def year_text_changed(t: winput):
    print(t.text)


def scroll_to_zoom_clicked(r):
    scrollToZoom = r.checked


def slider_moved(s):
    date = datetime.now() + timedelta(days=int(s.value * 10000))
    day_text.text = date.strftime("%d")
    month_text.text = date.strftime("%m")
    year_text.text = date.strftime("%Y")
    for planet in planets:
        planet.move(date)


draw_planets()
box()

scene.append_to_caption('\n')

day_text = winput(bind=day_text_changed, width=40, text=datetime.now().day)
month_text = winput(bind=month_text_changed, width=40, text=datetime.now().month)
year_text = winput(bind=year_text_changed, width=80, text=datetime.now().year)
scene.append_to_caption('   ')
button(bind=date_submitted, text="OK")

scene.append_to_caption('\n\n')

checkbox(bind=scroll_to_zoom_clicked, text='Scroll to zoom')
scene.append_to_caption('\n\n')

slider(bind=slider_moved, length=2000)
scene.append_to_caption('\n\n')