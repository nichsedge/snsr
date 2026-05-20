import random


class PyAutoGuiBackend:
    name = "pyautogui"

    def __init__(self, failsafe=True):
        import pyautogui
        self._pyautogui = pyautogui
        pyautogui.FAILSAFE = failsafe
        self.width, self.height = pyautogui.size()

    def jiggle_mouse(self):
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)
        self._pyautogui.moveTo(x, y, duration=random.uniform(0.5, 2))

    def tap_key(self, key):
        self._pyautogui.press(key)
