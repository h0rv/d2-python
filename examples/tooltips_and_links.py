from pathlib import Path

import d2


def main() -> None:
    diagram = d2.Diagram(
        shapes=[
            d2.Shape(name="api", tooltip="Public REST API"),
            d2.Shape(name="docs", link="https://d2lang.com"),
            d2.Shape(name="db", shape=d2.ShapeType.cylinder),
        ],
        connections=[
            d2.Connection("api", "db", tooltip="Reads and writes over TCP"),
        ],
    )
    Path("tooltips_and_links.svg").write_bytes(d2.render(diagram))


if __name__ == "__main__":
    main()
