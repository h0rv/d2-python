import sys
from importlib.metadata import distribution
from pathlib import Path


def find_d2_bin() -> str:
    exe = "d2.exe" if sys.platform == "win32" else "d2"
    for file in distribution("d2-bin").files or ():
        if file.name == exe and file.parent.name in {"bin", "Scripts"}:
            path = Path(str(file.locate())).resolve()
            if path.is_file():
                return str(path)
    raise FileNotFoundError(f"{exe} is missing from the d2-bin installation")
