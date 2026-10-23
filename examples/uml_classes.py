from pathlib import Path

import d2


def main() -> None:
    animal = d2.ClassShape(
        "Animal",
        fields=[d2.ClassField("name", "string", "+")],
        methods=[d2.ClassMethod("eat", "food string", "bool", "+")],
    )
    dog = d2.ClassShape(
        "Dog",
        fields=[d2.ClassField("breed", "string", "-")],
        methods=[d2.ClassMethod("bark", visibility="+")],
    )
    diagram = d2.Diagram(
        shapes=[animal, dog],
        connections=[
            d2.Connection(
                "Dog",
                "Animal",
                target_arrowhead=d2.Arrowhead(d2.ArrowheadShape.TRIANGLE),
            )
        ],
    )
    Path("uml_classes.svg").write_bytes(d2.render(diagram))


if __name__ == "__main__":
    main()
