from pathlib import Path

import d2


def main() -> None:
    diagram = d2.Diagram(
        classes={
            "service": d2.Style(fill="lightblue", stroke="blue", border_radius="8"),
            "store": d2.Style(fill="lightgreen", stroke="green"),
        },
        shapes=[
            d2.Shape(name="api", classes=["service"]),
            d2.Shape(name="worker", classes=["service"]),
            d2.Shape(name="db", shape=d2.ShapeType.cylinder, classes=["store"]),
        ],
        connections=[d2.Connection("api", "db"), d2.Connection("worker", "db")],
    )
    Path("classes.svg").write_bytes(d2.render(diagram))


if __name__ == "__main__":
    main()
