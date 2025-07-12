from d2.connection import Connection
from d2.connection import Direction


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
