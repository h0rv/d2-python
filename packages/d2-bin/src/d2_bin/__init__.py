import sys
import sysconfig
from pathlib import Path


def _user_scheme() -> str:
    if sys.platform == "win32":
        return "nt_user"
    framework = sysconfig.get_config_var("PYTHONFRAMEWORK")
    if sys.platform == "darwin" and isinstance(framework, str) and framework != "":
        return "osx_framework_user"
    return "posix_user"


def find_d2_bin() -> str:
    exe = "d2.exe" if sys.platform == "win32" else "d2"
    scripts_dirs = [
        sysconfig.get_path("scripts"),
        sysconfig.get_path("scripts", scheme=_user_scheme()),
        str(Path(sys.prefix) / ("Scripts" if sys.platform == "win32" else "bin")),
    ]
    for directory in scripts_dirs:
        path = Path(directory) / exe
        if path.is_file():
            return str(path)
    raise FileNotFoundError(f"{exe} not found in: {', '.join(scripts_dirs)}")
