from d2.style import Style


def test_d2_style() -> None:
    style = Style()
    assert str(style) == ""


def test_d2_style_fill() -> None:
    style = Style(fill="red")
    assert str(style) == "style: {\n  fill: red\n}"


def test_d2_style_stroke() -> None:
    style = Style(stroke="red")
    assert str(style) == "style: {\n  stroke: red\n}"


def test_d2_style_stroke_width() -> None:
    style = Style(stroke_width=2)
    assert str(style) == "style: {\n  stroke-width: 2\n}"


def test_d2_style_shadow() -> None:
    style = Style(shadow=True)
    assert str(style) == "style: {\n  shadow: true\n}"


def test_d2_style_opacity() -> None:
    style = Style(opacity=0.5)
    assert str(style) == "style: {\n  opacity: 0.5\n}"


def test_d2_style_stroke_dash() -> None:
    style = Style(stroke_dash=2)
    assert str(style) == "style: {\n  stroke-dash: 2\n}"


def test_d2_style_three_d() -> None:
    style = Style(three_d=True)
    assert str(style) == "style: {\n  3d: true\n}"


def test_d2_style_font_color() -> None:
    style = Style(font_color="red")
    assert str(style) == "style: {\n  font-color: red\n}"


def test_d2_style_font_color_hex() -> None:
    style = Style(font_color='"#274e13"')
    assert str(style) == 'style: {\n  font-color: "#274e13"\n}'


def test_d2_style_border_radius() -> None:
    style = Style(border_radius="999")
    assert str(style) == "style: {\n  border-radius: 999\n}"


def test_d2_style_all() -> None:
    style = Style(
        stroke="red",
        stroke_width=2,
        fill="red",
        shadow=True,
        opacity=0.5,
        stroke_dash=2,
        three_d=True,
        font_color='"#274e13"',
        border_radius="999",
    )
    expected_lines = [
        "style: {",
        "  stroke: red",
        "  stroke-width: 2",
        "  fill: red",
        "  shadow: true",
        "  opacity: 0.5",
        "  stroke-dash: 2",
        "  3d: true",
        '  font-color: "#274e13"',
        "  border-radius: 999",
        "}",
    ]
    assert str(style) == "\n".join(expected_lines)


def test_d2_style_falsy_values_are_emitted() -> None:
    style = Style(stroke_width=0, shadow=False, opacity=0, stroke_dash=0, three_d=False)
    expected_lines = [
        "style: {",
        "  stroke-width: 0",
        "  shadow: false",
        "  opacity: 0",
        "  stroke-dash: 0",
        "  3d: false",
        "}",
    ]
    assert str(style) == "\n".join(expected_lines)


def test_d2_style_unset_values_are_omitted() -> None:
    assert str(Style(shadow=None, opacity=None, stroke_width=None)) == ""


def test_d2_style_text_options() -> None:
    style = Style(
        font="mono",
        font_size=20,
        bold=True,
        italic=False,
        underline=True,
        text_transform="uppercase",
    )
    expected_lines = [
        "style: {",
        "  font: mono",
        "  font-size: 20",
        "  bold: true",
        "  italic: false",
        "  underline: true",
        "  text-transform: uppercase",
        "}",
    ]
    assert str(style) == "\n".join(expected_lines)


def test_d2_style_shape_options() -> None:
    style = Style(
        animated=True, double_border=True, multiple=False, fill_pattern="dots"
    )
    expected_lines = [
        "style: {",
        "  animated: true",
        "  double-border: true",
        "  multiple: false",
        "  fill-pattern: dots",
        "}",
    ]
    assert str(style) == "\n".join(expected_lines)
