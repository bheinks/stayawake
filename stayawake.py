from threading import Thread, Event

import pyautogui
import pystray
from PIL import Image
from util import resource_path, start_file, read_toml

# Constants
ICON_ENABLED = Image.open(resource_path('assets/enabled.png'))
ICON_DISABLED = Image.open(resource_path('assets/disabled.png'))
CONFIG_PATH = resource_path('config.toml')
KEY_DEFAULT = 'f24'
INTERVAL_DEFAULT = 5


class StayAwake:
    def __init__(self):
        self.key = KEY_DEFAULT
        self.interval = INTERVAL_DEFAULT
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
        default_item = pystray.MenuItem(
            'Enabled',
            self.toggle_enabled,
            checked=lambda _: not self.disabled.is_set(),
            default=True,
        )

        edit_item = pystray.MenuItem(
            'Edit configuration',
            self.edit_config
        )

        stop_item = pystray.MenuItem(
            'Exit',
            self.stop
        )

        return pystray.Icon(
            'stayawake',
            ICON_ENABLED,
            menu=pystray.Menu(default_item, edit_item, stop_item)
        )

    def edit_config(self):
        start_file(CONFIG_PATH)
        self.load_config()
    
    def load_config(self):
        config = read_toml(CONFIG_PATH)
        self.key = config.get('key', KEY_DEFAULT)
        self.interval = config.get('interval', INTERVAL_DEFAULT)

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
