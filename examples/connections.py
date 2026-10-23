from pathlib import Path

import d2


def main() -> None:
    diagram = d2.Diagram(
        direction="right",
        shapes=[d2.Shape(name=name) for name in ("a", "b", "c", "d", "e")],
        connections=[
            d2.Connection("a", "b", "sends"),
            d2.Connection("b", "a", direction=d2.Direction.FROM),
            d2.Connection("a", "c", "both ways", direction=d2.Direction.BOTH),
            d2.Connection("c", "d", direction=d2.Direction.NONE),
            d2.Connection(
                "d",
                "e",
                "styled",
                style=d2.Style(stroke="red", stroke_dash=3, animated=True),
                target_arrowhead=d2.Arrowhead(d2.ArrowheadShape.DIAMOND, filled=True),
            ),
            d2.Connection(
                "e",
                "a",
                source_arrowhead=d2.Arrowhead(d2.ArrowheadShape.CF_ONE, label="1"),
                target_arrowhead=d2.Arrowhead(d2.ArrowheadShape.CF_MANY, label="n"),
            ),
        ],
    )
    Path("connections.svg").write_bytes(d2.render(diagram))


if __name__ == "__main__":
    main()
