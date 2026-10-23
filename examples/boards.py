from pathlib import Path

import d2


def main() -> None:
    detail = d2.Diagram(
        shapes=[d2.Shape(name="api"), d2.Shape(name="db")],
        connections=[d2.Connection("api", "db")],
    )
    diagram = d2.Diagram(
        shapes=[d2.Shape(name="system")],
        layers=[d2.Layer(name="detail", diagram=detail)],
        scenarios=[
            d2.Layer(
                name="db_down",
                diagram=d2.Diagram(
                    shapes=[d2.Shape(name="db", style=d2.Style(fill="red"))]
                ),
            )
        ],
        steps=[
            d2.Layer(name="one", diagram=d2.Diagram(shapes=[d2.Shape(name="start")])),
            d2.Layer(name="two", diagram=d2.Diagram(shapes=[d2.Shape(name="finish")])),
        ],
    )
    Path("boards.d2").write_text(str(diagram), encoding="utf-8")


if __name__ == "__main__":
    main()
