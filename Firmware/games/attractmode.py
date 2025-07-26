import math
import random
from pix6t4.color import Color
from pix6t4.game import Game
from pix6t4.console import PIX6T4Color
from pix6t4.console import Button
from pix6t4.animation import Animation

class Rainbow(Animation):
    def pixel_color(self, x, y, r, angle):
        max_frame = 360
        self.frame_number = self.frame_number % max_frame
        return Color.fromHSLA((x * 2 + self.frame_number) * 5 % 360, 100, 50)

class BeachBall(Animation):
    def pixel_color(self, x, y, r, angle):
        max_frame = 360
        self.frame_number = self.frame_number % max_frame
        return Color.fromHSLA((angle + self.frame_number * 4) % 360, 100, 50)

class Droplet:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
class GhostInTheShell(Animation):
    def __init__(self, pix6t4: PIX6T4Color):
        super().__init__(pix6t4)
        self.droplets = []
        self.speed = 0.5
        self.max_droplets = 10
    def draw_frame(self):
        self.pix6t4.cls()
        if (len(self.droplets) < self.max_droplets):
            self.droplets.append(Droplet(
                x = -random.random() * 16,
                y = int(random.random() * 8)
            ))
        for droplet in self.droplets:
            droplet.x += self.speed
            if droplet.x > 16:
                self.droplets.remove(droplet)
        super().draw_frame()
    def pixel_color(self, x, y, r, angle):
        intensity = 0
        for droplet in self.droplets:
            if droplet.y == y and x < droplet.x:
                intensity += 8 - min(droplet.x - x, 8)
        return Color.fromRGB(0, min(255, int(intensity * 32)), 0)

animations = [Rainbow, BeachBall, GhostInTheShell]

class AttractMode(Game):
    """Attract mode for PIX6T4 Color."""
    name = "Attract Mode"
    priority = 8999 # Attract mode should be just before settings

    def __init__(self, pix6t4: PIX6T4Color):
        """Initialize the attract mode."""
        super().__init__(pix6t4)
        self.animations = [animation(pix6t4) for animation in animations]
        self.current_animation = 0

    def title_screen(self):
        """Display the title screen for the game."""
        self.pix6t4.cls()
        for x in range(8):
            for y in range(8):
                self.pix6t4.plot(x, y, Color.fromHSLA(x * 45, 100, 50))

    def loop(self):
        """The main attract mode loop."""
        self.animations[self.current_animation].draw_frame()

    def handle_button_pressed(self, button):
        """Handle button press events in attract mode."""
        if button == Button.RIGHT:
            self.current_animation = (self.current_animation + 1) % len(self.animations)
        elif button == Button.LEFT:
            self.current_animation = (self.current_animation - 1) % len(self.animations)

main = AttractMode