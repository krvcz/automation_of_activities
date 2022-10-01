import webbrowser
from pynput.mouse import Controller as mconn
from pynput.mouse import Button, Listener, Events
from pynput.keyboard import Controller as kconn
from pynput.keyboard import Key
import json
import time

mouse = mconn()
keyboard = kconn()

mapper = {'Move' : 'set_mouse_position', 'Click' : 'press_mouse_button' }

class Automat:
    def __init__(self, command_file, delay):
        self.command_list = self._parse_command_file(command_file)
        self.delay = delay
        self._mouse = mconn()
        self._keyboard = kconn()
        self._mouse_button = Button
        self._keyboard_button = Key
        self._mouse_listener = Events
        #self._keyboard_listener = Events

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


    def run_process(self):
        for task in self.command_list:
            var = getattr(self, task["eventType"])
            var(**task["payload"])
            time.sleep(self.delay)

    def record_process(self):
        tasks = []
        with self._mouse_listener() as events :
            for event in events:
                if getattr(event, 'button', 0) == self._mouse_button.right:
                    break
                else:
                    method = str(event)[:str(event).index('(')]
                    parameters = str(event)[str(event).index('('):].replace('=', ':').replace('(', '').replace(')', '').strip()
                    parameters_list = parameters.split(', ')
                    parameters_dict = {item[:item.index(':')] : item[item.index(':') + 1 :] for item in parameters_list }
                    task = {"eventType" : mapper[method],
                             "payload" : parameters_dict}
                    tasks.append(task)

        print(tasks)
        with open('./data.json', 'w', encoding='utf-8') as f:
            json.dump(tasks , f, ensure_ascii=False, indent=4)

automat = Automat('./data.json', 0.005)
automat.run_process()
# automat.record_process()
