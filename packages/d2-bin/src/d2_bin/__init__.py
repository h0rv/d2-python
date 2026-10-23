import os
import sys
import sysconfig


def _user_scheme() -> str:
    if sys.platform == "win32":
        return "nt_user"
    if sys.platform == "darwin" and sys._framework:
        return "osx_framework_user"
    return "posix_user"


def find_d2_bin() -> str:
    exe = "d2.exe" if sys.platform == "win32" else "d2"
    scripts_dirs = [
        sysconfig.get_path("scripts"),
        sysconfig.get_path("scripts", scheme=_user_scheme()),
        os.path.join(sys.prefix, "Scripts" if sys.platform == "win32" else "bin"),
    ]
    for directory in scripts_dirs:
        path = os.path.join(directory, exe)
        if os.path.isfile(path):
            return path
    raise FileNotFoundError(f"{exe} not found in: {', '.join(scripts_dirs)}")
