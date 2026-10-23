from d2.connection import Arrowhead
from d2.connection import ArrowheadShape
from d2.connection import Connection
from d2.connection import Direction
from d2.style import Style


def test_d2_connection_label():
    connection = Connection(shape_1="a", shape_2="b", label="c")
    assert str(connection) == "a -> b: c"


def test_d2_connection_no_label():
    connection = Connection(shape_1="a", shape_2="b")
    assert str(connection) == "a -> b"


def test_d2_connection_direction_to():
    connection = Connection(shape_1="a", shape_2="b", direction=Direction.TO)
    assert str(connection) == "a -> b"


def test_d2_connection_direction_from():
    connection = Connection(shape_1="a", shape_2="b", direction=Direction.FROM)
    assert str(connection) == "a <- b"


def test_d2_connection_direction_both():
    connection = Connection(shape_1="a", shape_2="b", direction=Direction.BOTH)
    assert str(connection) == "a <-> b"


def test_d2_connection_direction_none():
    connection = Connection(shape_1="a", shape_2="b", direction=Direction.NONE)
    assert str(connection) == "a -- b"


def test_d2_connection_uniqueness():
    connection = Connection(shape_1="a", shape_2="b", direction=Direction.TO)
    connection2 = Connection(shape_1="a", shape_2="b", direction=Direction.TO)
    assert connection == connection2


def test_d2_connection_label_is_quoted_when_needed():
    connection = Connection(shape_1="a", shape_2="b", label="x: y")
    assert str(connection) == 'a -> b: "x: y"'


def test_d2_connection_endpoints_stay_as_given():
    connection = Connection(shape_1="a.b", shape_2="c.d")
    assert str(connection) == "a.b -> c.d"


def test_d2_connection_style():
    connection = Connection(shape_1="a", shape_2="b", style=Style(stroke="red", animated=True))
    assert str(connection) == "\n".join(
        ["a -> b: {", "  style: {", "    stroke: red", "    animated: true", "  }", "}"]
    )


def test_d2_connection_tooltip():
    connection = Connection(shape_1="a", shape_2="b", label="c", tooltip="tip")
    assert str(connection) == "a -> b: c {\n  tooltip: tip\n}"


def test_d2_connection_arrowheads():
    connection = Connection(
        shape_1="a",
        shape_2="b",
        source_arrowhead=Arrowhead(ArrowheadShape.DIAMOND, label="1", filled=True),
        target_arrowhead=Arrowhead(ArrowheadShape.CF_MANY),
    )
    assert str(connection) == "\n".join(
        [
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
    )


def test_d2_connection_arrowhead_unfilled():
    arrowhead = Arrowhead(ArrowheadShape.CIRCLE, filled=False)
    assert arrowhead.lines("target-arrowhead") == [
        "target-arrowhead: {",
        "  shape: circle",
        "  style.filled: false",
        "}",
    ]


def test_d2_connection_equality_includes_new_fields():
    base = Connection(shape_1="a", shape_2="b")
    assert base == Connection(shape_1="a", shape_2="b")
    assert base != Connection(shape_1="a", shape_2="b", tooltip="tip")
