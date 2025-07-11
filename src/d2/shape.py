from __future__ import annotations

from enum import Enum
from typing import List
from typing import Optional

from d2.connection import Connection
from d2.helpers import add_label_and_properties
from d2.helpers import flatten
from d2.helpers import indent_lines
from d2.style import Style


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

    def lines(self) -> List[str]:
        sep = "|" * self.pipes
        return [f"{sep}{self.formatting}", *self.text.split("\n"), sep]

    def __repr__(self) -> str:
        return "\n".join(self.lines())


class Shape:
    def __init__(
        self,
        name: str,
        # The label of this shape
        label: Optional[str] = None,
        # The actual 2D shape of this shape
        shape: Optional[ShapeType] = None,
        # A list of child shapes (when this shape is a container)
        shapes: Optional[List[Shape]] = None,
        # The style of this shape
        style: Optional[Style] = None,
        # An icon for this shape
        icon: Optional[str] = None,
        # Connections for the child shapes (NOT the connections for this shape)
        connections: Optional[List[Connection]] = None,
        # A shape this is near
        near: Optional[str] = None,
        # A link for a shape (when clicked)
        link: Optional[str] = None,
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
        self.kwargs = kwargs

    def add_shape(self, shape: Shape):
        self.shapes.append(shape)

    def add_connection(self, connection: Connection):
        self.connections.append(connection)

    def lines(self) -> List[str]:
        shapes = flatten([shape.lines() for shape in self.shapes])
        connections = flatten([connection.lines() for connection in self.connections])
        properties = shapes + connections

        if self.shape:
            properties.append(f"shape: {self.shape.value}")

        if self.near:
            properties.append(f"near: {self.near}")

        if self.link:
            properties.append(f"link: {self.link}")

        if self.style:
            properties += self.style.lines()

        if self.icon:
            properties.append(f"icon: {self.icon}")

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

        lines = add_label_and_properties(self.name, self.label, properties)

        return lines

    def __repr__(self) -> str:
        lines = self.lines()
        return "\n".join(lines)
