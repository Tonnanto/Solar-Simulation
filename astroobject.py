from vpython import *


class AstroObject:

    def __init__(self, name, radius, color):
        self.idx = 0
        self.name = name
        self.radius = radius
        self.color = color
        self.sphere = sphere(radius=radius, color=color)
        self.label = label(text=name, xoffset=20, yoffset=20)

    def update_label(self):
        self.label.pos = self.sphere.pos
