import random
from pix6t4.bitmap import Bitmap
from pix6t4.color import Color
from pix6t4.game import Game
from pix6t4.console import Button

class Snake(Game):
    """Snake game for PIX6T4 Color."""
    name = "Snake"

    def start(self):
        """Initialize the game."""
        self.pix6t4.cls()
        self.apples = []
        self.max_apples = 3
        self.apple_probability = 0.5
        self.paint_apples(self.apples)
        self.snake = [(4, 4), (4, 5)]
        self.paint_snake(self.snake)
        self.direction = (0, 1)
        self.slowness = 10
        self.min_slowness = 2
        self.alive = True
        self.frame_number = 0

    def title_screen(self):
        """Display the title screen for the game."""
        Bitmap.from_ascii_art(
            """
 ###    
#ggg##  
#gYggg# 
#gggg#r 
 ####  r
  #gg#  
   #gg# 
   #gg# 
            """, {'#': Color.fromRGB(0, 64, 0)}).blit(0, 0, 8, 8, self.pix6t4.pixels)

    def paint_snake(self, snake, color=Color.GREEN):
        """Paint the snake on the screen."""
        for segment in snake:
            self.pix6t4.plot(segment[0], segment[1], color)

    def paint_apples(self, apples, color=Color.RED):
        """Paint the apples on the screen."""
        for apple in apples:
            self.pix6t4.plot(apple[0], apple[1], color)

    def handle_button_pressed(self, button):
        """Handle button press events."""
        match button:
            case Button.UP:
                self.direction = (-1, 0) if self.direction != (1, 0) else self.direction
            case Button.DOWN:
                self.direction = (1, 0) if self.direction != (-1, 0) else self.direction
            case Button.LEFT:
                self.direction = (0, -1) if self.direction != (0, 1) else self.direction
            case Button.RIGHT:
                self.direction = (0, 1) if self.direction != (0, -1) else self.direction

    def loop(self):
        """The main game loop."""
        self.frame_number += 1
        # Skip frames based on slowness or if dead
        if (self.frame_number % self.slowness != 0) or not self.alive:
            return
        # Check if we need to add an apple
        if len(self.apples) < self.max_apples and random.random() < self.apple_probability:
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            if (x, y) not in self.snake and (x, y) not in self.apples:
                self.apples.append((x, y))
                self.paint_apples(self.apples)
        # Move the snake
        old_head = self.snake[-1]
        new_head = ((old_head[0] + self.direction[0]) % 8, (old_head[1] + self.direction[1]) % 8)
        if new_head in self.snake:
            # Snake bit itself. Game over.
            self.paint_snake(self.snake, Color.RED)
            self.alive = False
            self.pix6t4.beep(frequency=100, duration=500)
            pass
        else:
            self.snake.append(new_head)
            self.paint_snake([new_head])
            if new_head in self.apples:
                # Snake ate an apple. Grow the snake and remove the apple.
                self.apples.remove(new_head)
                # Also speed things up
                if self.slowness > self.min_slowness:
                    self.slowness -= 1
                self.pix6t4.beep(duration=100)
            else:
                # Remove the previous tail.
                self.pix6t4.plot(self.snake[0][0], self.snake[0][1], Color.BLACK)
                self.snake = self.snake[1:]

main = Snake