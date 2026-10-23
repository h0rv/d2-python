from pathlib import Path

import pytest

d2_bin = pytest.importorskip("d2_bin")


def test_find_d2_bin__returns_the_installed_binary() -> None:
    path = Path(d2_bin.find_d2_bin())

    assert path.is_file()
    assert path.name in {"d2", "d2.exe"}
