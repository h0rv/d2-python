from d2.connection import Connection
from d2.diagram import Diagram
from d2.shape import Shape
from d2.style import Style


def example():
    print("Contructing a simple graph...")
    shapes = [
        Shape(name="shape_name1", style=Style(fill="red")),
        Shape(name="shape_name2", style=Style(fill="blue")),
    ]
    connections = [Connection(shape_1="shape_name1", shape_2="shape_name2")]

    diagram = Diagram(shapes=shapes, connections=connections)

    print("Writing graph to file...")
    with open("graph.d2", "w", encoding="utf-8") as f:
        f.write(str(diagram))
        print("Done! (graph.d2)")


if __name__ == "__main__":
    example()
