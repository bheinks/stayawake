import sys
from pathlib import Path

def resource_path(relative_path):
    base_path = Path(getattr(sys, "_MEIPASS", Path(sys.argv[0]).resolve().parent))
    return base_path / relative_path
