from d2.class_shape import ClassField, ClassMethod, ClassShape


def test_d2_class_shape_empty() -> None:
    assert str(ClassShape("Animal")) == "Animal: {\n  shape: class\n}"


def test_d2_class_shape_fields_and_methods() -> None:
    shape = ClassShape(
        "Animal",
        fields=[
            ClassField("name", "string", "+"),
            ClassField("age", "int", "-"),
            ClassField("tags", "[]string", "#"),
            ClassField("plain"),
        ],
        methods=[
            ClassMethod("eat", "a uint64", "(x, y int)", "+"),
            ClassMethod("sleep", visibility="-"),
        ],
    )
    expected_lines = [
        "Animal: {",
        "  shape: class",
        '  +name: "string"',
        '  -age: "int"',
        '  "#tags": "[]string"',
        "  plain",
        '  +eat(a uint64): "(x, y int)"',
        "  -sleep()",
        "}",
    ]
    assert str(shape) == "\n".join(expected_lines)


def test_d2_class_shape_add_members_and_label() -> None:
    shape = ClassShape("Animal", label="An animal")
    shape.add_field(ClassField("name", "string"))
    shape.add_method(ClassMethod("run"))
    expected_lines = [
        "Animal: An animal {",
        "  shape: class",
        '  name: "string"',
        "  run()",
        "}",
    ]
    assert str(shape) == "\n".join(expected_lines)
