from pix6t4.color import Color
from pix6t4.console import Button, PIX6T4Color

class Game:
    """The PIX6T4 Color game engine as a base class."""
    name = "Base Game"
    priority = 1000  # Default priority for games, can be overridden by subclasses

    def __init__(self, pix6t4: PIX6T4Color):
        """Initialize the game with a PIX6T4 Color instance."""
        self.pix6t4 = pix6t4
    def title_screen(self):
        """Display the title screen for the game."""
        self.pix6t4.cls()
        for x in range(8):
            for y in range(8):
                self.pix6t4.plot(x, y, Color.WHITE if (x + y) % 2 == 0 else Color.BLACK)
    def start(self):
        """Start the game."""
        pass
    def loop(self):
        """
        The main game loop.
        Override this to implement your game.
        """
        raise NotImplementedError("This method should be overridden in subclasses.")
    def handle_button_pressed(self, button: Button):
        """Handle button press events.
        Override this to implement button handling in your game."""
        pass
    def handle_button_released(self, button: Button):
        """Handle button release events.
        Override this to implement button handling in your game."""
        pass