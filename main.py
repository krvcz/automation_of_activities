import webbrowser
from pynput.mouse import Controller as mconn
from pynput.mouse import Button
from pynput.keyboard import Controller as kconn
from pynput.keyboard import Key
import json
import time

mouse = mconn()
keyboard = kconn()



class Automat:
    def __init__(self, command_file, delay):
        self.command_list = self._parse_command_file(command_file)
        self.delay = delay
        self._mouse = mconn()
        self._keyboard = kconn()
        self._mouse_button = Button
        self._keyboard_button = Key

    @staticmethod
    def _parse_command_file(command_file):
        with open(command_file) as file:
            data = json.load(file)
            if isinstance(data, (dict, list)):
                pass
            else:
                raise TypeError('Niewłaściwy format pliku')
        return data

    @staticmethod
    def open_browser(url):
        webbrowser.open_new(url)
        time.sleep(8)

    @property
    def mouse(self):
        return self._mouse

    @property
    def keyboard(self):
        return self._keyboard

    def press_mouse_button(self, button, release=True):
        if release:
            self._mouse.press(getattr(self._mouse_button, button))
            self._mouse.release(getattr(self._mouse_button, button))
        else:
            self._mouse.press(getattr(self._mouse_button, button))

    def press_keyboard_button(self, button, release=True):
        if release:
            self._keyboard.press(getattr(self._keyboard_button, button, button))
            self._keyboard.release(getattr(self._keyboard_button, button, button))
        else:
            self._keyboard.press(getattr(self._keyboard_button, button, button))

    def set_mouse_position(self, x, y):
        self._mouse.position = (x, y)

    def type_word(self, word):
        self._keyboard.type(word)

    def run_process(self):
        for task in self.command_list:
            var = getattr(self, task["eventType"])
            var(**task["payload"])
            time.sleep(self.delay)


automat = Automat('./action.json', 2)
automat.run_process()
# Read pointer position
# print('The current pointer position is {0}'.format(
#     mouse.position))
#
# # Set pointer position
# open_browser()
# mouse.position = (1850, 120)
# time.sleep(10)
# mouse.press(Button.left)
# mouse.release(Button.left)
# time.sleep(2)
# mouse.position = (900, 400)
# mouse.press(Button.left)
# mouse.release(Button.left)
# mouse.press(Button.left)
# mouse.press(Button.left)
# keyboard.press(Key.backspace)
# keyboard.release(Key.backspace)
# keyboard.type('40173')
# mouse.position = (900, 450)
# mouse.press(Button.left)
# mouse.release(Button.left)
# keyboard.type('9Perla1719@')
# mouse.position = (900, 520)
# mouse.press(Button.left)
# mouse.release(Button.left)

# # print('Now we have moved it to {0}'.format(
# #     mouse.position))
#
# # Move pointer relative to current position
# mouse.move(600, -5)
#
# # Press and release
# mouse.press(Button.left)
# mouse.release(Button.left)
#
# # Double click; this is different from pressing and releasing
# # twice on macOS
# mouse.click(Button.left, 2)
#
# # Scroll two steps down
# mouse.scroll(0, 2)
