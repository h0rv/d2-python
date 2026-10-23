from pathlib import Path

import d2

script = Path(__file__)
banner = script.with_suffix(".svg")
icon = "https://icons.terrastruct.com/dev%2Fpython.svg"
blue = d2.Style(stroke="#3776ab", stroke_width=3)
yellow = d2.Style(stroke="#ffd43b", stroke_width=3)

source = ""
for _ in range(3):
    code = d2.Text(script.read_text(), "python")
    d2_text = d2.Text("\n".join([*source.splitlines()[:6], "..."]), "d2")
    image = d2.Shape(name="svg", label="this banner", shape=d2.ShapeType.image)
    image.icon, image.width, image.height = str(banner.resolve()), 600, 260
    diagram = d2.Diagram(
        direction="right",
        shapes=[
            d2.Shape(name="python", label=code, icon=icon, style=blue),
            d2.Shape(name="d2", label=d2_text, style=yellow),
            image,
        ],
        connections=[
            d2.Connection("python", "d2", "d2-python", style=blue),
            d2.Connection("d2", "svg", "d2", style=blue),
        ],
    )
    source = str(diagram)
    banner.write_bytes(d2.render(diagram, layout="elk"))
