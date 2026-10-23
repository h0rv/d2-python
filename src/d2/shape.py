from __future__ import annotations

import sys
from enum import Enum
from typing import TYPE_CHECKING, Literal

from d2._limits import bounded
from d2._syntax import (
    BlockField,
    Field,
    Key,
    Keyword,
    Label,
    Statement,
    Text,
    Url,
    Value,
    class_references,
    emit,
    properties,
    split_label,
)

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
    "top-left",
    "top-center",
    "top-right",
    "center-left",
    "center-center",
    "center-right",
    "bottom-left",
    "bottom-center",
    "bottom-right",
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
        self.icon = icon or None
        self.connections = connections or []
        self.near = near or None
        self.link = link or None
        self.tooltip = tooltip or None
        self.width = width
        self.height = height
        self.grid_rows = bounded("grid_rows", grid_rows, 1)
        self.grid_columns = bounded("grid_columns", grid_columns, 1)
        self.grid_gap = bounded("grid_gap", grid_gap, 0)
        self.direction = direction
        self.classes = classes or []
        self.label_near = label_near
        self.icon_near = icon_near
        self.top = bounded("top", top, 0)
        self.left = bounded("left", left, 0)
        self.vertical_gap = bounded("vertical_gap", vertical_gap, 0)
        self.horizontal_gap = bounded("horizontal_gap", horizontal_gap, 0)
        self.kwargs = kwargs

    def add_shape(self, shape: Shape) -> None:
        self.shapes.append(shape)

    def add_connection(self, connection: Connection) -> None:
        self.connections.append(connection)

    def members(self) -> tuple[Statement, ...]:
        return ()

    def attributes(self) -> tuple[Statement, ...]:
        entries: tuple[tuple[str, Value | None], ...] = (
            ("width", self.width),
            ("height", self.height),
            ("grid-rows", self.grid_rows),
            ("grid-columns", self.grid_columns),
            ("grid-gap", self.grid_gap),
            ("direction", Keyword.of(self.direction)),
            ("vertical-gap", self.vertical_gap),
            ("horizontal-gap", self.horizontal_gap),
            ("top", self.top),
            ("left", self.left),
            ("label.near", Keyword.of(self.label_near)),
            ("icon.near", Keyword.of(self.icon_near)),
        )
        return (*properties(entries), *class_references(self.classes))

    def body(self) -> tuple[Statement, ...]:
        return (
            *(s for shape in self.shapes for s in shape.statements()),
            *(s for connection in self.connections for s in connection.statements()),
            *properties((("shape", self.shape),)),
            *self.members(),
            *properties((("near", Keyword.of(self.near)), ("link", Url.of(self.link)))),
            *(self.style.statements() if self.style is not None else ()),
            *properties(
                (("icon", Url.of(self.icon)), ("tooltip", Label.of(self.tooltip)))
            ),
            *self.attributes(),
            *(BlockField(Keyword(key), text) for key, text in self.kwargs.items()),
        )

    def statements(self) -> tuple[Field, ...]:
        label, label_block = split_label(self.label)
        return (Field(Key(self.name), label, (*label_block, *self.body())),)

    def lines(self) -> list[str]:
        return emit(self.statements())

    @override
    def __repr__(self) -> str:
        return "\n".join(self.lines())
