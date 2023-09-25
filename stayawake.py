from functools import partial
from threading import Thread, Event

import pyautogui
import pystray
from PIL import Image
from util import resource_path, read_json, write_json

# Constants
ICON_ENABLED = Image.open(resource_path('assets/enabled.png'))
ICON_DISABLED = Image.open(resource_path('assets/disabled.png'))
CONFIG_PATH = resource_path('config.json')
DEFAULT_KEY = 'f24'
KEYS = pyautogui.KEY_NAMES
DEFAULT_INTERVAL = 5
INTERVALS = [1, 2, 3, 4, 5, 10, 15, 20, 30, 40, 50, 60]


class StayAwake:
    def __init__(self):
        self.key = DEFAULT_KEY
        self.interval = DEFAULT_INTERVAL
        self.exit = Event()
        self.disabled = Event()
        self.press_thread = Thread(target=self.press_loop)
        self.icon = self.build_icon()

    def start(self):
        self.read_config()
        self.press_thread.start()
        self.icon.run()

    def stop(self):
        self.exit.set()
        self.icon.stop()

    def build_icon(self):
        def key_setter(key):
            return lambda: self.set_key(key)

        def interval_setter(interval):
            return lambda: self.set_interval(interval)

        def key_selected(key, _):
            return key == self.key

        def interval_selected(interval, _):
            return interval == self.interval

        default_item = pystray.MenuItem(
            'Enabled',
            self.toggle_enabled,
            checked=lambda _: not self.disabled.is_set(),
            default=True,
        )

        key_menu = pystray.Menu(
            *[pystray.MenuItem(
                repr(k),
                key_setter(k),
                checked=partial(key_selected, k),
                radio=True) for k in KEYS
            ]
        )

        interval_menu = pystray.Menu(
            *[pystray.MenuItem(
                f'{i} seconds',
                interval_setter(i),
                checked=partial(interval_selected, i),
                radio=True) for i in INTERVALS
            ]
        )

        config_item = pystray.MenuItem(
            'Configuration',
            pystray.Menu(
                pystray.MenuItem('Key', key_menu),
                pystray.MenuItem('Interval', interval_menu)
            )
        )

        stop_item = pystray.MenuItem(
            'Exit',
            self.stop
        )

        return pystray.Icon(
            'stayawake',
            ICON_ENABLED,
            menu=pystray.Menu(default_item, config_item, stop_item)
        )

    def set_key(self, key):
        self.key = key
        self.write_config()

    def set_interval(self, interval):
        self.interval = interval
        self.write_config()

    def read_config(self):
        config = read_json(CONFIG_PATH)
        self.key = config.get('key', DEFAULT_KEY)
        self.interval = config.get('interval', DEFAULT_INTERVAL)

    def write_config(self):
        config = {'key': self.key, 'interval': self.interval}
        write_json(CONFIG_PATH, config)

    def toggle_enabled(self):
        if self.disabled.is_set():
            self.disabled.clear()
            self.icon.icon = ICON_ENABLED
        else:
            self.disabled.set()
            self.icon.icon = ICON_DISABLED

    def press_loop(self):
        while not self.exit.is_set():
            if not self.disabled.is_set():
                pyautogui.press(self.key)

            self.exit.wait(self.interval)


if __name__ == '__main__':
    stayawake = StayAwake()
    stayawake.start()
