from __future__ import annotations

from enum import Enum
from typing import Literal

from d2.connection import Connection
from d2.helpers import add_label_and_properties
from d2.helpers import flatten
from d2.helpers import indent_lines
from d2.helpers import quote_label
from d2.helpers import quote_name
from d2.style import Style


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


class Text:
    def __init__(
        self,
        # The actual text body (multiline is fine)
        text: str,
        # The format, eg) md, tex, html, css etc
        formatting: str,
        # The number of pipes to use
        pipes: int = 1,
    ):
        self.text = text
        self.formatting = formatting
        self.pipes = pipes

    def lines(self) -> list[str]:
        sep = "|" * self.pipes
        return [f"{sep}{self.formatting}", *self.text.split("\n"), sep]

    def __repr__(self) -> str:
        return "\n".join(self.lines())


class Shape:
    def __init__(
        self,
        name: str,
        # The label of this shape
        label: str | None = None,
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
        **kwargs: Text,
    ):
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
        self.kwargs = kwargs

    def add_shape(self, shape: Shape):
        self.shapes.append(shape)

    def add_connection(self, connection: Connection):
        self.connections.append(connection)

    def member_lines(self) -> list[str]:
        return []

    def lines(self) -> list[str]:
        shapes = flatten([shape.lines() for shape in self.shapes])
        connections = flatten([connection.lines() for connection in self.connections])
        properties = shapes + connections

        if self.shape:
            properties.append(f"shape: {self.shape.value}")

        properties += self.member_lines()

        if self.near:
            properties.append(f"near: {self.near}")

        if self.link:
            properties.append(f"link: {self.link}")

        if self.style:
            properties += self.style.lines()

        if self.icon:
            properties.append(f"icon: {self.icon}")

        if self.tooltip:
            properties.append(f"tooltip: {quote_label(self.tooltip)}")

        for key, value in (
            ("width", self.width),
            ("height", self.height),
            ("grid-rows", self.grid_rows),
            ("grid-columns", self.grid_columns),
            ("grid-gap", self.grid_gap),
            ("direction", self.direction),
        ):
            if value is not None:
                properties.append(f"{key}: {value}")

        if self.classes:
            names = [quote_name(name) for name in self.classes]
            properties.append(f"class: {names[0] if len(names) == 1 else '[' + '; '.join(names) + ']'}")

        for key, value in self.kwargs.items():
            other_property = value.lines()
            other_property_line_1 = other_property[0]
            other_property_lines_other = other_property[1:-1]
            other_property_line_end = other_property[-1]
            properties += [
                f"{key}: {other_property_line_1}",
                *indent_lines(other_property_lines_other),
                other_property_line_end,
            ]

        lines = add_label_and_properties(quote_name(self.name), self.label, properties)

        return lines

    def __repr__(self) -> str:
        lines = self.lines()
        return "\n".join(lines)
