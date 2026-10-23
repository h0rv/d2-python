import d2


def test_raw__dedents_and_trims() -> None:
    raw = d2.Raw("""
        a -> b
          style.stroke: red
    """)

    assert raw.lines() == ["a -> b", "  style.stroke: red"]


def test_raw__blank_source_has_no_lines() -> None:
    assert d2.Raw("  \n ").lines() == []


def test_raw__parse_keeps_raw_and_wraps_str() -> None:
    raw = d2.Raw("x")

    assert d2.Raw.parse(raw) is raw
    assert d2.Raw.parse("x") == raw


def test_diagram__raw_is_appended_last() -> None:
    diagram = d2.Diagram(
        shapes=[d2.Shape(name="a"), d2.Shape(name="b")],
        connections=[d2.Connection("a", "b")],
        raw="(a -> b)[0].style.stroke: red",
    )
    diagram.add_raw(d2.Raw("a.style.fill: blue"))

    assert str(diagram).split("\n") == [
        "a",
        "b",
        "a -> b",
        "(a -> b)[0].style.stroke: red",
        "a.style.fill: blue",
    ]


def test_shape__raw_goes_inside_the_shape() -> None:
    shape = d2.Shape(name="a", raw="style.fill: red\nstyle.stroke: blue")

    assert str(shape) == "a: {\n  style.fill: red\n  style.stroke: blue\n}"


def test_connection__raw_goes_inside_the_connection() -> None:
    connection = d2.Connection("a", "b", raw="style.stroke: red")

    assert str(connection) == "a -> b: {\n  style.stroke: red\n}"


def test_layer__raw_diagram_is_nested() -> None:
    layer = d2.Layer("x", d2.Diagram(raw="a -> b"))
    diagram = d2.Diagram(layers=[layer])

    assert str(diagram) == "layers: {\n  x: {\n    a -> b\n  }\n}"
