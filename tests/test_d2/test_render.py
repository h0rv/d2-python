import shutil
import sys
from types import ModuleType

import pytest

import d2
from d2.render import find_d2


def has_d2() -> bool:
    try:
        find_d2()
    except FileNotFoundError:
        return False
    return True


requires_d2 = pytest.mark.skipif(not has_d2(), reason="d2 is not installed")


def test_find_d2__prefers_d2_bin(monkeypatch: pytest.MonkeyPatch) -> None:
    fake = ModuleType("d2_bin")
    monkeypatch.setattr(fake, "find_d2_bin", lambda: "/from/d2_bin/d2", raising=False)
    monkeypatch.setitem(sys.modules, "d2_bin", fake)
    monkeypatch.setattr(shutil, "which", lambda name: "/from/path/d2")

    assert find_d2() == "/from/d2_bin/d2"


def test_find_d2__falls_back_to_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(sys.modules, "d2_bin", None)
    monkeypatch.setattr(shutil, "which", lambda name: "/from/path/d2")

    assert find_d2() == "/from/path/d2"


def test_find_d2__raises_when_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(sys.modules, "d2_bin", None)
    monkeypatch.setattr(shutil, "which", lambda name: None)

    with pytest.raises(FileNotFoundError, match="d2 is not installed"):
        find_d2()


def test_render__missing_binary_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(sys.modules, "d2_bin", None)
    monkeypatch.setattr(shutil, "which", lambda name: None)

    with pytest.raises(FileNotFoundError, match="d2-python\\[bin\\]"):
        d2.render("a -> b")


@requires_d2
def test_render__svg() -> None:
    diagram = d2.Diagram(
        shapes=[d2.Shape(name="a"), d2.Shape(name="b")],
        connections=[d2.Connection(shape_1="a", shape_2="b")],
    )

    assert b"<svg" in d2.render(diagram)


@requires_d2
def test_render__txt() -> None:
    output = d2.render("a -> b", "txt").decode()

    assert "a" in output
    assert "b" in output


@requires_d2
def test_render__invalid_source_raises_d2_error() -> None:
    with pytest.raises(d2.D2Error):
        d2.render("a -> {")
