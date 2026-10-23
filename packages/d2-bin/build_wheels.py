# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
import argparse
import base64
import hashlib
import io
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Literal, NamedTuple

D2_VERSION = "0.9.0"
WHEEL_VERSION = "0.9.0.post1"
D2_TAG = f"v{D2_VERSION}"
RELEASE_URL = f"https://github.com/terrastruct/d2/releases/download/{D2_TAG}"

Platform = Literal[
    "linux-amd64",
    "linux-arm64",
    "macos-amd64",
    "macos-arm64",
    "windows-amd64",
    "windows-arm64",
]

WHEEL_TAGS: dict[Platform, str] = {
    "linux-amd64": "manylinux_2_17_x86_64.manylinux2014_x86_64.musllinux_1_1_x86_64",
    "linux-arm64": "manylinux_2_17_aarch64.manylinux2014_aarch64.musllinux_1_1_aarch64",
    "macos-amd64": "macosx_10_12_x86_64",
    "macos-arm64": "macosx_11_0_arm64",
    "windows-amd64": "win_amd64",
    "windows-arm64": "win_arm64",
}

PACKAGE_DIR = Path(__file__).resolve().parent
DIST_INFO = f"d2_bin-{WHEEL_VERSION}.dist-info"
ENTRY_POINTS = b"[console_scripts]\nd2-bin = d2_bin.__main__:main\n"
DATA_DIR = f"d2_bin-{WHEEL_VERSION}.data"
LICENSE_FILES = ("LICENSE.txt", "THIRD_PARTY_NOTICES.txt")
SUMMARY = (
    "The unmodified official D2 diagram scripting language binary,"
    " packaged as a Python wheel."
)


class Arguments(argparse.Namespace):
    platforms: list[Platform]
    out_dir: Path


class WheelFile(NamedTuple):
    path: str
    content: bytes
    mode: int


def download(url: str) -> bytes:
    with urllib.request.urlopen(url) as response:
        return response.read()


def read_checksums() -> dict[str, str]:
    lines = download(f"{RELEASE_URL}/SHA256SUMS").decode().splitlines()
    return {
        name: digest
        for digest, name in (line.split() for line in lines if line.strip())
    }


def fetch_release(platform: Platform, checksums: dict[str, str]) -> tarfile.TarFile:
    name = f"d2-{D2_TAG}-{platform}.tar.gz"
    data = download(f"{RELEASE_URL}/{name}")
    actual = hashlib.sha256(data).hexdigest()
    if actual != checksums[name]:
        raise ValueError(
            f"checksum mismatch for {name}: expected {checksums[name]}, got {actual}"
        )
    return tarfile.open(fileobj=io.BytesIO(data), mode="r:gz")


def read_member(archive: tarfile.TarFile, name: str) -> bytes:
    member = archive.extractfile(f"d2-{D2_TAG}/{name}")
    if member is None:
        raise ValueError(f"{name} is not a regular file in the archive")
    return member.read()


def metadata() -> bytes:
    readme = (PACKAGE_DIR / "README.md").read_text(encoding="utf-8")
    headers = [
        "Metadata-Version: 2.4",
        "Name: d2-bin",
        f"Version: {WHEEL_VERSION}",
        f"Summary: {SUMMARY}",
        "Description-Content-Type: text/markdown",
        "License-Expression: MPL-2.0",
        "License-File: LICENSE.txt",
        "License-File: THIRD_PARTY_NOTICES.txt",
        "Requires-Python: >=3.8",
        "Project-URL: Homepage, https://github.com/terrastruct/d2",
        "Project-URL: Repository, https://github.com/h0rv/d2-python",
    ]
    return ("\n".join(headers) + "\n\n" + readme).encode()


def wheel_file(tag: str) -> bytes:
    lines = [
        "Wheel-Version: 1.0",
        "Generator: d2-bin build_wheels.py",
        "Root-Is-Purelib: false",
    ]
    lines += [f"Tag: py3-none-{part}" for part in tag.split(".")]
    return ("\n".join(lines) + "\n").encode()


def record(files: list[WheelFile]) -> bytes:
    rows = []
    for file in files:
        digest = (
            base64.urlsafe_b64encode(hashlib.sha256(file.content).digest())
            .rstrip(b"=")
            .decode()
        )
        rows.append(f"{file.path},sha256={digest},{len(file.content)}")
    rows.append(f"{DIST_INFO}/RECORD,,")
    return ("\n".join(rows) + "\n").encode()


def build_wheel(platform: Platform, checksums: dict[str, str], out_dir: Path) -> Path:
    tag = WHEEL_TAGS[platform]
    exe = "d2.exe" if platform.startswith("windows") else "d2"
    with fetch_release(platform, checksums) as archive:
        binary = read_member(archive, f"bin/{exe}")
        licenses = [
            WheelFile(f"{DIST_INFO}/licenses/{name}", read_member(archive, name), 0o644)
            for name in LICENSE_FILES
        ]

    files = [
        WheelFile(
            "d2_bin/__init__.py",
            (PACKAGE_DIR / "src/d2_bin/__init__.py").read_bytes(),
            0o644,
        ),
        WheelFile(
            "d2_bin/__main__.py",
            (PACKAGE_DIR / "src/d2_bin/__main__.py").read_bytes(),
            0o644,
        ),
        WheelFile(f"{DATA_DIR}/scripts/{exe}", binary, 0o755),
        WheelFile(f"{DIST_INFO}/METADATA", metadata(), 0o644),
        WheelFile(f"{DIST_INFO}/WHEEL", wheel_file(tag), 0o644),
        WheelFile(f"{DIST_INFO}/entry_points.txt", ENTRY_POINTS, 0o644),
        *licenses,
    ]
    files.append(WheelFile(f"{DIST_INFO}/RECORD", record(files), 0o644))

    out_dir.mkdir(parents=True, exist_ok=True)
    wheel_path = out_dir / f"d2_bin-{WHEEL_VERSION}-py3-none-{tag}.whl"
    with zipfile.ZipFile(wheel_path, "w", zipfile.ZIP_DEFLATED) as wheel:
        for file in files:
            info = zipfile.ZipInfo(file.path, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100000 | file.mode) << 16
            wheel.writestr(info, file.content)
    return wheel_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build d2-bin wheels from the official D2 release binaries."
    )
    parser.add_argument("platforms", nargs="*", choices=list(WHEEL_TAGS))
    parser.add_argument("--out-dir", type=Path, default=Path("dist"))
    args = parser.parse_args(namespace=Arguments())

    checksums = read_checksums()
    for platform in args.platforms or list(WHEEL_TAGS):
        sys.stdout.write(f"{build_wheel(platform, checksums, args.out_dir)}\n")


if __name__ == "__main__":
    main()
