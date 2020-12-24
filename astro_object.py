from vpython import *

class Astro_Object:

    def __init__(self, name, radius, color):
        self.idx = 0
        self.name = name
        self.radius = radius
        self.color = color
        self.sphere = sphere(radius = radius, color = color)
        self.label = label(text = name, xoffset = 20, yoffset = 20)

    def updateLabel(self):
        self.label.pos = self.sphere.pos
