from pathlib import Path

import d2


def main() -> None:
    diagram = d2.Diagram(
        vars=d2.Config(layout_engine="tala"),
        shapes=[
            d2.Shape(name="left_box", top=0, left=0),
            d2.Shape(name="right_box", top=120, left=300),
            d2.Shape(
                name="table",
                grid_columns=2,
                vertical_gap=40,
                horizontal_gap=10,
                top=300,
                left=100,
                shapes=[d2.Shape(name=name) for name in "abcd"],
            ),
        ],
    )
    Path("fixed_positions.svg").write_bytes(d2.render(diagram))


if __name__ == "__main__":
    main()
