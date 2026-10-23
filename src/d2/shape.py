from __future__ import annotations

import sys
from enum import Enum
from typing import TYPE_CHECKING, Literal

from d2.helpers import (
    add_label_and_properties,
    flatten,
    non_empty,
    quote_label,
    quote_name,
)
from d2.text import Text

if TYPE_CHECKING:
    from d2.connection import Connection
    from d2.style import Style

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


LayoutDirection = Literal["up", "down", "left", "right"]


class ShapeType(Enum):
    rectangle = "rectangle"
    square = "square"
    page = "page"
    parallelogram = "parallelogram"
    document = "document"
    cylinder = "cylinder"
    queue = "queue"
    package = "package"
    step = "step"
    callout = "callout"
    stored_data = "stored_data"
    person = "person"
    diamond = "diamond"
    oval = "oval"
    circle = "circle"
    hexagon = "hexagon"
    cloud = "cloud"
    text = "text"
    code = "code"
    sql_table = "sql_table"
    image = "image"
    classs = "class"
    sequence_diagram = "sequence_diagram"
    c4_person = "c4-person"


LabelPosition = Literal[
    "outside-top-left",
    "outside-top-center",
    "outside-top-right",
    "outside-left-top",
    "outside-left-center",
    "outside-left-bottom",
    "outside-right-top",
    "outside-right-center",
    "outside-right-bottom",
    "outside-bottom-left",
    "outside-bottom-center",
    "outside-bottom-right",
    "border-top-left",
    "border-top-center",
    "border-top-right",
    "border-left-top",
    "border-left-center",
    "border-left-bottom",
    "border-right-top",
    "border-right-center",
    "border-right-bottom",
    "border-bottom-left",
    "border-bottom-center",
    "border-bottom-right",
    "inside-top-left",
    "inside-top-center",
    "inside-top-right",
    "inside-middle-left",
    "inside-middle-center",
    "inside-middle-right",
    "inside-bottom-left",
    "inside-bottom-center",
    "inside-bottom-right",
]


NearPosition = Literal[
    "top-left",
    "top-center",
    "top-right",
    "center-left",
    "center-right",
    "bottom-left",
    "bottom-center",
    "bottom-right",
]


def label_parts(label: str | Text | None) -> tuple[str | None, list[str]]:
    if isinstance(label, Text):
        return None, label.block_lines("label")
    return label, []


class Shape:
    def __init__(
        self,
        name: str,
        # The label of this shape
        label: str | Text | None = None,
        # The actual 2D shape of this shape
        shape: ShapeType | None = None,
        # A list of child shapes (when this shape is a container)
        shapes: list[Shape] | None = None,
        # The style of this shape
        style: Style | None = None,
        # An icon for this shape
        icon: str | None = None,
        # Connections for the child shapes (NOT the connections for this shape)
        connections: list[Connection] | None = None,
        # A shape this is near
        near: str | None = None,
        # A link for a shape (when clicked)
        link: str | None = None,
        *,
        tooltip: str | None = None,
        width: int | None = None,
        height: int | None = None,
        grid_rows: int | None = None,
        grid_columns: int | None = None,
        grid_gap: int | None = None,
        direction: LayoutDirection | None = None,
        classes: list[str] | None = None,
        label_near: LabelPosition | None = None,
        icon_near: LabelPosition | None = None,
        top: int | None = None,
        left: int | None = None,
        vertical_gap: int | None = None,
        horizontal_gap: int | None = None,
        **kwargs: Text,
    ) -> None:
        self.name = name
        self.label = label
        self.shape = shape
        self.shapes = shapes or []
        self.style = style
        self.icon = icon
        self.connections = connections or []
        self.near = near
        self.link = link
        self.tooltip = tooltip
        self.width = width
        self.height = height
        self.grid_rows = grid_rows
        self.grid_columns = grid_columns
        self.grid_gap = grid_gap
        self.direction = direction
        self.classes = classes or []
        self.label_near = label_near
        self.icon_near = icon_near
        self.top = top
        self.left = left
        self.vertical_gap = vertical_gap
        self.horizontal_gap = horizontal_gap
        self.kwargs = kwargs

    def add_shape(self, shape: Shape) -> None:
        self.shapes.append(shape)

    def add_connection(self, connection: Connection) -> None:
        self.connections.append(connection)

    def member_lines(self) -> list[str]:
        return []

    def attribute_lines(self) -> list[str]:
        properties: list[str] = []
        for key, value in (
            ("width", self.width),
            ("height", self.height),
            ("grid-rows", self.grid_rows),
            ("grid-columns", self.grid_columns),
            ("grid-gap", self.grid_gap),
            ("direction", self.direction),
            ("vertical-gap", self.vertical_gap),
            ("horizontal-gap", self.horizontal_gap),
            ("top", self.top),
            ("left", self.left),
            ("label.near", self.label_near),
            ("icon.near", self.icon_near),
        ):
            if value is not None:
                properties.append(f"{key}: {value}")

        if self.classes:
            names = [quote_name(name) for name in self.classes]
            joined = names[0] if len(names) == 1 else f"[{'; '.join(names)}]"
            properties.append(f"class: {joined}")

        return properties

    def lines(self) -> list[str]:
        shapes = flatten([shape.lines() for shape in self.shapes])
        connections = flatten([connection.lines() for connection in self.connections])
        properties = shapes + connections

        if self.shape is not None:
            properties.append(f"shape: {self.shape.value}")

        properties += self.member_lines()

        if (near := non_empty(self.near)) is not None:
            properties.append(f"near: {near}")

        if (link := non_empty(self.link)) is not None:
            properties.append(f"link: {link}")

        if self.style is not None:
            properties += self.style.lines()

        if (icon := non_empty(self.icon)) is not None:
            properties.append(f"icon: {icon}")

        if (tooltip := non_empty(self.tooltip)) is not None:
            properties.append(f"tooltip: {quote_label(tooltip)}")

        properties += self.attribute_lines()

        for key, value in self.kwargs.items():
            properties += value.block_lines(key)

        label, label_lines = label_parts(self.label)
        return add_label_and_properties(
            quote_name(self.name), label, [*label_lines, *properties]
        )

    @override
    def __repr__(self) -> str:
        lines = self.lines()
        return "\n".join(lines)
