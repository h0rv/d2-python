from d2.connection import Connection
from d2.diagram import Config, Diagram, Layer
from d2.shape import Shape
from d2.style import Style


def test_d2_diagram() -> None:
    diagram = Diagram()
    assert str(diagram) == ""


def test_d2_diagram_one_shape() -> None:
    diagram = Diagram()
    diagram.add_shape(Shape(name="shape_name"))
    assert str(diagram) == "shape_name"


def test_d2_diagram_two_shapes() -> None:
    shapes = [Shape(name="shape_name1"), Shape(name="shape_name2")]
    diagram = Diagram(shapes=shapes)
    expected_lines = ["shape_name1", "shape_name2"]
    assert str(diagram) == "\n".join(expected_lines)


def test_d2_diagram_one_connection() -> None:
    shapes = [Shape(name="shape_name1"), Shape(name="shape_name2")]
    connections = [Connection(shape_1="shape_name1", shape_2="shape_name2")]

    diagram = Diagram(shapes=shapes, connections=connections)
    expected_lines = ["shape_name1", "shape_name2", "shape_name1 -> shape_name2"]
    assert str(diagram) == "\n".join(expected_lines)


def test_d2_diagram_one_connection_imperative_connection() -> None:
    diagram = Diagram()
    diagram.add_shape(Shape(name="shape_name1"))
    diagram.add_shape(Shape(name="shape_name2"))
    diagram.add_connection(Connection(shape_1="shape_name1", shape_2="shape_name2"))
    expected_lines = ["shape_name1", "shape_name2", "shape_name1 -> shape_name2"]
    assert str(diagram) == "\n".join(expected_lines)


def test_d2_diagram_one_connection_with_style() -> None:
    shapes = [
        Shape(name="shape_name1", style=Style(fill="red")),
        Shape(name="shape_name2", style=Style(fill="blue")),
    ]
    connections = [Connection(shape_1="shape_name1", shape_2="shape_name2")]

    diagram = Diagram(shapes=shapes, connections=connections)
    expected_lines = [
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
    assert str(diagram) == "\n".join(expected_lines)


def test_d2_diagram_direction() -> None:
    diagram = Diagram(shapes=[Shape(name="a")], direction="right")
    assert str(diagram) == "direction: right\na"


def test_d2_diagram_classes() -> None:
    diagram = Diagram(classes={"hot": Style(fill="red"), "empty": Style()})
    expected_lines = [
        "classes: {",
        "  hot: {",
        "    style: {",
        "      fill: red",
        "    }",
        "  }",
        "}",
    ]
    assert str(diagram) == "\n".join(expected_lines)


def test_d2_diagram_config() -> None:
    diagram = Diagram(
        vars=Config(
            layout_engine="elk",
            theme_id=4,
            dark_theme_id=200,
            pad=0,
            sketch=True,
            center=False,
        )
    )
    expected_lines = [
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
    assert str(diagram) == "\n".join(expected_lines)


def test_d2_diagram_empty_config_is_omitted() -> None:
    assert str(Diagram(vars=Config())) == ""


def test_d2_diagram_scenarios_and_steps() -> None:
    inner = Diagram(connections=[Connection(shape_1="a", shape_2="b")])
    diagram = Diagram(
        scenarios=[Layer(name="alt", diagram=inner)],
        steps=[Layer(name="one", diagram=inner)],
    )
    expected_lines = [
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
    assert str(diagram) == "\n".join(expected_lines)


def test_d2_diagram_comments() -> None:
    diagram = Diagram(shapes=[Shape(name="a")], comments=["first\nsecond"])
    diagram.add_comment("third")
    assert str(diagram) == "# first\n# second\n# third\na"
