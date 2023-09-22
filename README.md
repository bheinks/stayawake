# stayawake ![stayawake](assets/enabled.png)

A simple Python program to keep your system from sleeping by pressing a key every couple of seconds.

## Requirements
```
pillow>=10.0.1
pystray>=0.19.5
pyautogui>=0.9.54
```

## Building
```
pdm install
pyinstaller stayawake.spec
```

The output is a single executable built for your current platform.

## Usage
This program is entirely system tray-based. A single click on the icon toggles between enabled and disabled. To exit, right click and select exit.

## TODO
- Make key pressed and interval configurable
- Add cross-platform support (Windows only currently)