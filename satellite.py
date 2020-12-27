from vpython import *
from astro_object import Astro_Object
from orbit import Orbit
from util import calc_days
from datetime import datetime
from settings import Settings


class Satellite(Astro_Object):

    # def __init__(self, name, radius, color, orbit, home):
    #     super(Satellite, self).__init__(name=name, radius=radius, color=color)
    #     self.home = home
    #     self.satellites = []
    #     self.orbit = orbit
    #     self.move_to_date(datetime.now())
    #     self.orbit.draw(1000, self.color, center=vec(0, 0, 0))

    def __init__(self, dic, clr, home):
        name = dic['name']
        radius = dic['radius']
        super(Satellite, self).__init__(name=name, radius=radius, color=clr)
        self.home = home
        self.satellites = []

        orbit_dic = dic['orbit']
        self.orbit = Orbit(orbit_dic)

        self.orbit.draw(1000, self.color, center=vec(0, 0, 0))
        self.move_to_date(datetime.now())

        # if 'satellites' in dic:
        #     for sat_dic in dic['satellites']:
        #         self.satellites.append(Satellite(sat_dic, color.white, self))

    def set_satellites(self, satellites):
        self.satellites = satellites
        for sat in self.satellites:
            sat.home = self
            sat.orbit.draw(100, sat.color, center=self.sphere.pos)
            sat.move(Settings.days)

    def move_to_date(self, date: datetime):
        self.move(calc_days(date))

    def move(self, days: float):
        if self.orbit is None:
            print("No orbit")
            return

        loc = self.orbit.get_loc_by_day(days)

        if self.home is not None:
            self.sphere.pos = self.home.sphere.pos + loc
        else:
            self.sphere.pos = loc

        # draw satellites orbits + adjust position
        T = (datetime.now().year - 2000) / 100
        for sat in self.satellites:
            sat.orbit.draw(100, sat.color, center=self.sphere.pos, T=T)
            sat.move(days)

        # Adjust Scene center if planet is focused
        if Settings.center_object == self:
            scene.center = self.sphere.pos

        self.update_label()
