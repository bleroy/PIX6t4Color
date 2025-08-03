from pix6t4.bitmap import Bitmap
from pix6t4.color import Color
from pix6t4.game import Game
from pix6t4.console import PIX6T4Color, Button

class MsPixMan(Game):
    """MsPixMan game for PIX6T4 Color."""
    name = "Ms. Pix-Man"
    # #: wall
    # .: candy
    # o: cookie
    # -: ghost spawn point
    # <: player start point
    mazes = ["""
##################
#....#.......#....
#o##.#.#####.#.##o
#.................
##.#.###.#.###.#.#
  .#.....#.....#. 
##.### ##### ###.#
##.             .#
##.### ##-## ###.#
##.#   #####   #.#
  .  #       #  . 
##.##### # #####.#
##.....  #  .....#
##.###.#####.###.#
#........<........
#.##.###.#.###.##.
#.##.#...#...#.##.
#o##.#.#####.#.##o
#.................
##################""", """
##################
     #.......#    
#### #.#####.# ###
#o.......#.......o
#.####.#.#.#.####.
#.#....#...#....#.
#.#.## ##### ##.#.
#....#       #....
####.# ##-## #.###
#....# #   # #....
#.##.  #####  .##.
#..#.#       #.#..
##.#.## ### ##.#.#
##......###......#
##.####.###.####.#
  ...#..   ..#... 
##.#.#.#####.#.#.#
#o.#.....#.....#.o
#.##.###.#.###.##.
#.................
##################""", """
##################
#......#...#......
#o####.#.#.#.####o
#.#......#......#.
#...#.##.#.##.#...
###.#.........#.##
 ...## ##### ##...
#.#             #.
#.## # ##-## # ##.
#.   # #   # #   .
#.# ## ##### ## #.
#.#             #.
#.## ### # ### ##.
#....#...#...#....
##.#.#.#####.#.#.#
#o.#.....<.....#.o
#.##.###.#.###.##.
#....#...#...#....
#.##.#.#####.#.##.
#....#.......#....
##################""", """
##################
#.................
#o#.##.#####.##.#o
#.#....#...#....#.
#.##.#.#.#.#.#.##.
#....#...#...#....
##.#####.#.#####.#
##...#       #...#
   #.# ##-## #.#  
####.  #####  .###
   #.#       #.#  
##...### # ###...#
##.#...  #  ...#.#
##.###.# # #.###.#
#......# < #......
#.##.#.#####.#.##.
#.#..#.......#..#.
#o#.####.#.####.#o
#........#........
##################"""]
    maze_colors = [Color.DARKPINK, Color.LIGHTBLUE, Color.LILAC, Color.DARKBLUE]
    glow_cycle = 16
    min_glow = 0.5
    max_glow = 1.0

    def __init__(self, pix6t4: PIX6T4Color):
        """Initialize the MsPixMan game."""
        super().__init__(pix6t4)

    def title_screen(self):
        """Display the title screen for the game."""
        Bitmap.from_ascii_art(
            """
#rrYYY##
rBrYYYY#
rrYYBYrr
YYYYYY##
YYYY####
YYYYYYrr
#YYYYYY#
##YYYY##
            """).blit(0, 0, 8, 8, self.pix6t4.pixels)

    def start(self):
        """Start the MsPixMan game."""
        self.pix6t4.game_running = True
        self.current_maze_index = 0
        self.round = 0
        self.score = 0
        self.slowness = 10
        self.start_level()

    def start_level(self):
        """Start a new level in the MsPixMan game."""
        self.maze = [list(line) for line in str(MsPixMan.mazes[self.current_maze_index]).strip().splitlines()]
        # Find the player start position
        for y, row in enumerate(self.maze):
            for x, char in enumerate(row):
                if char == '<':
                    self.player_x = x
                    self.player_y = y
        self.direction = (0, 0)
        self.window_x = max(0, self.player_x - 4)
        self.window_y = max(0, self.player_y - 4)
        self.glow = MsPixMan.min_glow
        self.frame_number = 0

    def render(self):
        """Render the current state of the game."""
        for x in range(self.window_x, self.window_x + 8):
            for y in range(self.window_y, self.window_y + 8):
                self.pix6t4.plot(
                    y - self.window_y,
                    x - self.window_x,
                    self.map_maze_cell_to_color(self.maze[y % len(self.maze)][x % len(self.maze[0])]))
    
    def map_maze_cell_to_color(self, cell: str) -> Color:
        """Map a maze cell character to a color."""
        if cell == '#':
            return MsPixMan.maze_colors[self.current_maze_index]
        elif cell == '.':
            return Color.DARKGREY
        elif cell == 'o':
            return Color.WHITE.with_brightness(self.glow)
        elif cell == '-':
            return MsPixMan.maze_colors[self.current_maze_index].with_brightness(0.5)
        elif cell == '<':
            return Color.YELLOW
        elif cell == 'B': # Blinky
            return Color.RED
        elif cell == 'P': # Pinky
            return Color.PINK
        elif cell == 'I': # Inky
            return Color.CYAN
        elif cell == 'S': # Sue
            return Color.ORANGE
        else:
            return Color.BLACK

    def handle_button_pressed(self, button):
        """Handle button press events."""
        new_direction = (-1, 0) if button == Button.UP else \
                        (1, 0) if button == Button.DOWN else \
                        (0, -1) if button == Button.LEFT else \
                        (0, 1) if button == Button.RIGHT else \
                        (0, 0)
        if self.maze[(self.player_y + new_direction[0]) % len(self.maze)][(self.player_x + new_direction[1]) % len(self.maze[0])] != '#':
            # Only change the direction if the new one wouldn't lead into a wall.
            # This enables the player to anticipate turns.
            self.direction = new_direction

    def loop(self):
        """The main game loop."""
        # Make cookies glow up and down
        glow_direction = 1 if self.frame_number % MsPixMan.glow_cycle < MsPixMan.glow_cycle // 2 else -1
        self.glow = max(
            MsPixMan.min_glow,
            min(
                MsPixMan.max_glow,
                self.glow + glow_direction * (MsPixMan.max_glow - MsPixMan.min_glow) / (MsPixMan.glow_cycle // 2)
            )
        )
        self.frame_number += 1
        # Handle player movement
        if self.direction != (0, 0) and self.frame_number % self.slowness == 0:
            new_x = self.player_x + self.direction[1]
            new_y = self.player_y + self.direction[0]
            intended_cell = self.maze[new_y % len(self.maze)][new_x % len(self.maze[0])]
            if intended_cell == '#': # Wall
                self.direction = (0, 0)
            else:
                # Move the player
                self.maze[self.player_y][self.player_x] = ' '
                self.player_x = new_x % len(self.maze[0])
                self.player_y = new_y
                self.maze[self.player_y][self.player_x] = '<'
                # Slide the window to follow the player
                if (self.player_x - 4) % len(self.maze[0]) > self.window_x:
                    self.window_x = (self.player_x - 4) % len(self.maze[0])
                elif (self.player_x - 3) % len(self.maze[0]) < self.window_x:
                    self.window_x = (self.player_x - 3) % len(self.maze[0])
                if self.player_y > self.window_y + 4:
                    self.window_y = min(self.player_y - 4, len(self.maze) - 8)
                elif self.player_y < self.window_y + 3:
                    self.window_y = max(0, self.player_y - 3)
                if intended_cell == '.': # Candy
                    self.score += 10
        self.render()

main = MsPixMan