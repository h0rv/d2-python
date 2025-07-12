from d2.connection import Connection
from d2.diagram import Diagram
from d2.shape import Shape
from d2.style import Style


def test_d2_diagram():
    diagram = Diagram()
    assert str(diagram) == ""


def test_d2_diagram_one_shape():
    diagram = Diagram()
    diagram.add_shape(Shape(name="shape_name"))
    assert str(diagram) == "shape_name"


def test_d2_diagram_two_shapes():
    shapes = [Shape(name="shape_name1"), Shape(name="shape_name2")]
    diagram = Diagram(shapes=shapes)
    assert str(diagram) == "\n".join(["shape_name1", "shape_name2"])


def test_d2_diagram_one_connection():
    shapes = [Shape(name="shape_name1"), Shape(name="shape_name2")]
    connections = [Connection(shape_1="shape_name1", shape_2="shape_name2")]

    diagram = Diagram(shapes=shapes, connections=connections)
    assert str(diagram) == "\n".join(["shape_name1", "shape_name2", "shape_name1 -> shape_name2"])


def test_d2_diagram_one_connection_imperative_connection():
    diagram = Diagram()
    diagram.add_shape(Shape(name="shape_name1"))
    diagram.add_shape(Shape(name="shape_name2"))
    diagram.add_connection(Connection(shape_1="shape_name1", shape_2="shape_name2"))
    assert str(diagram) == "\n".join(["shape_name1", "shape_name2", "shape_name1 -> shape_name2"])


def test_d2_diagram_one_connection_with_style():
    shapes = [
        Shape(name="shape_name1", style=Style(fill="red")),
        Shape(name="shape_name2", style=Style(fill="blue")),
    ]
    connections = [Connection(shape_1="shape_name1", shape_2="shape_name2")]

    diagram = Diagram(shapes=shapes, connections=connections)
    assert str(diagram) == "\n".join(
        [
            "shape_name1: {",
            "  style: {",
            "    fill: red",
            "  }",
            "}",
            "shape_name2: {",
            "  style: {",
            "    fill: blue",
            "  }",
            "}",
            "shape_name1 -> shape_name2",
        ]
    )
