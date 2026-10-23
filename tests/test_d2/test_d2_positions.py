import d2
from d2.sql_table import SQLTable


def test_shape__label_and_icon_near() -> None:
    shape = d2.Shape(
        name="a",
        icon="https://x.test/i.svg",
        label_near="outside-top-left",
        icon_near="border-top-center",
    )

    assert str(shape).split("\n") == [
        "a: {",
        "  icon: https://x.test/i.svg",
        "  label.near: outside-top-left",
        "  icon.near: border-top-center",
        "}",
    ]


def test_shape__top_left_and_gaps() -> None:
    shape = d2.Shape(name="a", top=10, left=0, vertical_gap=4, horizontal_gap=6)

    assert str(shape).split("\n") == [
        "a: {",
        "  vertical-gap: 4",
        "  horizontal-gap: 6",
        "  top: 10",
        "  left: 0",
        "}",
    ]


def test_shape__c4_person() -> None:
    shape = d2.Shape(name="user", shape=d2.ShapeType.c4_person)

    assert "shape: c4-person" in str(shape)


def test_shape__defaults_add_nothing() -> None:
    assert str(d2.Shape(name="a")) == "a"


def test_shape__text_label() -> None:
    shape = d2.Shape(name="a", label=d2.Text("# Title", "md"), width=100)

    assert str(shape).split("\n") == [
        "a: {",
        "  label: |md",
        "    # Title",
        "  |",
        "  width: 100",
        "}",
    ]


def test_connection__text_label() -> None:
    connection = d2.Connection("a", "b", d2.Text("**calls**", "md"))

    assert str(connection).split("\n") == [
        "a -> b: {",
        "  label: |md",
        "    **calls**",
        "  |",
        "}",
    ]


def test_connection__icon_link_and_classes() -> None:
    connection = d2.Connection(
        "a",
        "b",
        icon="https://x.test/i.svg",
        link="https://x.test",
        classes=["hot", "wide"],
    )

    assert str(connection).split("\n") == [
        "a -> b: {",
        "  icon: https://x.test/i.svg",
        "  link: https://x.test",
        "  class: [hot; wide]",
        "}",
    ]


def test_connection__equality_includes_new_fields() -> None:
    assert d2.Connection("a", "b", icon="x") != d2.Connection("a", "b")
    assert d2.Connection("a", "b", link="x") == d2.Connection("a", "b", link="x")


def test_layer__label_is_the_board_title() -> None:
    diagram = d2.Diagram(
        scenarios=[
            d2.Layer("slow", d2.Diagram(shapes=[d2.Shape(name="a")]), label="Slow path")
        ]
    )

    assert str(diagram) == "scenarios: {\n  slow: Slow path {\n    a\n  }\n}"


def test_sql_table__text_label() -> None:
    table = SQLTable("t", {"id": "int"}, label=None)
    table.label = d2.Text("# t", "md")

    assert str(table).split("\n")[1] == "  label: |md"
