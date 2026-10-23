from pathlib import Path

import d2


def main() -> None:
    diagram = d2.Diagram(
        shapes=[
            d2.Shape(
                name="board",
                grid_columns=3,
                grid_gap=10,
                shapes=[d2.Shape(name=f"cell{i}") for i in range(1, 7)],
            ),
        ],
    )
    Path("grids.svg").write_bytes(d2.render(diagram))


if __name__ == "__main__":
    main()
