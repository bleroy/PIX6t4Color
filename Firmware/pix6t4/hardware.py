import board
import neopixel
import pwmio
import async_buzzer
import keypad

from pix6t4.console import PIX6T4Color

class PIX6T4ColorHardware(PIX6T4Color):
    def __init__(self, revision: int):
        super().__init__()
        self.revision = revision
        self.num_pixels = 64 if revision == 1 else 70 # Rev > 1 has more LED for the logo animation
        self.led_pin = board.GP10
        self.leds = neopixel.NeoPixel(self.led_pin, self.num_pixels, auto_write=False)
        self.pin_up = board.GP0
        self.pin_down = board.GP1
        self.pin_left = board.GP2
        self.pin_right = board.GP3
        self.pin_y = board.GP4
        self.pin_b = board.GP5
        self.pin_x = board.GP6
        self.pin_a = board.GP7
        self.pin_select = board.GP8
        self.pin_start = board.GP9
        self.buttons = keypad.Keys((
              self.pin_up,
              self.pin_down,
              self.pin_left,
              self.pin_right,
              self.pin_y,
              self.pin_b,
              self.pin_x,
              self.pin_a,
              self.pin_select,
              self.pin_start
            ), value_when_pressed=False, pull=True)
        self.pin_buzzer = board.A3
        self.buzzer_io = pwmio.PWMOut(self.pin_buzzer, variable_frequency=True)
        self.buzzer = async_buzzer.Buzzer(self.buzzer_io)
        self.brightness = 0.1

    def render(self):
        """Render the current state of the PIX6T4 Color."""
        i = 0
        for x, row in enumerate(self.pixels):
            for y, col in enumerate(row):
                color = self.pixels[x][y].with_brightness(self.brightness).value >> 8
                self.leds[i] = color
                i += 1
        self.leds.show()

    def loop(self):
        """Main loop for the PIX6T4 Color hardware."""
        # detect button presses before delegating to the base class
        event = self.buttons.events.get()
        if event and event.pressed:
            self.handle_button_pressed(event.key_number)
        super().loop()
    
    def beep(self, frequency: int = 440, duration: int = 200):
        """Play a beep sound."""
        if self.sound_enabled:
            self.buzzer.play([(frequency, duration)])

def main(revision: int = 1):
    hardware = PIX6T4ColorHardware(revision)
    hardware.run()