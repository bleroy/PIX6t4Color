from pix6t4.bitmap import Bitmap
from pix6t4.color import Color
from pix6t4.game import Game
from pix6t4.console import PIX6T4Color

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
  .  #       #  .#
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
    rounds = [
        (0, Color.PINK),
        (0, Color.Pink),
        (1, Color.LIGHTBLUE)
        ]

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
        self.current_round_index = 0
        self.current_round = MsPixMan.rounds[self.current_round_index]
        self.maze = MsPixMan.mazes[self.current_round[0]].copy()
        self.play_field = Bitmap.from_ascii_art(
            MsPixMan.mazes[self.current_round[0]],
            {
                '#': self.current_round[1],
                '.': Color.GREY,
                'o': Color.WHITE,
                '-': self.current_round[1].with_brightness(0.5),
                '<': Color.YELLOW
            })            

    def loop(self):
        """The main game loop."""
        pass

main = MsPixMan