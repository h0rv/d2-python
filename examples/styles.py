from pathlib import Path

import d2


def main() -> None:
    diagram = d2.Diagram(
        shapes=[
            d2.Shape(
                name="colors",
                style=d2.Style(fill="gold", stroke="brown", stroke_width=3),
            ),
            d2.Shape(
                name="text",
                style=d2.Style(
                    font="mono",
                    font_size=24,
                    font_color="white",
                    bold=True,
                    fill="navy",
                ),
            ),
            d2.Shape(name="faded", style=d2.Style(fill="red", opacity=0.3)),
            d2.Shape(name="block", style=d2.Style(three_d=True)),
            d2.Shape(name="shadowed", style=d2.Style(shadow=True)),
            d2.Shape(name="rounded", style=d2.Style(border_radius="12")),
        ],
    )
    Path("styles.svg").write_bytes(d2.render(diagram))


if __name__ == "__main__":
    main()
