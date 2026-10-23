from pathlib import Path

import d2


def main() -> None:
    diagram = d2.Diagram(
        variables={"env": "production", "primary": "#dbeafe"},
        shapes=[
            d2.Shape(
                name="api", label="API (${env})", style=d2.Style(fill="${primary}")
            ),
            d2.Shape(
                name="db",
                label="Database",
                style=d2.Style(fill="linear-gradient(#f69d3c, #3f87a6)"),
            ),
        ],
        connections=[d2.Connection("api", "db", style=d2.Style(stroke="red"))],
        legend=d2.Legend(
            label="Key",
            shapes=[d2.Shape(name="gradient", label="Storage")],
            connections=[
                d2.Connection("a", "b", "critical", style=d2.Style(stroke="red"))
            ],
        ),
        scenarios=[
            d2.Layer(
                "db_down",
                d2.Diagram(shapes=[d2.Shape(name="db", style=d2.Style(fill="red"))]),
                label="Database down",
            )
        ],
    )
    Path("variables_and_legend.svg").write_bytes(d2.render(diagram))


if __name__ == "__main__":
    main()
