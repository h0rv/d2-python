from __future__ import annotations

import sys
from typing import Literal

from d2._limits import bounded
from d2._syntax import Color, Field, Keyword, Value, emit, properties

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

FillPattern = Literal["dots", "lines", "grain", "paper", "none"]
TextTransform = Literal["uppercase", "lowercase", "capitalize", "none"]


class Style:
    def __init__(
        self,
        stroke: str | Color | None = None,
        stroke_width: int | None = None,
        fill: str | Color | None = None,
        shadow: bool | None = None,
        opacity: float | None = None,
        stroke_dash: int | None = None,
        three_d: bool | None = None,
        font_color: str | Color | None = None,
        border_radius: int | str | None = None,
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
        self.stroke = Color.of(stroke)
        self.stroke_width = bounded("stroke_width", stroke_width, 0, 15)
        self.fill = Color.of(fill)
        self.shadow = shadow
        self.opacity = bounded("opacity", opacity, 0, 1)
        self.stroke_dash = bounded("stroke_dash", stroke_dash, 0, 10)
        self.three_d = three_d
        self.font_color = Color.of(font_color)
        self.border_radius = bounded(
            "border_radius",
            None if border_radius in (None, "") else int(border_radius),
            0,
        )
        self.font = font
        self.font_size = bounded("font_size", font_size, 8, 100)
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.text_transform = text_transform
        self.animated = animated
        self.double_border = double_border
        self.multiple = multiple
        self.fill_pattern = fill_pattern

    def statements(self) -> tuple[Field, ...]:
        entries: tuple[tuple[str, Value | None], ...] = (
            ("stroke", self.stroke),
            ("stroke-width", self.stroke_width),
            ("fill", self.fill),
            ("shadow", self.shadow),
            ("opacity", self.opacity),
            ("stroke-dash", self.stroke_dash),
            ("3d", self.three_d),
            ("font-color", self.font_color),
            ("border-radius", self.border_radius),
            ("font", Keyword.of(self.font)),
            ("font-size", self.font_size),
            ("bold", self.bold),
            ("italic", self.italic),
            ("underline", self.underline),
            ("text-transform", Keyword.of(self.text_transform)),
            ("animated", self.animated),
            ("double-border", self.double_border),
            ("multiple", self.multiple),
            ("fill-pattern", Keyword.of(self.fill_pattern)),
        )
        styles = properties(entries)
        return (Field(Keyword("style"), body=styles),) if styles else ()

    def lines(self) -> list[str]:
        return emit(self.statements())

    @override
    def __repr__(self) -> str:
        return "\n".join(self.lines())
