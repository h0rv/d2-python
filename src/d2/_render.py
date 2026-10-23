import shutil
import subprocess
from typing import Literal

from d2.diagram import Diagram

RenderFormat = Literal["svg", "png", "pdf", "txt", "gif", "pptx"]


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


def run_d2(command: list[str], source: Diagram | str) -> bytes:
    result = subprocess.run(
        [find_d2(), *command],
        input=str(source).encode(),
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise D2Error(result.stderr.decode(errors="replace"))
    return result.stdout


def flag(name: str, *, value: str | float | bool | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, bool):
        return [f"--{name}={'true' if value else 'false'}"]
    return [f"--{name}", str(value)]


def render(
    diagram: Diagram | str,
    format: RenderFormat = "svg",
    *,
    layout: Literal["dagre", "elk", "tala"] | None = None,
    theme: int | None = None,
    target: str = "",
    dark_theme: int | None = None,
    sketch: bool | None = None,
    pad: int | None = None,
    scale: float | None = None,
    center: bool | None = None,
    omit_version: bool | None = None,
    no_xml_tag: bool | None = None,
    salt: str | None = None,
    animate_interval: int | None = None,
    ascii_mode: Literal["standard", "extended"] | None = None,
    timeout: int | None = None,
) -> bytes:
    options = (
        ("layout", layout),
        ("theme", theme),
        ("dark-theme", dark_theme),
        ("sketch", sketch),
        ("pad", pad),
        ("scale", scale),
        ("center", center),
        ("omit-version", omit_version),
        ("no-xml-tag", no_xml_tag),
        ("salt", salt),
        ("animate-interval", animate_interval),
        ("ascii-mode", ascii_mode),
        ("timeout", timeout),
    )
    command = [part for name, value in options for part in flag(name, value=value)]
    command += ["--target", target, "--stdout-format", format, "-", "-"]
    return run_d2(command, diagram)


def validate(source: Diagram | str) -> None:
    run_d2(["validate", "-"], source)


def format(source: Diagram | str) -> str:
    formatted = run_d2(["fmt", "-"], source).decode()
    return formatted if formatted != "" else str(source)
