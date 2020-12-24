from datetime import datetime

from vpython import *


# The primary orbital elements are here denoted as:
#     N = longitude of the ascending node
#     i = inclination to the ecliptic (plane of the Earth's orbit)
#     w = argument of perihelion
#     a = semi-major axis, or mean distance from Sun
#     e = eccentricity (0=circle, 0-1=ellipse, 1=parabola)
#     M = mean anomaly (0 at perihelion; increases uniformly with time)
# Related orbital elements are:
#     w1 = N + w   = longitude of perihelion
#     L  = M + w1  = mean longitude
#     q  = a*(1-e) = perihelion distance
#     Q  = a*(1+e) = aphelion distance
#     P  = a ^ 1.5 = orbital period (years if a is in AU, astronomical units)
#     T  = Epoch_of_M - (M(deg)/360_deg) / P  = time of perihelion
#     v  = true anomaly (angle between position and perihelion)
#     E  = eccentric anomaly


class Orbit:

    def __init__(self, N, i, w, a, e, M, m):
        self.N = N
        self.i = i
        self.w = w
        self.a = a * 149_597_870
        self.e = e
        self.M = M
        self.m = m

        # self.w1 = N + w
        # self.L = M + self.w1
        # self.q = a * (1 - e)
        # self.Q = a * (1 + e)
        # self.P = a ** 1.5
        # self.T = Epoch_of_M - (M / 360) / self.P

    def draw(self, corners, color):
        theta = 0
        dtheta = pi / corners
        orbit_list = []

        while theta <= 2 * pi:
            orbit_list.append(self.get_loc(theta))
            theta += dtheta

        circle = curve(pos=orbit_list, color=color)

    def get_loc(self, E):
        xv = self.a * (cos(E) - self.e)
        yv = self.a * (sqrt(1.0 - self.e * self.e) * sin(E))

        v = atan2(yv, xv)  # true anomaly
        r = sqrt(xv * xv + yv * yv)  # distance from sun

        x = r * (cos(radians(self.N)) * cos(v + radians(self.w)) - sin(radians(self.N)) * sin(
            v + radians(self.w)) * cos(radians(self.i)))
        y = r * (sin(radians(self.N)) * cos(v + radians(self.w)) + cos(radians(self.N)) * sin(
            v + radians(self.w)) * cos(radians(self.i)))
        z = r * (sin(v + radians(self.w)) * sin(radians(self.i)))

        return vec(x, y, z)

    # def move(day):
    #     E = self.M + self.e * (180 / pi) * sin(self.M) * (1.0 + self.e * cos(self.M)) # eccentric anomaly [°]
    #
    #     xv = r * cos(v) = a * ( cos(E) - e )
    #     yv = r * sin(v) = a * ( sqrt(1.0 - e*e) * sin(E) )
    #
    #     v = atan2( yv, xv )
    #     r = sqrt( xv*xv + yv*yv )
    #
    #     x = r * (cos(self.N) * cos(v + self.w) - sin(self.N) * sin(v + self.w) * cos(self.i))
    #     y = r * (sin(self.N) * cos(v + self.w) + cos(self.N) * sin(v + self.w) * cos(self.i))
    #     z = r * (sin(v + self.w) * sin(self.i))


def calc_days(date: datetime):
    y: int = date.year
    m: int = date.month
    D: int = date.day

    return 367 * y - 7 * (y + (m + 9) / 12) / 4 - 3 * ((y + (m - 9) / 7) / 100 + 1) / 4 + 275 * m / 9 + D - 730515
