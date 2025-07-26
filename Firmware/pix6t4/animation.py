from math import atan2, pi, sqrt

from pix6t4.color import Color
from pix6t4.console import PIX6T4Color


class Animation:
    def __init__(self, pix6t4: PIX6T4Color):
        self.pix6t4 = pix6t4
        self.frame_number = 0
        self.x_center = len(pix6t4.pixels) / 2
        self.y_center = len(pix6t4.pixels[0]) / 2

    def pixel_color(self, x, y, r, angle) -> Color:
        """Override this method to define the pixel color based on position and angle."""
        return self.pixels[x][y]

    def draw_frame(self):
        """Override this to take over the rendering of the entire screen."""
        for x in range(len(self.pix6t4.pixels)):
            for y in range(len(self.pix6t4.pixels[x])):
                r = sqrt((x - self.x_center) ** 2 + (y - self.y_center) ** 2)
                angle = (atan2(y - self.y_center, x - self.x_center) * 180 / pi + 180) % 360
                self.pix6t4.plot(x, y, self.pixel_color(x, y, r, angle))
        self.frame_number += 1
