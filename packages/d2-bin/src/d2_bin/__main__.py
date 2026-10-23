import os
import subprocess
import sys

from d2_bin import find_d2_bin


def main() -> None:
    d2 = find_d2_bin()
    if sys.platform == "win32":
        raise SystemExit(subprocess.call([d2, *sys.argv[1:]]))
    os.execvp(d2, [d2, *sys.argv[1:]])


if __name__ == "__main__":
    main()
