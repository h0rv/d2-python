from d2.class_shape import ClassField
from d2.class_shape import ClassMethod
from d2.class_shape import ClassShape


def test_d2_class_shape_empty():
    assert str(ClassShape("Animal")) == "Animal: {\n  shape: class\n}"


def test_d2_class_shape_fields_and_methods():
    shape = ClassShape(
        "Animal",
        fields=[
            ClassField("name", "string", "+"),
            ClassField("age", "int", "-"),
            ClassField("tags", "[]string", "#"),
            ClassField("plain"),
        ],
        methods=[ClassMethod("eat", "a uint64", "(x, y int)", "+"), ClassMethod("sleep", visibility="-")],
    )
    assert str(shape) == "\n".join(
        [
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
    )


def test_d2_class_shape_add_members_and_label():
    shape = ClassShape("Animal", label="An animal")
    shape.add_field(ClassField("name", "string"))
    shape.add_method(ClassMethod("run"))
    assert str(shape) == "\n".join(["Animal: An animal {", "  shape: class", '  name: "string"', "  run()", "}"])
