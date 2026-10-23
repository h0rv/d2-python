from pathlib import Path

import d2

ICON = "https://icons.terrastruct.com/essentials%2F112-server.svg"


def main() -> None:
    diagram = d2.Diagram(
        shapes=[
            d2.Shape(
                name="api",
                label=d2.Text("# API\n\nPublic **REST** endpoint", "md"),
                width=260,
                height=160,
                icon=ICON,
                icon_near="border-top-left",
            ),
            d2.Shape(
                name="db",
                label="Database",
                shape=d2.ShapeType.cylinder,
                label_near="outside-bottom-center",
            ),
        ],
        connections=[
            d2.Connection(
                "api",
                "db",
                d2.Text("`SELECT *`\nover **TLS**", "md"),
                icon=ICON,
                link="https://d2lang.com",
            )
        ],
    )
    Path("labels_and_positions.svg").write_bytes(d2.render(diagram))


if __name__ == "__main__":
    main()
