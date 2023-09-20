from functools import partial
from threading import Thread, Event
from time import sleep

from PIL import Image
import pyautogui
import pystray

# Constants
pyautogui.PAUSE = 5
KEY = 'f20'
ICON_ENABLED = Image.open('enabled.png')
ICON_DISABLED = Image.open('disabled.png')


def main():
    running = Event()
    running.set()

    enabled = Event()
    enabled.set()

    press_thread = Thread(target=press_loop, args=(running, enabled))
    press_thread.start()

    icon = build_icon(running, enabled)
    icon.run()


def build_icon(running, enabled):
    default_item = pystray.MenuItem(
        'Enabled',
        partial(toggle_enabled, enabled),
        checked=lambda _: enabled.is_set(),
        default=True,
    )

    stop_item = pystray.MenuItem(
        'Exit',
        partial(stop, running)
    )

    return pystray.Icon(
        'stayawake',
        ICON_ENABLED,
        menu=pystray.Menu(default_item, stop_item)
    )


def toggle_enabled(enabled, icon, _):
    if enabled.is_set():
        enabled.clear()
        icon.icon = ICON_DISABLED
    else:
        enabled.set()
        icon.icon = ICON_ENABLED


def stop(running, icon, _):
    running.clear()
    icon.stop()


def press_loop(running, enabled):
    while running.is_set():
        if enabled.is_set():
            pyautogui.press(KEY)
        else:
            sleep(pyautogui.PAUSE)


if __name__ == '__main__':
    main()
