import shutil
import subprocess
from typing import Literal

from .diagram import Diagram


class D2Error(Exception):
    pass


def find_d2() -> str:
    try:
        from d2_bin import find_d2_bin
    except ImportError:
        path = shutil.which("d2")
        if path is None:
            raise FileNotFoundError(
                "d2 is not installed: pip install 'd2-python[bin]' or see https://d2lang.com/tour/install"
            ) from None
        return path
    return find_d2_bin()


def render(
    diagram: Diagram | str,
    format: Literal["svg", "png", "pdf", "txt"] = "svg",
    *,
    layout: Literal["dagre", "elk", "tala"] | None = None,
    theme: int | None = None,
) -> bytes:
    command = [find_d2()]
    if layout is not None:
        command += ["--layout", layout]
    if theme is not None:
        command += ["--theme", str(theme)]
    command += ["--stdout-format", format, "-", "-"]

    result = subprocess.run(command, input=str(diagram).encode(), capture_output=True, check=False)
    if result.returncode != 0:
        raise D2Error(result.stderr.decode(errors="replace"))
    return result.stdout
