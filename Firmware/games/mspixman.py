from pix6t4.bitmap import Bitmap
from pix6t4.game import Game
from pix6t4.console import PIX6T4Color

class MsPixMan(Game):
    """MsPixMan game for PIX6T4 Color."""
    name = "Ms. Pix-Man"
    def __init__(self, pix6t4: PIX6T4Color):
        """Initialize the MsPixMan game."""
        super().__init__(pix6t4)

    def title_screen(self):
        """Display the title screen for the game."""
        Bitmap.from_ascii_art(
            """
 rrYYY  
rBrYYYY 
rrYYBYrr
YYYYYY  
YYYY    
YYYYYYrr
 YYYYYY 
  YYYY  
            """).blit(0, 0, 8, 8, self.pix6t4.pixels)

    def loop(self):
        """The main game loop."""
        pass

main = MsPixMan