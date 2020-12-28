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
from util import au_to_km


class Orbit:

    def __init__(self, dic: {str: any}):
        self.a = dic['a']  # AU
        self.e = dic['e']  # value [0 ... 1]
        self.I = dic['I']  # degrees
        self.L = dic['L']  # degrees
        self.o = dic['o']  # degrees
        self.O = dic['O']  # degrees
        self._a = dic['~a']  # AU per century
        self._e = dic['~e']  # change per century
        self._I = dic['~I']  # degrees per century
        self._L = dic['~L']  # degrees per century
        self._o = dic['~o']  # degrees per century
        self._O = dic['~O']  # degrees per century

        # only relevant for jupiter - pluto
        self.b, self.c, self.s, self.f = 0, 0, 0, 0

        if 'b' in dic:
            self.b = dic['b']
        if 'c' in dic:
            self.c = dic['c']
        if 's' in dic:
            self.s = dic['s']
        if 'f' in dic:
            self.f = dic['f']

        self.T = (datetime.now().year - 2000) / 100
        self.color = None
        self.center = vec(0, 0, 0)
        self.curve = None
        self.refresh_interval = 1 / (abs(self._a) + abs(self._e) + abs(self._I) + abs(self._o) + abs(self._O))

    def draw(self, corners, color, center, T=None):
        self.color = color
        self.center = center
        if T is None:
            T = self.T
        else:
            self.T = T
        theta = 0
        dtheta = 360.0 / corners
        orbit_list = []

        while theta <= 360 + dtheta:
            orbit_list.append(self.get_loc(theta, T) + center)
            theta += dtheta

        if self.curve is not None:
            self.curve.visible = False
            del self.curve

        self.curve = curve(pos=orbit_list, color=color)
        return

    def get_loc_by_day(self, d):
        T = d / 36525  # Centuries past J2000.0
        if abs(self.T - T) > self.refresh_interval:
            self.draw(1000, self.color, self.center, T)
        return self.get_loc(self.get_eccentric_anomaly(T), T)

    def get_eccentric_anomaly(self, T):
        e = self.e + self._e * T
        L = self.L + self._L * T
        o = self.o + self._o * T

        M = 0.0
        if -30 < T < 30:  # between 3000 BC and 3000 AC
            M = L - o + self.b * T ** 2 + self.c * cos(self.f * T) + self.s * sin(self.f * T)
        else:
            M = L - o

        M %= 360
        if M > 180:
            M -= 360

        e_ = e * 57.29577951  # e in degrees
        tol = 10 ** (-6)  # tolerance

        # E: float = M + e_ * sin(radians(M))  # start value
        #
        # while True:
        #     d_M = M - (E - e_ * sin(radians(E)))
        #     d_E = d_M / (1 - e_ * cos(radians(E)))
        #     if abs(d_E) < tol:
        #         break
        #     E += d_E

        E: float = M + e * sin(radians(M)) + 0.5 * e**2 * sin(radians(2*M))  # approximation of Kepler Equation

        return E

    def get_loc(self, E, T=None):
        if T is None:
            T = self.T

        a = au_to_km(self.a + self._a * T)
        e = self.e + self._e * T
        I = self.I + self._I * T
        o = self.o + self._o * T
        O = self.O + self._O * T
        arg_per = o - O

        # Coordinates in orbital plane
        x_orb = a * (cos(radians(E)) - e)
        y_orb = a * (1 - e ** 2) ** 0.5 * sin(radians(E))

        cos_o, sin_o = cos(radians(arg_per)), sin(radians(arg_per))
        cos_O, sin_O = cos(radians(O)), sin(radians(O))
        cos_I, sin_I = cos(radians(I)), sin(radians(I))

        x = (cos_o * cos_O - sin_o * sin_O * cos_I) * x_orb + (-sin_o * cos_O - cos_o * sin_O * cos_I) * y_orb
        y = (cos_o * sin_O + sin_o * cos_O * cos_I) * x_orb + (-sin_o * sin_O + cos_o * cos_O * cos_I) * y_orb
        z = (sin_o * sin_I) * x_orb + (cos_o * sin_I) * y_orb

        return vec(x, y, z)
