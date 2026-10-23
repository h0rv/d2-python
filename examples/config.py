from pathlib import Path

import d2


def main() -> None:
    diagram = d2.Diagram(
        direction="right",
        vars=d2.Config(layout_engine="elk", theme_id=4, sketch=True, pad=40),
        shapes=[d2.Shape(name="a"), d2.Shape(name="b"), d2.Shape(name="c")],
        connections=[d2.Connection("a", "b"), d2.Connection("b", "c")],
    )
    Path("config.svg").write_bytes(d2.render(diagram))


if __name__ == "__main__":
    main()
