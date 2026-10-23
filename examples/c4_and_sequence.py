from pathlib import Path

import d2


def main() -> None:
    c4 = d2.Diagram(
        shapes=[
            d2.Shape(name="customer", label="Customer", shape=d2.ShapeType.c4_person),
            d2.Shape(name="shop", label="Web shop"),
        ],
        connections=[d2.Connection("customer", "shop", "buys")],
    )
    Path("c4.svg").write_bytes(d2.render(c4))

    sequence = d2.Diagram(
        shapes=[
            d2.Shape(
                name="checkout",
                shape=d2.ShapeType.sequence_diagram,
                shapes=[d2.Shape(name="user"), d2.Shape(name="shop"), d2.Shape("bank")],
                connections=[
                    d2.Connection("user", "shop", "pay"),
                    d2.Connection("shop", "bank", "charge"),
                    d2.Connection("bank", "shop", "ok", style=d2.Style(stroke_dash=3)),
                ],
            )
        ]
    )
    Path("sequence.svg").write_bytes(d2.render(sequence))


if __name__ == "__main__":
    main()
