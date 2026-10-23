from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from d2.connection import Connection
from d2.helpers import add_label_and_properties
from d2.helpers import indent
from d2.helpers import indent_lines
from d2.helpers import quote_name
from d2.shape import LayoutDirection
from d2.shape import Shape
from d2.style import Style


@dataclass(frozen=True, kw_only=True)
class Config:
    layout_engine: Literal["dagre", "elk", "tala"] | None = None
    theme_id: int | None = None
    dark_theme_id: int | None = None
    pad: int | None = None
    sketch: bool | None = None
    center: bool | None = None

    def lines(self) -> list[str]:
        entries = [
            ("layout-engine", self.layout_engine),
            ("theme-id", self.theme_id),
            ("dark-theme-id", self.dark_theme_id),
            ("pad", self.pad),
            ("sketch", self.sketch),
            ("center", self.center),
        ]
        properties = [
            f"{key}: {str(value).lower() if isinstance(value, bool) else value}"
            for key, value in entries
            if value is not None
        ]
        if not properties:
            return []
        return ["vars: {", *indent_lines(add_label_and_properties("d2-config", None, properties)), "}"]


class Layer:
    def __init__(
        self,
        name: str,
        diagram: Diagram | None = None,
    ):
        self.name = name
        self.diagram = diagram or Diagram()

    def set_diagram(self, diagram: Diagram):
        self.diagram = diagram

    def lines(self, depth=1) -> list[str]:
        lines = self.diagram.lines()

        if len(lines) == 0:
            return []

        outer_indent_size = depth * 2
        inner_indent_size = outer_indent_size + 2

        # Wrap lines with layer { } and add indentation
        wrapped_lines = [
            indent(f"{quote_name(self.name)}: {{", outer_indent_size),
            *indent_lines(lines, inner_indent_size),
            indent("}", outer_indent_size),
        ]

        return wrapped_lines

    def __repr__(self) -> str:
        lines = self.lines()
        return "\n".join(lines)


def board_lines(key: str, boards: list[Layer]) -> list[str]:
    lines = [line for board in boards for line in board.lines()]
    return [f"{key}: {{", *lines, "}"] if lines else []


class Diagram:
    def __init__(
        self,
        shapes: list[Shape] | None = None,
        connections: list[Connection] | None = None,
        layers: list[Layer] | None = None,
        *,
        direction: LayoutDirection | None = None,
        classes: dict[str, Style] | None = None,
        vars: Config | None = None,
        scenarios: list[Layer] | None = None,
        steps: list[Layer] | None = None,
        comments: list[str] | None = None,
    ):
        self.shapes = shapes or []
        self.connections = connections or []
        self.layers = layers or []
        self.direction = direction
        self.classes = classes or {}
        self.vars = vars
        self.scenarios = scenarios or []
        self.steps = steps or []
        self.comments = comments or []

    def add_shape(self, shape: Shape):
        self.shapes.append(shape)

    def add_connection(self, connection: Connection):
        self.connections.append(connection)

    def add_layer(self, layer: Layer):
        self.layers.append(layer)

    def add_scenario(self, scenario: Layer):
        self.scenarios.append(scenario)

    def add_step(self, step: Layer):
        self.steps.append(step)

    def add_comment(self, comment: str):
        self.comments.append(comment)

    def class_lines(self) -> list[str]:
        classes = [
            line
            for name, style in self.classes.items()
            if style.lines()
            for line in indent_lines(add_label_and_properties(quote_name(name), None, style.lines()))
        ]
        return ["classes: {", *classes, "}"] if classes else []

    def lines(self) -> list[str]:
        comments = [f"# {line}" for comment in self.comments for line in comment.split("\n")]
        config = self.vars.lines() if self.vars else []
        direction = [f"direction: {self.direction}"] if self.direction else []
        shapes = [str(shape) for shape in self.shapes]
        connections = [str(connection) for connection in self.connections]

        return (
            comments
            + config
            + direction
            + self.class_lines()
            + shapes
            + connections
            + board_lines("layers", self.layers)
            + board_lines("scenarios", self.scenarios)
            + board_lines("steps", self.steps)
        )

    def __repr__(self) -> str:
        lines = self.lines()
        return "\n".join(lines)
