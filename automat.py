import webbrowser
import json
import time
from pynput.mouse import Controller as mconn
from pynput.mouse import Button, Events
from pynput.keyboard import Controller as kconn
from pynput.keyboard import Key
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener





class Automat:
    def __init__(self, delay):
        self.command_list = None
        self.delay = delay
        self._mouse = mconn()
        self._keyboard = kconn()
        self._mouse_button = Button
        self._keyboard_button = Key
        self.keyboard_listener = KeyboardListener(on_press=self.on_press)
        self.mouse_listener = MouseListener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)


    def on_press(self, key):
        if key == self._keyboard_button.esc:
            self.keyboard_listener.stop()
            self.mouse_listener.stop()
        else:
            self.command_list.append({"eventType": 'press_keyboard_button',
                                        "payload": {
                                            'button': str(key).replace('Key.', '').replace("'", "")
                                        }
                                        })

    def on_release(self, key):
        self.command_list.append({"eventType": 'press_keyboard_button',
                                  "payload": {
                                      'button': str(key).replace('Key.', '').replace("'", "")
                                  }
                                  })


    def on_move(self, x, y):
        self.command_list.append({"eventType": 'set_mouse_position',
               "payload": {
                   'x': x,
                   'y' : y
               }
               })


    def on_click(self, x, y, button, pressed):
        self.command_list.append({"eventType": 'press_mouse_button',
               "payload": {
                   'button': str(button).replace('Button.', '')
               }
               })

    def on_scroll(self, x, y, dx, dy):
        self.command_list.append({"eventType": 'scroll_page',
                                  "payload": {
                                      'dx': dx,
                                      'dy' : dy
                                  }
                                  })


    @staticmethod
    def _parse_command_file(command_file):
        with open(command_file) as file:
            data = json.load(file)
            if isinstance(data, (dict, list)):
                pass
            else:
                raise TypeError('Invalid JSON format')
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

    def press_mouse_button(self, button, release=True, **kwargs):
        if release:
            self._mouse.press(getattr(self._mouse_button, button))
            self._mouse.release(getattr(self._mouse_button, button))
        else:
            self._mouse.press(getattr(self._mouse_button, button))

    def press_keyboard_button(self, button, release=True, **kwargs):
        if release:
            self._keyboard.press(getattr(self._keyboard_button, button, button))
            self._keyboard.release(getattr(self._keyboard_button, button, button))
        else:
            self._keyboard.press(getattr(self._keyboard_button, button, button))

    def set_mouse_position(self, x, y, **kwargs):
        self._mouse.position = (x, y)

    def type_word(self, word, **kwargs):
        self._keyboard.type(word)

    def scroll_page(self, dx, dy, **kwargs):
        self._mouse.scroll(dx, dy)


    def run_process(self, command_file = None):
        if command_file is None and self.command_list is None:
            raise Exception('Missing JSON file. \n Upload JSON file or record macro')
        elif command_file is not None:
            self.command_list = self._parse_command_file(command_file)
        for task in self.command_list:
            var = getattr(self, task["eventType"])
            var(**task["payload"])
            time.sleep(self.delay)

    def record_process(self):
        if self.command_list is None:
            self.command_list = []

        self.keyboard_listener.start()
        self.mouse_listener.start()
        self.keyboard_listener.join()
        self.mouse_listener.join()


    def save_recorded_process(self):
        with open('./data.json', 'w', encoding='utf-8') as file:
            json.dump(self.command_list , file, ensure_ascii=False, indent=4)
