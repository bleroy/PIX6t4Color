import os

from pix6t4.color import Color

class Button:
    """PIX6T4 Color buttons"""
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    Y = 4
    B = 5
    X = 6
    A = 7
    SELECT = 8
    START = 9

class Direction:
    """Directions from the d-pad"""
    NONE = 0x00
    NORTH = 0x01
    SOUTH = 0x02
    EAST = 0x04
    WEST = 0x08
    NORTH_EAST = NORTH | EAST
    NORTH_WEST = NORTH | WEST
    SOUTH_EAST = SOUTH | EAST
    SOUTH_WEST = SOUTH | WEST

class PIX6T4Color:
    """The interface to implement for a PIX6T4 Color, real hardware or emulator."""
    def __init__(self):
        """Initialize the PIX6T4 Color interface."""
        self.direction = Direction.NONE
        self.A = False
        self.B = False
        self.X = False
        self.Y = False
        self.game_running = False
        self.pixels = [[Color.BLACK for _ in range(8)] for _ in range(8)]
        self.games = []
        self.discover_games()
        self.current_game = None if len(self.games) == 0 else self.games[0]
        self.current_game_index = 0
        self.sound_enabled = True
        self.brightness = 1.0

    def discover_games(self):
        """Scans the games folder for available games, loads them and returns them as a dictionary."""
        game_files = [f for f in os.listdir('games') if f.endswith('.py')]
        for game_file in game_files:
            name = game_file[:-3]
            module = __import__(f'games.{name}')
            game = getattr(module, name).main
            self.games.append(game(self))
        # Order games by priority
        self.games.sort(key=lambda game: game.priority)

    def run(self):
        """Run the PIX6T4 Color console."""
        while True:
            self.loop()

    def loop(self):
        """The main loop of the PIX6T4 Color."""
        if self.game_running:
            self.current_game.loop()
        else:
            self.current_game.title_screen()
        self.render()

    def handle_button_pressed(self, button: Button):
        """Handle button press events."""
        if self.current_game is None:
            return
        if button == Button.UP:
            self.direction |= Direction.NORTH
        elif button == Button.DOWN:
            self.direction |= Direction.SOUTH
        elif button == Button.LEFT:
            self.direction |= Direction.WEST
        elif button == Button.RIGHT:
            self.direction |= Direction.EAST
        elif button == Button.Y:
            self.Y = True
        elif button == Button.B:
            self.B = True
        elif button == Button.X:
            self.X = True
        elif button == Button.A:
            self.A = True
        elif button == Button.SELECT:
            self.handle_select()
        elif button == Button.START:
            self.handle_start()
        if self.game_running:
            self.current_game.handle_button_pressed(button)

    def handle_button_released(self, button: Button):
        """Handle button release events."""
        if self.current_game is None:
            return
        if button == Button.UP:
            self.direction &= ~Direction.NORTH
        elif button == Button.DOWN:
            self.direction &= ~Direction.SOUTH
        elif button == Button.LEFT:
            self.direction &= ~Direction.WEST
        elif button == Button.RIGHT:
            self.direction &= ~Direction.EAST
        elif button == Button.Y:
            self.Y = False
        elif button == Button.B:
            self.B = False
        elif button == Button.X:
            self.X = False
        elif button == Button.A:
            self.A = False
        if not self.game_running:
            if button in (Button.UP, Button.LEFT):
                self.go_to_next_game()
            elif button in (Button.DOWN, Button.RIGHT):
                self.go_to_previous_game()
        else:
            self.current_game.handle_button_released(button)

    def go_to_previous_game(self):
        self.current_game_index = (self.current_game_index + 1) % len(self.games)
        self.current_game = self.games[self.current_game_index]

    def go_to_next_game(self):
        self.current_game_index = (self.current_game_index - 1) % len(self.games)
        self.current_game = self.games[self.current_game_index]

    def handle_select(self):
        """Handle the select button press."""
        if self.game_running:
            self.game_running = False
        else:
            self.go_to_next_game()

    def handle_start(self):
        """Handle the start button press."""
        self.current_game.start()
        self.game_running = True

    def enable_sound(self, enabled: bool = True):
        """Enable or disable sound."""
        self.sound_enabled = enabled

    def cls(self, background_color: Color = Color.BLACK):
        """Clear the screen."""
        for y in range(8):
            for x in range(8):
                self.plot(x, y, background_color)

    def plot(self, x: int, y: int, color: Color):
        """Plot a pixel at (x, y) with the given color."""
        if 0 <= x < 8 and 0 <= y < 8:
            self.pixels[y][x] = color
    
    def beep(self, frequency: int = 440, duration: int = 100):
        """Play a beep sound."""
        if self.sound_enabled:
            pass
    
    def render(self):
        """Render the current state of the PIX6T4 Color."""
        raise NotImplementedError("This method should be overridden in subclasses.")
