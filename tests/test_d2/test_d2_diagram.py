from d2.connection import Connection
from d2.diagram import Config
from d2.diagram import Diagram
from d2.diagram import Layer
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


def test_d2_diagram_direction():
    diagram = Diagram(shapes=[Shape(name="a")], direction="right")
    assert str(diagram) == "direction: right\na"


def test_d2_diagram_classes():
    diagram = Diagram(classes={"hot": Style(fill="red"), "empty": Style()})
    assert str(diagram) == "\n".join(["classes: {", "  hot: {", "    style: {", "      fill: red", "    }", "  }", "}"])


def test_d2_diagram_config():
    diagram = Diagram(vars=Config(layout_engine="elk", theme_id=4, dark_theme_id=200, pad=0, sketch=True, center=False))
    assert str(diagram) == "\n".join(
        [
            "vars: {",
            "  d2-config: {",
            "    layout-engine: elk",
            "    theme-id: 4",
            "    dark-theme-id: 200",
            "    pad: 0",
            "    sketch: true",
            "    center: false",
            "  }",
            "}",
        ]
    )


def test_d2_diagram_empty_config_is_omitted():
    assert str(Diagram(vars=Config())) == ""


def test_d2_diagram_scenarios_and_steps():
    inner = Diagram(connections=[Connection(shape_1="a", shape_2="b")])
    diagram = Diagram(scenarios=[Layer(name="alt", diagram=inner)], steps=[Layer(name="one", diagram=inner)])
    assert str(diagram) == "\n".join(
        [
            "scenarios: {",
            "  alt: {",
            "    a -> b",
            "  }",
            "}",
            "steps: {",
            "  one: {",
            "    a -> b",
            "  }",
            "}",
        ]
    )


def test_d2_diagram_comments():
    diagram = Diagram(shapes=[Shape(name="a")], comments=["first\nsecond"])
    diagram.add_comment("third")
    assert str(diagram) == "# first\n# second\n# third\na"
