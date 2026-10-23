import sys
from typing import Literal

from d2.helpers import add_label_and_properties, quote_label

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


FillPattern = Literal["dots", "lines", "grain", "none"]
TextTransform = Literal["uppercase", "lowercase", "title", "none"]


def stringify_bool(val: bool) -> str:
    return "true" if val else "false"


def render_value(value: str | float | bool) -> str | None:
    if isinstance(value, bool):
        return stringify_bool(value)
    if isinstance(value, str):
        return quote_label(value) if value != "" else None
    return str(value)


class Style:
    def __init__(
        self,
        stroke: str | None = None,
        stroke_width: int | None = None,
        fill: str | None = None,
        shadow: bool | None = None,
        opacity: float | None = None,
        stroke_dash: int | None = None,
        three_d: bool | None = None,
        font_color: str | None = None,
        border_radius: str | None = None,
        *,
        font: Literal["mono"] | None = None,
        font_size: int | None = None,
        bold: bool | None = None,
        italic: bool | None = None,
        underline: bool | None = None,
        text_transform: TextTransform | None = None,
        animated: bool | None = None,
        double_border: bool | None = None,
        multiple: bool | None = None,
        fill_pattern: FillPattern | None = None,
    ) -> None:
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.fill = fill
        self.shadow = shadow
        self.opacity = opacity
        self.stroke_dash = stroke_dash
        self.three_d = three_d
        self.font_color = font_color
        self.border_radius = border_radius
        self.font = font
        self.font_size = font_size
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.text_transform = text_transform
        self.animated = animated
        self.double_border = double_border
        self.multiple = multiple
        self.fill_pattern = fill_pattern

    def lines(self) -> list[str]:
        entries: list[tuple[str, str | float | bool | None]] = [
            ("stroke", self.stroke),
            ("stroke-width", self.stroke_width),
            ("fill", self.fill),
            ("shadow", self.shadow),
            ("opacity", self.opacity),
            ("stroke-dash", self.stroke_dash),
            ("3d", self.three_d),
            ("font-color", self.font_color),
            ("border-radius", self.border_radius),
            ("font", self.font),
            ("font-size", self.font_size),
            ("bold", self.bold),
            ("italic", self.italic),
            ("underline", self.underline),
            ("text-transform", self.text_transform),
            ("animated", self.animated),
            ("double-border", self.double_border),
            ("multiple", self.multiple),
            ("fill-pattern", self.fill_pattern),
        ]
        styles = [
            f"{key}: {rendered}"
            for key, value in entries
            if value is not None and (rendered := render_value(value)) is not None
        ]

        if len(styles) == 0:
            return []

        return add_label_and_properties("style", None, styles)

    @override
    def __repr__(self) -> str:
        lines = self.lines()
        return "\n".join(lines)
