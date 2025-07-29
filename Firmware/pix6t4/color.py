class Color:
    def __init__(self, value: int):
        """
        Initialize a Color instance.
        The value should be in the format 0xRRGGBBAA.
        """
        self.value = value

    @staticmethod
    def fromInt(value: int):
        """
        Create a Color from an integer.
        The integer should be in the format 0xRRGGBBAA.
        """
        return Color(value)

    @staticmethod
    def fromRGBA(red: int, green: int, blue: int, alpha: float = 1.0):
        """
        Create a Color from red, green, blue and alpha components.
        The alpha component should be a float between 0 (transparent) and 1 (opaque).
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Red, green, and blue components must be between 0 and 255.")
        if not (0 <= alpha <= 1):
            raise ValueError("Alpha must be between 0 and 1.")
        return Color((red << 24) | (green << 16) | (blue << 8) | int(alpha * 255))

    @staticmethod
    def fromRGB(red: int, green: int, blue: int):
        """
        Create a Color from red, green, and blue components.
        The alpha component is set to 1.0 (opaque).
        """
        return Color.fromRGBA(red, green, blue, 1.0)

    @property
    def red(self):
        """
        Return the red component of the color.
        The red component is an integer between 0 and 255.
        """
        return (self.value & 0xFF000000) >> 24

    @property
    def green(self):
        """
        Return the green component of the color.
        The green component is an integer between 0 and 255.
        """
        return (self.value & 0x00FF0000) >> 16

    @property
    def blue(self):
        """
        Return the blue component of the color.
        The blue component is an integer between 0 and 255.
        """
        return (self.value & 0x0000FF00) >> 8

    @property
    def alpha(self):
        """
        Return the alpha component of the color.
        The alpha component is a float between 0 (transparent) and 1 (opaque).
        """
        return (self.value & 0x000000FF) / 255.0

    def with_transparency(self, alpha: float):
        """Return a new Color with the specified alpha transparency."""
        if not (0 <= alpha <= 1):
            raise ValueError("Alpha must be between 0 and 1.")
        return Color(self.value & 0xFFFFFF00 | int(alpha * 255))
    
    def with_brightness(self, brightness: float=1.0):
        """
        Return a new Color with the specified brightness.
        Brightness should be a float between 0 (black) and 1 (original color).
        """
        if not (0 <= brightness <= 1):
            raise ValueError("Brightness must be between 0 and 1.")
        return Color.fromRGBA(
            int(self.red * brightness),
            int(self.green * brightness),
            int(self.blue * brightness),
            self.alpha
        )

    def paint_on(self, other: 'Color'):
        """
        Paints this color on top of another, taking alpha transparency into account.
        The other color must be solid (no transparency).
        The returned color is solid.
        """
        if other & 0xFF < 0xFF:
            raise ValueError("The other color must be solid (no transparency).")
        hexAlpha = self & 0xFF
        if hexAlpha == 0xFF:
            return self
        return Color.fromRGB(
            int((self.red * hexAlpha + other.red * (0xFF - hexAlpha)) / 0xFF),
            int((self.green * hexAlpha + other.green * (0xFF - hexAlpha)) / 0xFF),
            int((self.blue * hexAlpha + other.blue * (0xFF - hexAlpha)) / 0xFF)
        )
    
    def solidify(self):
        """Returns the color without transparency."""
        return Color(self | 0x000000FF)

    def to_RGBA(self):
        """Convert Color to an RGBA tuple."""
        return ((self & 0xFF000000) >> 24, (self & 0x00FF0000) >> 16, (self & 0x0000FF00) >> 8, (self & 0x000000FF) / 255.0)
    
    def toHSLA(self):
        """
        Return the HSLA representation of the color.
        Returns a tuple (hue, saturation, lightness, alpha).
        Hue is in degrees (0-360), saturation and lightness are percentages (0-100).
        """
        r = self.red / 255.0
        g = self.green / 255.0
        b = self.blue / 255.0
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        delta = max_c - min_c

        if delta == 0:
            hue = 0
        elif max_c == r:
            hue = (60 * ((g - b) / delta) + 360) % 360
        elif max_c == g:
            hue = (60 * ((b - r) / delta) + 120) % 360
        else:
            hue = (60 * ((r - g) / delta) + 240) % 360

        lightness = (max_c + min_c) / 2.0 * 100
        saturation = (delta / (1 - abs(2 * lightness / 100 - 1))) * 100 if delta != 0 else 0

        return (hue, saturation, lightness, self.alpha)

    def fromHSLA(hue: float, saturation: float, lightness: float, alpha: float = 1.0):
        """
        Create a Color from HSLA values.
        Hue is in degrees (0-360), saturation and lightness are percentages (0-100).
        Alpha is a float between 0 (transparent) and 1 (opaque).
        """
        if not (0 <= hue < 360):
            raise ValueError("Hue must be between 0 and 360 degrees.")
        if not (0 <= saturation <= 100 and 0 <= lightness <= 100):
            raise ValueError("Saturation and lightness must be between 0 and 100.")
        if not (0 <= alpha <= 1):
            raise ValueError("Alpha must be between 0 and 1.")

        c = (1 - abs(2 * lightness / 100 - 1)) * saturation / 100
        x = c * (1 - abs((hue / 60) % 2 - 1))
        m = lightness / 100 - c / 2

        if hue < 60:
            r, g, b = c, x, 0
        elif hue < 120:
            r, g, b = x, c, 0
        elif hue < 180:
            r, g, b = 0, c, x
        elif hue < 240:
            r, g, b = 0, x, c
        elif hue < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x

        return Color.fromRGBA(int((r + m) * 255), int((g + m) * 255), int((b + m) * 255), alpha)

Color.BLACK = Color(0x000000FF)
Color.RED = Color(0xFF0000FF)
Color.GREEN = Color(0x00FF00FF)
Color.BLUE = Color(0x0000FFFF)
Color.YELLOW = Color(0xFFFF00FF)
Color.CYAN = Color(0x00FFFFFF)
Color.MAGENTA = Color(0xFF00FFFF)
Color.WHITE = Color(0xFFFFFFFF)
Color.GREY = Color(0x808080FF)
Color.ORANGE = Color(0xFFA500FF)
Color.PURPLE = Color(0x800080FF)
Color.BROWN = Color(0xA52A2AFF)
Color.PINK = Color(0xFFC0CBFF)
Color.LIGHTBLUE = Color(0xADD8E6)
Color.TRANSPARENT = Color(0xFFFFFF00)
