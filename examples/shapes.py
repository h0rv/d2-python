from pathlib import Path

import d2

ICON = "https://icons.terrastruct.com/essentials%2F112-server.svg"


def main() -> None:
    diagram = d2.Diagram(
        direction="right",
        shapes=[
            d2.Shape(name="db", label="Database", shape=d2.ShapeType.cylinder),
            d2.Shape(name="jobs", shape=d2.ShapeType.queue),
            d2.Shape(name="user", shape=d2.ShapeType.person),
            d2.Shape(name="decision", shape=d2.ShapeType.diamond),
            d2.Shape(name="internet", shape=d2.ShapeType.cloud),
            d2.Shape(name="server", icon=ICON),
        ],
    )
    Path("shapes.svg").write_bytes(d2.render(diagram))


if __name__ == "__main__":
    main()
