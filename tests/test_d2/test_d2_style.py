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


def test_d2_style_font_color():
    style = Style(font_color="red")
    assert str(style) == "style: {\n  font-color: red\n}"

def test_d2_style_font_color_hex():
    style = Style(font_color='"#274e13"')
    assert str(style) == 'style: {\n  font-color: "#274e13"\n}'

def test_d2_style_border_radius():
    style = Style(border_radius="999")
    assert str(style) == "style: {\n  border-radius: 999\n}"


def test_d2_style_all():
    style = Style(
        stroke="red",
        stroke_width=2,
        fill="red",
        shadow=True,
        opacity=0.5,
        stroke_dash=2,
        three_d=True,
        font_color='"#274e13"',
        border_radius='999',
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
            "  font-color: \"#274e13\"",
            "  border-radius: 999",
            "}",
        ]
    )
