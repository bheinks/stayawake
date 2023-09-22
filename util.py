import sys
import tomllib
from pathlib import Path
from platform import system

if system() == 'Windows':
    from os import startfile
else:
    from subprocess import call


def resource_path(relative_path):
    base_path = Path(getattr(sys, "_MEIPASS", Path(sys.argv[0]).resolve().parent))
    return base_path / relative_path


def start_file(path):
    if system() == 'Darwin':    # macOS
        call(('open', path))
    elif system() == 'Windows': # Windows
        startfile(path)
    else:                       # Linux
        call(('xdg-open', path))


def read_toml(path):
    try:
        with open(path, 'rb') as f:
            toml = tomllib.load(f)
    except (tomllib.TOMLDecodeError, FileNotFoundError):
        toml = {}
    
    return toml
