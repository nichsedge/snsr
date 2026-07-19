import random
import time


class PynputBackend:
    name = "pynput"

    def __init__(self):
        from pynput.keyboard import Controller as KeyboardController
        from pynput.mouse import Controller as MouseController
        self.mouse = MouseController()
        self.keyboard = KeyboardController()

    def jiggle_mouse(self):
        dx = random.randint(-150, 150)
        dy = random.randint(-150, 150)
        self.mouse.move(dx, dy)
        time.sleep(0.1)
        self.mouse.move(-dx, -dy)

    def tap_key(self, key):
        self.keyboard.press(key)
        self.keyboard.release(key)
