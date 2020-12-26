from vpython import *
from astro_object import Astro_Object
from util import calc_days
from datetime import datetime
from settings import Settings


class Planet(Astro_Object):

    def __init__(self, name, radius, color, home, orbit):
        super(Planet, self).__init__(name=name, radius=radius, color=color)
        self.home = home
        self.dist = dist
        self.orbit = orbit
        self.orbit.draw(1000, self.color)
        self.move_to_date(datetime.now())

    def move_to_date(self, date: datetime):
        self.move(calc_days(date))

    def move(self, days: float):
        if self.orbit is None:
            return
        # E = M + e*(180/pi) * sin(M) * ( 1.0 + e * cos(M) )
        M = self.orbit.M + self.orbit.m * days
        E = M + self.orbit.e * (180 / pi) * sin(radians(M)) * (1.0 + self.orbit.e * cos(radians(M)))

        loc = self.orbit.get_loc(radians(E))

        # Adjust Scene center if planet is focused
        self.sphere.pos = loc
        if Settings.center_object == self:
            scene.center = self.sphere.pos

        self.update_label()
