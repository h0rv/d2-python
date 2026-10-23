from pathlib import Path

import d2

me = Path(__file__)
svg = me.with_suffix(".svg")
blue, yellow = d2.Style(stroke="#3776ab"), d2.Style(stroke="#ffd43b")
code = d2.Shape(name="py", label=d2.Text(me.read_text(), "python"), style=blue)
image = d2.Shape(name="svg", label="", shape=d2.ShapeType.image, icon=str(svg))
image.width, image.height = 600, 260

source = ""
for _ in range(3):
    text = d2.Text("\n".join([*source.splitlines()[:4], "..."]), "d2")
    diagram = d2.Diagram(
        direction="right",
        shapes=[code, d2.Shape(name="d2", label=text, style=yellow), image],
        connections=[d2.Connection("py", "d2"), d2.Connection("d2", "svg")],
    )
    source = str(diagram)
    svg.write_bytes(d2.render(diagram, layout="elk", pad=20))
