import pytest

import d2
from d2._render import RenderFormat
from tests.test_d2.test_render import requires_d2


@requires_d2
def test_validate__accepts_valid_source() -> None:
    d2.validate("a -> b")


@requires_d2
def test_validate__accepts_a_diagram() -> None:
    d2.validate(d2.Diagram(shapes=[d2.Shape(name="a")]))


@requires_d2
def test_validate__raises_with_the_d2_message() -> None:
    with pytest.raises(d2.D2Error, match="maps must be terminated"):
        d2.validate("a -> {")


@requires_d2
def test_format__normalizes_source() -> None:
    assert d2.fmt("a->b\nx:{y}").split("\n")[:2] == ["a -> b", "x: {y}"]


@requires_d2
def test_format__is_idempotent() -> None:
    once = d2.fmt("a->b")

    assert d2.fmt(once) == once


@requires_d2
def test_format__returns_already_formatted_source_unchanged() -> None:
    assert d2.fmt("a -> b\n") == "a -> b\n"


@requires_d2
def test_format__raises_on_invalid_source() -> None:
    with pytest.raises(d2.D2Error):
        d2.fmt("a -> {")


@requires_d2
def test_render__new_features_compile_with_d2() -> None:
    diagram = d2.Diagram(
        variables={"who": "world"},
        legend=d2.Legend(shapes=[d2.Shape(name="k", label="Service")]),
        shapes=[
            d2.Shape(
                name="a",
                label="hello ${who}",
                shape=d2.ShapeType.c4_person,
                label_near="outside-top-center",
            ),
            d2.Shape(name="b", label=d2.Text("**bold**", "md")),
        ],
        connections=[d2.Connection("a", "b", d2.Text("*calls*", "md"))],
    )

    assert b"<svg" in d2.render(diagram, omit_version=True)


@requires_d2
def test_render__top_and_left_need_tala() -> None:
    diagram = d2.Diagram(shapes=[d2.Shape(name="a", top=10, left=10)])

    assert b"<svg" in d2.render(diagram, layout="tala")
    with pytest.raises(d2.D2Error, match="locked positions"):
        d2.render(diagram, layout="dagre")


@requires_d2
@pytest.mark.parametrize("format_", ["gif", "pptx", "pdf", "png"])
def test_render__other_formats_return_bytes(
    format_: RenderFormat,
) -> None:
    assert d2.render("a -> b", format_)
