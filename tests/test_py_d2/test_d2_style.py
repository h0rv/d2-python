from d2.style import Style


def test_d2_style():
    style = Style()
    assert str(style) == ""


def test_d2_style_fill():
    style = Style(fill="red")
    assert str(style) == "style: {\n  fill: red\n}"


def test_d2_style_stroke():
    style = Style(stroke="red")
    assert str(style) == "style: {\n  stroke: red\n}"


def test_d2_style_stroke_width():
    style = Style(stroke_width=2)
    assert str(style) == "style: {\n  stroke-width: 2\n}"


def test_d2_style_shadow():
    style = Style(shadow=True)
    assert str(style) == "style: {\n  shadow: true\n}"


def test_d2_style_opacity():
    style = Style(opacity=0.5)
    assert str(style) == "style: {\n  opacity: 0.5\n}"


def test_d2_style_stroke_dash():
    style = Style(stroke_dash=2)
    assert str(style) == "style: {\n  stroke-dash: 2\n}"


def test_d2_style_three_d():
    style = Style(three_d=True)
    assert str(style) == "style: {\n  3d: true\n}"


def test_d2_style_all():
    style = Style(
        stroke="red",
        stroke_width=2,
        fill="red",
        shadow=True,
        opacity=0.5,
        stroke_dash=2,
        three_d=True,
    )
    assert str(style) == "\n".join(
        [
            "style: {",
            "  stroke: red",
            "  stroke-width: 2",
            "  fill: red",
            "  shadow: true",
            "  opacity: 0.5",
            "  stroke-dash: 2",
            "  3d: true",
            "}",
        ]
    )
