from d2.connection import Arrowhead, ArrowheadShape, Connection, Direction
from d2.style import Style


def test_d2_connection_label() -> None:
    connection = Connection(shape_1="a", shape_2="b", label="c")
    assert str(connection) == "a -> b: c"


def test_d2_connection_no_label() -> None:
    connection = Connection(shape_1="a", shape_2="b")
    assert str(connection) == "a -> b"


def test_d2_connection_direction_to() -> None:
    connection = Connection(shape_1="a", shape_2="b", direction=Direction.TO)
    assert str(connection) == "a -> b"


def test_d2_connection_direction_from() -> None:
    connection = Connection(shape_1="a", shape_2="b", direction=Direction.FROM)
    assert str(connection) == "a <- b"


def test_d2_connection_direction_both() -> None:
    connection = Connection(shape_1="a", shape_2="b", direction=Direction.BOTH)
    assert str(connection) == "a <-> b"


def test_d2_connection_direction_none() -> None:
    connection = Connection(shape_1="a", shape_2="b", direction=Direction.NONE)
    assert str(connection) == "a -- b"


def test_d2_connection_uniqueness() -> None:
    connection = Connection(shape_1="a", shape_2="b", direction=Direction.TO)
    connection2 = Connection(shape_1="a", shape_2="b", direction=Direction.TO)
    assert connection == connection2


def test_d2_connection_label_is_quoted_when_needed() -> None:
    connection = Connection(shape_1="a", shape_2="b", label="x: y")
    assert str(connection) == 'a -> b: "x: y"'


def test_d2_connection_endpoints_stay_as_given() -> None:
    connection = Connection(shape_1="a.b", shape_2="c.d")
    assert str(connection) == "a.b -> c.d"


def test_d2_connection_style() -> None:
    connection = Connection(
        shape_1="a", shape_2="b", style=Style(stroke="red", animated=True)
    )
    expected_lines = [
        "a -> b: {",
        "  style: {",
        "    stroke: red",
        "    animated: true",
        "  }",
        "}",
    ]
    assert str(connection) == "\n".join(expected_lines)


def test_d2_connection_tooltip() -> None:
    connection = Connection(shape_1="a", shape_2="b", label="c", tooltip="tip")
    assert str(connection) == "a -> b: c {\n  tooltip: tip\n}"


def test_d2_connection_arrowheads() -> None:
    connection = Connection(
        shape_1="a",
        shape_2="b",
        source_arrowhead=Arrowhead(ArrowheadShape.DIAMOND, label="1", filled=True),
        target_arrowhead=Arrowhead(ArrowheadShape.CF_MANY),
    )
    expected_lines = [
        "a -> b: {",
        "  source-arrowhead: {",
        "    shape: diamond",
        "    label: 1",
        "    style.filled: true",
        "  }",
        "  target-arrowhead: {",
        "    shape: cf-many",
        "  }",
        "}",
    ]
    assert str(connection) == "\n".join(expected_lines)


def test_d2_connection_arrowhead_unfilled() -> None:
    arrowhead = Arrowhead(ArrowheadShape.CIRCLE, filled=False)
    assert arrowhead.lines("target-arrowhead") == [
        "target-arrowhead: {",
        "  shape: circle",
        "  style.filled: false",
        "}",
    ]


def test_d2_connection_equality_includes_new_fields() -> None:
    base = Connection(shape_1="a", shape_2="b")
    assert base == Connection(shape_1="a", shape_2="b")
    assert base != Connection(shape_1="a", shape_2="b", tooltip="tip")
