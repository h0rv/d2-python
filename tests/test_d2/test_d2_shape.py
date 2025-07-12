from d2.connection import Connection
from d2.shape import Shape
from d2.shape import ShapeType
from d2.shape import Text
from d2.style import Style


def test_d2_shape():
    shape = Shape(name="shape_name")
    assert str(shape) == "shape_name"


def test_d2_shape_label():
    shape = Shape(name="shape_name", label="shape_label")
    assert str(shape) == "shape_name: shape_label"


def test_d2_shape_empty_label():
    shape = Shape(name="shape_name", label="")
    assert str(shape) == 'shape_name: ""'


def test_d2_shape_style():
    shape = Shape(name="shape_name", style=Style(fill="red"))
    assert str(shape) == "shape_name: {\n  style: {\n    fill: red\n  }\n}"


def test_d2_shape_container():
    shape = Shape(name="shape_name", label="container_label")
    shape.add_shape(Shape(name="shape_1"))
    shape.add_shape(Shape(name="shape_2"))
    shape.add_connection(Connection(shape_1="shape_1", shape_2="shape_2"))
    assert str(shape) == "\n".join(
        ["shape_name: container_label {", "  shape_1", "  shape_2", "  shape_1 -> shape_2", "}"]
    )


def test_d2_shape_container_style():
    shape = Shape(name="shape_name", label="container_label")
    shape.add_shape(Shape(name="shape_1", style=Style(fill="red")))
    shape.add_shape(Shape(name="shape_2"))
    shape.add_connection(Connection(shape_1="shape_1", shape_2="shape_2"))

    assert str(shape) == "\n".join(
        [
            "shape_name: container_label {",
            "  shape_1: {",
            "    style: {",
            "      fill: red",
            "    }",
            "  }",
            "  shape_2",
            "  shape_1 -> shape_2",
            "}",
        ]
    )


def test_d2_shape_container_in_container_with_shapes():
    shape = Shape(name="shape_name", label="container_label")
    shape.add_shape(
        Shape(
            name="shape_1",
            style=Style(fill="red"),
            shapes=[Shape(name="shape_2", style=Style(fill="blue")), Shape(name="shape_3")],
            connections=[Connection(shape_1="shape_2", shape_2="shape_3")],
        )
    )
    shape.add_shape(Shape(name="shape_4"))

    assert str(shape) == "\n".join(
        [
            "shape_name: container_label {",
            "  shape_1: {",
            "    shape_2: {",
            "      style: {",
            "        fill: blue",
            "      }",
            "    }",
            "    shape_3",
            "    shape_2 -> shape_3",
            "    style: {",
            "      fill: red",
            "    }",
            "  }",
            "  shape_4",
            "}",
        ]
    )


def test_d2_shape_shapes():
    shape_rectangle = Shape(name="shape_name", shape=ShapeType.rectangle)
    shape_rectangle = Shape(name="shape_name", shape=ShapeType.rectangle)
    shape_square = Shape(name="shape_name", shape=ShapeType.square)
    shape_page = Shape(name="shape_name", shape=ShapeType.page)
    shape_parallelogram = Shape(name="shape_name", shape=ShapeType.parallelogram)
    shape_document = Shape(name="shape_name", shape=ShapeType.document)
    shape_cylinder = Shape(name="shape_name", shape=ShapeType.cylinder)
    shape_queue = Shape(name="shape_name", shape=ShapeType.queue)
    shape_package = Shape(name="shape_name", shape=ShapeType.package)
    shape_step = Shape(name="shape_name", shape=ShapeType.step)
    shape_callout = Shape(name="shape_name", shape=ShapeType.callout)
    shape_stored_data = Shape(name="shape_name", shape=ShapeType.stored_data)
    shape_person = Shape(name="shape_name", shape=ShapeType.person)
    shape_diamond = Shape(name="shape_name", shape=ShapeType.diamond)
    shape_oval = Shape(name="shape_name", shape=ShapeType.oval)
    shape_circle = Shape(name="shape_name", shape=ShapeType.circle)
    shape_hexagon = Shape(name="shape_name", shape=ShapeType.hexagon)
    shape_cloud = Shape(name="shape_name", shape=ShapeType.cloud)
    shape_text = Shape(name="shape_name", shape=ShapeType.text)
    shape_code = Shape(name="shape_name", shape=ShapeType.code)
    shape_sql_table = Shape(name="shape_name", shape=ShapeType.sql_table)
    shape_image = Shape(name="shape_name", shape=ShapeType.image)
    shape_classs = Shape(name="shape_name", shape=ShapeType.classs)
    shape_sequence_diagram = Shape(name="shape_name", shape=ShapeType.sequence_diagram)

    assert str(shape_rectangle) == "shape_name: {\n  shape: rectangle\n}"
    assert str(shape_rectangle) == "shape_name: {\n  shape: rectangle\n}"
    assert str(shape_square) == "shape_name: {\n  shape: square\n}"
    assert str(shape_page) == "shape_name: {\n  shape: page\n}"
    assert str(shape_parallelogram) == "shape_name: {\n  shape: parallelogram\n}"
    assert str(shape_document) == "shape_name: {\n  shape: document\n}"
    assert str(shape_cylinder) == "shape_name: {\n  shape: cylinder\n}"
    assert str(shape_queue) == "shape_name: {\n  shape: queue\n}"
    assert str(shape_package) == "shape_name: {\n  shape: package\n}"
    assert str(shape_step) == "shape_name: {\n  shape: step\n}"
    assert str(shape_callout) == "shape_name: {\n  shape: callout\n}"
    assert str(shape_stored_data) == "shape_name: {\n  shape: stored_data\n}"
    assert str(shape_person) == "shape_name: {\n  shape: person\n}"
    assert str(shape_diamond) == "shape_name: {\n  shape: diamond\n}"
    assert str(shape_oval) == "shape_name: {\n  shape: oval\n}"
    assert str(shape_circle) == "shape_name: {\n  shape: circle\n}"
    assert str(shape_hexagon) == "shape_name: {\n  shape: hexagon\n}"
    assert str(shape_cloud) == "shape_name: {\n  shape: cloud\n}"
    assert str(shape_text) == "shape_name: {\n  shape: text\n}"
    assert str(shape_code) == "shape_name: {\n  shape: code\n}"
    assert str(shape_sql_table) == "shape_name: {\n  shape: sql_table\n}"
    assert str(shape_image) == "shape_name: {\n  shape: image\n}"
    assert str(shape_classs) == "shape_name: {\n  shape: class\n}"
    assert str(shape_sequence_diagram) == "shape_name: {\n  shape: sequence_diagram\n}"


def test_d2_shape_icon():
    shape = Shape(name="shape_name", icon="https://icons.terrastruct.com/essentials%2F117-database.svg")
    assert str(shape) == "shape_name: {\n  icon: https://icons.terrastruct.com/essentials%2F117-database.svg\n}"


def test_d2_shape_near():
    shape = Shape(name="shape_name", near="some_other_shape")
    assert str(shape) == "shape_name: {\n  near: some_other_shape\n}"


def test_d2_shape_link():
    shape = Shape(name="shape_name", link="https://github.com/MrBlenny/py-d2")
    assert str(shape) == "shape_name: {\n  link: https://github.com/MrBlenny/py-d2\n}"


def test_d2_shape_other_properties():
    text = "Some text"
    shape = Shape(name="shape_name", thing=Text(text=text, formatting="md"))
    assert str(shape) == "\n".join(["shape_name: {", "  thing: |md", "    Some text", "  |", "}"])


def test_d2_shape_other_properties_multi_line():
    text = "\n".join(["multiline text", "like this", "works too"])
    shape = Shape(name="shape_name", thing=Text(text=text, formatting="md"))
    assert str(shape) == "\n".join(
        ["shape_name: {", "  thing: |md", "    multiline text", "    like this", "    works too", "  |", "}"]
    )


def test_d2_shape_other_properties_can_be_anything():
    text = "\n".join(["multiline text", "like this", "works too"])
    shape = Shape(
        name="shape_name",
        description=Text(text=text, formatting="md"),
        other_thing=Text(text=text, formatting="md"),
    )
    assert str(shape) == "\n".join(
        [
            "shape_name: {",
            "  description: |md",
            "    multiline text",
            "    like this",
            "    works too",
            "  |",
            "  other_thing: |md",
            "    multiline text",
            "    like this",
            "    works too",
            "  |",
            "}",
        ]
    )


def test_d2_shape_text_can_specify_pipe_count():
    text = "const iLoveTypescript = 1 || true;\nconst really = () => iLoveTypescript"
    shape = Shape(name="shape_name", code=Text(text=text, formatting="ts", pipes=3))
    assert str(shape) == "\n".join(
        [
            "shape_name: {",
            "  code: |||ts",
            "    const iLoveTypescript = 1 || true;",
            "    const really = () => iLoveTypescript",
            "  |||",
            "}",
        ]
    )
