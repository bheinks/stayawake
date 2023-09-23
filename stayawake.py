from functools import partial
from threading import Thread, Event

import pyautogui
import pystray
from PIL import Image
from util import resource_path, start_file, read_toml

# Constants
ICON_ENABLED = Image.open(resource_path('assets/enabled.png'))
ICON_DISABLED = Image.open(resource_path('assets/disabled.png'))
CONFIG_PATH = resource_path('config.toml')
DEFAULT_KEY = 'f24'
DEFAULT_KEYS = pyautogui.KEY_NAMES
DEFAULT_INTERVAL = 5
DEFAULT_INTERVALS = [1, 2, 3, 4, 5, 10, 15, 20, 30, 40, 50, 60]


class StayAwake:
    def __init__(self):
        self.key = DEFAULT_KEY
        self.interval = DEFAULT_INTERVAL
        self.exit = Event()
        self.disabled = Event()
        self.press_thread = Thread(target=self.press_loop)
        self.icon = self.build_icon()
    
    def start(self):
        self.load_config()
        self.press_thread.start()
        self.icon.run()

    def stop(self):
        self.exit.set()
        self.icon.stop()

    def build_icon(self):
        def build_key_setter(key):
            return lambda: self.set_key(key)

        def build_interval_setter(interval):
            return lambda: self.set_interval(interval)

        default_item = pystray.MenuItem(
            'Enabled',
            self.toggle_enabled,
            checked=lambda _: not self.disabled.is_set(),
            default=True,
        )

        key_menu = pystray.Menu(
            *[pystray.MenuItem(repr(k), build_key_setter(k), radio=True) for k in DEFAULT_KEYS]
        )

        interval_menu = pystray.Menu(
            *[pystray.MenuItem(f'{i} secs', build_interval_setter(i), radio=True) for i in DEFAULT_INTERVALS]
        )

        config_item = pystray.MenuItem(
            'Configuration',
            pystray.Menu(
                pystray.MenuItem('Keys', key_menu),
                pystray.MenuItem('Intervals', interval_menu)
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

    def set_interval(self, interval):
        self.interval = interval

    def edit_config(self):
        start_file(CONFIG_PATH)
        self.load_config()
    
    def load_config(self):
        config = read_toml(CONFIG_PATH)
        self.key = config.get('key', DEFAULT_KEY)
        self.interval = config.get('interval', DEFAULT_INTERVAL)

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
                print(f'pressing {self.key}')

            self.exit.wait(self.interval)


if __name__ == '__main__':
    stayawake = StayAwake()
    stayawake.start()
