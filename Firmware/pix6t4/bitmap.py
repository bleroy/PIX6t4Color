from pix6t4.color import Color

palette = {
    ' ': Color.WHITE,
    'R': Color.RED,
    'G': Color.GREEN,
    'B': Color.BLUE,
    '.': Color.GREY,
    'Y': Color.YELLOW,
    'C': Color.CYAN,
    'M': Color.MAGENTA,
    'r': Color.fromRGB(128, 0, 0),  # Dark red
    'g': Color.fromRGB(0, 128, 0),  # Dark green
    'b': Color.fromRGB(0, 0, 128),  # Dark blue
    'y': Color.fromRGB(128, 128, 0),  # Olive
    'c': Color.fromRGB(0, 128, 128),  # Teal
    'm': Color.fromRGB(128, 0, 128),  # Purple
    'P': Color.PINK,
    '#': Color.BLACK
    }

class Bitmap:
    """Bitmap class for PIX6T4 Color."""
    
    def __init__(self, width: int, height: int):
        """Initialize the bitmap with given width and height."""
        self.width = width
        self.height = height
        self.pixels = [[0x000000FF for _ in range(width)] for _ in range(height)]
    
    @staticmethod
    def from_ascii_art(ascii_art: str, custom_palette: dict = palette):
        """Create a bitmap from an ASCII art string."""
        lines = ascii_art.strip('\n').split('\n')
        height = len(lines)
        width = max(len(line) for line in lines)
        bitmap = Bitmap(width, height)
        
        for x, line in enumerate(lines):
            for y, char in enumerate(line):
                color = custom_palette[char] if char in custom_palette else palette[char] if char in palette else Color.BLACK
                bitmap.set_pixel(x, y, color)
        
        return bitmap
    
    def blit(self, x: int, y: int, width: int, height: int, target):
        """copies part of the bitmap onto a matrix of colors."""
        for row in self.pixels[y:y + height]:
            for color in row[x:x + width]:
                target[x][y] = color
                x += 1
            y += 1
            x = 0
    
    def set_pixel(self, x: int, y: int, color: int):
        """Set the color of a pixel at (x, y)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = color

main = Bitmap