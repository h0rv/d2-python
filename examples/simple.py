from pathlib import Path

from d2.connection import Connection
from d2.diagram import Diagram
from d2.shape import Shape
from d2.style import Style


def main() -> None:
    shapes = [
        Shape(name="shape_name1", style=Style(fill="red")),
        Shape(name="shape_name2", style=Style(fill="blue")),
    ]
    connections = [Connection(shape_1="shape_name1", shape_2="shape_name2")]

    diagram = Diagram(shapes=shapes, connections=connections)

    Path("graph.d2").write_text(str(diagram), encoding="utf-8")


if __name__ == "__main__":
    main()
