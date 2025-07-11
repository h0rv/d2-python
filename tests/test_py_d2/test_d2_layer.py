from d2.connection import Connection
from d2.diagram import Diagram
from d2.diagram import Layer


def test_d2_layer():
    layer = Layer(name="my_layer")
    diagram = Diagram(layers=[layer])
    assert str(diagram) == ""


def test_d2_layer_single_subdiagram():
    """Test a root diagram with a connection and a single layer containing its own connection."""
    root_connection = Connection(shape_1="x", shape_2="y")

    layer_connection = Connection(shape_1="1", shape_2="2")
    layer_diagram = Diagram(connections=[layer_connection])

    layer = Layer(name="numbers", diagram=layer_diagram)

    root_diagram = Diagram(connections=[root_connection], layers=[layer])

    expected_output = "x -> y\nlayers: {\n  numbers: {\n    1 -> 2\n  }\n}"

    assert str(root_diagram) == expected_output


def test_d2_layer_two_layers_depth_1():
    """Test diagram with two layers at depth 1"""
    connection1 = Connection(shape_1="a", shape_2="b")
    layer1_diagram = Diagram(connections=[connection1])
    layer1 = Layer(name="layer1", diagram=layer1_diagram)

    connection2 = Connection(shape_1="c", shape_2="d")
    layer2_diagram = Diagram(connections=[connection2])
    layer2 = Layer(name="layer2", diagram=layer2_diagram)

    root_diagram = Diagram(layers=[layer1, layer2])
    expected_output = "layers: {\n  layer1: {\n    a -> b\n  }\n  layer2: {\n    c -> d\n  }\n}"
    assert str(root_diagram) == expected_output


def test_d2_layer_nested_layer_depth_2():
    """Test diagram with a layer nested inside another layer (depth 2)"""
    inner_connection = Connection(shape_1="e", shape_2="f")
    inner_diagram = Diagram(connections=[inner_connection])
    inner_layer = Layer(name="inner_layer", diagram=inner_diagram)

    outer_connection = Connection(shape_1="g", shape_2="h")
    outer_diagram = Diagram(connections=[outer_connection], layers=[inner_layer])
    outer_layer = Layer(name="outer_layer", diagram=outer_diagram)

    root_diagram = Diagram(layers=[outer_layer])
    expected_output = (
        "layers: {\n"
        "  outer_layer: {\n"
        "    g -> h\n"
        "    layers: {\n"
        "      inner_layer: {\n"
        "        e -> f\n"
        "      }\n"
        "    }\n"
        "  }\n"
        "}"
    )
    assert str(root_diagram) == expected_output
