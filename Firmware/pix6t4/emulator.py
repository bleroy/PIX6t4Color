from time import sleep
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import pyaudio
from pix6t4.console import Button, PIX6T4Color

import sys

audio = pyaudio.PyAudio()

class SquareWaveIterable:
    """An iterable that generates a square wave sound."""
    def __init__(self, frequency, frame_count: int, start_frame: int = 0):
        self.frequency = frequency
        self.period = int(44100 / frequency)
        self.frame_count = frame_count
        self.start_frame = start_frame
        self.current_frame = start_frame

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_frame >= self.start_frame + self.frame_count:
            raise StopIteration
        sample = 0x00 if self.current_frame % self.period < self.period // 2 else 0xFF
        self.current_frame += 1
        return sample
    
class LedMatrix(QWidget):
    """ A simple LED matrix widget"""
    def __init__(self, pix6t4: PIX6T4Color, pixelSize=30, rows=8, cols=8, margin=2):
        super().__init__()
        self.pixelSize = pixelSize
        self.rows = rows
        self.cols = cols
        self.margin = margin
        self.pix6t4 = pix6t4
        self.setFixedSize(self.cols * self.pixelSize, self.rows * self.pixelSize)
        self.pixels = pix6t4.pixels
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(0, 0, self.width(), self.height(), QColor(32, 32, 32))
        for x, row in enumerate(self.pixels):
            for y, col in enumerate(row):
                color = QColor(self.pixels[x][y].with_brightness(self.pix6t4.brightness) >> 8)
                painter.fillRect(y * self.pixelSize + self.margin,
                                 x * self.pixelSize + self.margin,
                                 self.pixelSize - self.margin * 2,
                                 self.pixelSize - self.margin * 2,
                                 color)
        painter.end()
    
class MainWindow(QMainWindow):
    def __init__(self, pix6t4: PIX6T4Color):
        super().__init__()
        self.pix6t4 = pix6t4
        self.__setupUi()

    def __setupUi(self):
        self.setWindowTitle("PIX6T4 Color")
        self.resize(240, 240)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.widget = LedMatrix(self.pix6t4)
        self.widget.setGeometry(QRect(0, 0, 240, 240))
        self.widget.setAutoFillBackground(True)
        self.setCentralWidget(self.widget)

    def keyPressEvent(self, event):
        match event.key():
            case Qt.Key.Key_Escape:
                self.pix6t4.handle_button_pressed(Button.SELECT)
            case Qt.Key.Key_Enter | Qt.Key.Key_Return:
                self.pix6t4.handle_button_pressed(Button.START)
            case Qt.Key.Key_Up | Qt.Key.Key_W:
                self.pix6t4.handle_button_pressed(Button.UP)
            case Qt.Key.Key_Down | Qt.Key.Key_S:
                self.pix6t4.handle_button_pressed(Button.DOWN)
            case Qt.Key.Key_Left | Qt.Key.Key_A:
                self.pix6t4.handle_button_pressed(Button.LEFT)
            case Qt.Key.Key_Right | Qt.Key.Key_D:
                self.pix6t4.handle_button_pressed(Button.RIGHT)
            case Qt.Key.Key_Alt | Qt.Key.Key_Y:
                self.pix6t4.handle_button_pressed(Button.Y)
            case Qt.Key.Key_Backspace | Qt.Key.Key_Shift | Qt.Key.Key_B:
                self.pix6t4.handle_button_pressed(Button.B)
            case Qt.Key.Key_Control | Qt.Key.Key_X:
                self.pix6t4.handle_button_pressed(Button.X)
            case Qt.Key.Key_Space:
                self.pix6t4.handle_button_pressed(Button.A)

    def keyReleaseEvent(self, a0):
        match a0.key():
            case Qt.Key.Key_Up | Qt.Key.Key_W:
                self.pix6t4.handle_button_released(Button.UP)
            case Qt.Key.Key_Down | Qt.Key.Key_S:
                self.pix6t4.handle_button_released(Button.DOWN)
            case Qt.Key.Key_Left | Qt.Key.Key_A:
                self.pix6t4.handle_button_released(Button.LEFT)
            case Qt.Key.Key_Right | Qt.Key.Key_D:
                self.pix6t4.handle_button_released(Button.RIGHT)
            case Qt.Key.Key_Alt | Qt.Key.Key_Y:
                self.pix6t4.handle_button_released(Button.Y)
            case Qt.Key.Key_Backspace | Qt.Key.Key_Shift | Qt.Key.Key_B:
                self.pix6t4.handle_button_released(Button.B)
            case Qt.Key.Key_Control | Qt.Key.Key_X:
                self.pix6t4.handle_button_released(Button.X)
            case Qt.Key.Key_Space:
                self.pix6t4.handle_button_released(Button.A)

class PIX6T4ColorEmulator(PIX6T4Color):
    """Emulator for the PIX6T4 Color console."""
    def __init__(self):
        super().__init__()
        app = QApplication(sys.argv)
        window = MainWindow(self)
        self.window = window
        self.widget = window.widget
        self.timer = QTimer(window)
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.loop)
        self.timer.start()
        self.current_frame = 0
        self.stream = None
        self.stream_start = None
        self.stream_duration = 0
        window.show()
        sys.exit(app.exec())

    def render(self):
        """Render the current state of the PIX6T4 Color."""
        self.widget.pixels = self.pixels
        self.widget.repaint()

    def enable_sound(self, enabled = True):
        super().enable_sound(enabled)
        if (self.stream) != None and not enabled:
            self.stream.close()
            self.stream = None
    
    def stop_stream(self):
        if self.stream is not None:
            self.stream.close()
            self.stream = None

    def beep(self, frequency = 440, duration = 200):
        self.current_frame = 0
        self.stream_duration = duration
        if self.sound_enabled:
            def cb(_, frame_count, time_info, status):
                if (self.stream_start.addMSecs(self.stream_duration) < QDateTime.currentDateTime()):
                    return (bytes(0), pyaudio.paComplete)
                samples = bytes(SquareWaveIterable(frequency, frame_count, self.current_frame))
                self.current_frame += frame_count
                return (samples, pyaudio.paContinue)

            self.stop_stream()
            self.stream = audio.open(format=pyaudio.paInt8, channels=1, rate=44100, output=True, stream_callback=cb)
            self.stream.start_stream()
            self.stream_start = QDateTime.currentDateTime()

def main():
    """Run the PIX6T4 Color emulator."""
    emulator = PIX6T4ColorEmulator()
    emulator.run()
