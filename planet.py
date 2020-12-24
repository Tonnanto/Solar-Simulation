from vpython import *
from astro_object import Astro_Object
from orbit import calc_days
from datetime import datetime


class Planet(Astro_Object):

    def __init__(self, name, radius, color, home, orbit):
        super(Planet, self).__init__(name=name, radius=radius, color=color)
        self.home = home
        self.dist = dist
        self.orbit = orbit
        self.orbit.draw(100, self.color)
        self.move(datetime.now())

    # def drawOrbit(self, corners):
    #     if self.home == None: return
    #     theta = 0
    #     dtheta = pi / corners
    #     r = self.dist
    #     circle_list = []
    #     while (theta <= 2*pi):
    #         circle_list.append(vec(r * cos(theta), r * sin(theta), 0))
    #         theta += dtheta
    #
    #     circle = curve(pos = circle_list, color = self.color)

    def move(self, date):
        if self.orbit is None:
            return
        # E = M + e*(180/pi) * sin(M) * ( 1.0 + e * cos(M) )
        M = self.orbit.M + self.orbit.m * calc_days(date)
        E = M + self.orbit.e * (180 / pi) * sin(radians(M)) * (1.0 + self.orbit.e * cos(radians(M)))

        loc = self.orbit.get_loc(radians(E))

        self.sphere.pos = loc

        self.updateLabel()

    # def move(self, vector):
    #     for i in range(1000):
    #         rate(1000)
    #         self.sphere.pos = self.sphere.pos + vector
    #         dist = (self.sphere.pos.x ** 2 + self.sphere.pos.y ** 2 + self.sphere.pos.z ** 2) ** 0.5
    #         rad_vec = (self.sphere.pos - self.home.sphere.pos) / dist
    #         fgrav = -10000 * rad_vec / dist ** 2
    #         vector = vector + fgrav
    #         self.sphere.pos += vector
    #         self.updateLabel()
    #         if dist <= self.home.sphere.radius: break
