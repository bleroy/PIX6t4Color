from pix6t4.bitmap import Bitmap
from pix6t4.color import Color
from pix6t4.game import Game
from pix6t4.console import PIX6T4Color
from pix6t4.console import Button

class SettingsScreen:
    """Settings screen for PIX6T4 Color."""
    def __init__(self, pix6t4: PIX6T4Color):
        """Initialize the settings screen."""
        self.pix6t4 = pix6t4

    def display(self):
        """Display the settings screen."""
        pass

    def handle_up(self):
        """Handle up button press."""
        raise NotImplementedError("This method should be overridden in subclasses.")
    
    def handle_down(self):
        """Handle down button press."""
        raise NotImplementedError("This method should be overridden in subclasses.")
    
    def handle_A(self):
        """Handle A button press."""
        raise NotImplementedError("This method should be overridden in subclasses.")

class BrightnessSettings(SettingsScreen):
    def display(self):
        Bitmap.from_ascii_art("""
o  @   o
 @ o  @ 
  o@@o  
  @@@@o@
@o@@@@  
  o@@o  
 @  o @ 
o   @  o
                              """,
                              {'@': Color(0xFFF200FF), 'o': Color(0xFFF9BDFF)}).blit(0, 0, 8, 8, self.pix6t4.pixels)
        
    def handle_up(self):
        """Increase brightness."""
        self.pix6t4.brightness = min(self.pix6t4.brightness + 0.1, 1.0)
        self.display()

    def handle_down(self):
        """Decrease brightness."""
        self.pix6t4.brightness = max(self.pix6t4.brightness - 0.1, 0.0)
        self.display()

    def handle_A(self):
        pass

class VolumeSettings(SettingsScreen):
    def display(self):
        Bitmap.from_ascii_art("""
   o o. 
  @@  o.
@@ @. .o
@@ @ o o
@@ @ o o
@@ @. .o
  @@  o 
   o o. """ if self.pix6t4.sound_enabled else """
   o   X
  @@  X 
@@ @ X  
@@ @X   
@@ X    
@@X@    
 X@@    
X  o    """, {'@': Color.BLACK, 'o': Color(0x464646FF), '.': Color(0xB4B4B4FF), 'X': Color.RED}).blit(0, 0, 8, 8, self.pix6t4.pixels)
        
    def handle_up(self):
        """Sound on"""
        self.pix6t4.enable_sound(True)
        self.pix6t4.beep()
        self.display()

    def handle_down(self):
        """Sound off"""
        self.pix6t4.enable_sound(False)
        self.display()

    def handle_A(self):
        """Toggle sound on/off."""
        self.pix6t4.enable_sound(not self.pix6t4.sound_enabled)
        if (self.pix6t4.sound_enabled):
            self.pix6t4.beep()
        self.display()

settings_screens = [BrightnessSettings, VolumeSettings]

class Settings(Game):
    """Settings app for PIX6T4 Color."""
    name = "Settings"
    priority = 9000 # Settings app should always be last

    def __init__(self, pix6t4: PIX6T4Color):
        """Initialize the settings app."""
        super().__init__(pix6t4)
        self.pix6t4 = pix6t4
        self.current_screen_index = 0
        self.screens = [settings_screen(pix6t4) for settings_screen in settings_screens]

    def title_screen(self):
        """Display the title screen for the settings app."""
        Bitmap.from_ascii_art("""
 . .O . 
.O.Oo.O.
 .oooo. 
Ooo..oO.
.Oo..ooO
 .oooo. 
.O.oO.O.
 . O. . 
            """, {'.': Color(0xB4B4B4FF), 'o': Color(0x464646FF), 'O': Color.BLACK}).blit(0, 0, 8, 8, self.pix6t4.pixels)
    
    def start(self):
        """Start the app."""
        self.current_screen_index = 0
        self.screens[self.current_screen_index].display()
    
    def loop(self):
        pass

    def handle_button_pressed(self, button):
        """Handle button press events in settings mode."""
        if button == Button.RIGHT:
            self.current_screen_index = (self.current_screen_index + 1) % len(self.screens)
            self.screens[self.current_screen_index].display()
        elif button == Button.LEFT:
            self.current_screen_index = (self.current_screen_index - 1) % len(self.screens)
            self.screens[self.current_screen_index].display()
        # Delegate other button handling to the current screen
        elif button == Button.UP:
            self.screens[self.current_screen_index].handle_up()
        elif button == Button.DOWN:
            self.screens[self.current_screen_index].handle_down()
        elif button == Button.A:
            self.screens[self.current_screen_index].handle_A()

main = Settings