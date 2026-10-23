from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

from d2.helpers import (
    add_label_and_properties,
    indent,
    indent_lines,
    quote_label,
    quote_name,
)
from d2.raw import Raw

if TYPE_CHECKING:
    from collections.abc import Mapping

    from d2.connection import Connection
    from d2.shape import LayoutDirection, Shape
    from d2.style import Style

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


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
        return [
            "vars: {",
            *indent_lines(add_label_and_properties("d2-config", None, properties)),
            "}",
        ]


VarValue = str | int | float | bool


def var_lines(variables: Mapping[str, VarValue]) -> list[str]:
    entries = [
        f"{quote_name(name)}: "
        + (
            str(value).lower()
            if isinstance(value, bool)
            else ('""' if value == "" else quote_label(str(value)))
        )
        for name, value in variables.items()
    ]
    return ["vars: {", *indent_lines(entries), "}"] if entries else []


@dataclass(frozen=True, kw_only=True)
class Legend:
    shapes: list[Shape] = field(default_factory=list)
    connections: list[Connection] = field(default_factory=list)
    label: str | None = None
    near: str | None = None

    def lines(self) -> list[str]:
        properties = [f"near: {self.near}"] if self.near is not None else []
        properties += [line for shape in self.shapes for line in shape.lines()]
        properties += [
            line for connection in self.connections for line in connection.lines()
        ]
        return add_label_and_properties("legend", self.label, properties)


class Layer:
    def __init__(
        self,
        name: str,
        diagram: Diagram | None = None,
        *,
        label: str | None = None,
    ) -> None:
        self.name = name
        self.label = label
        self.diagram = Diagram() if diagram is None else diagram

    def set_diagram(self, diagram: Diagram) -> None:
        self.diagram = diagram

    def lines(self, depth: int = 1) -> list[str]:
        lines = self.diagram.lines()

        if len(lines) == 0:
            return []

        outer_indent_size = depth * 2
        inner_indent_size = outer_indent_size + 2

        title = f" {quote_label(self.label)}" if self.label is not None else ""
        return [
            indent(f"{quote_name(self.name)}:{title} {{", outer_indent_size),
            *indent_lines(lines, inner_indent_size),
            indent("}", outer_indent_size),
        ]

    @override
    @override
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
        variables: Mapping[str, VarValue] | None = None,
        legend: Legend | None = None,
        raw: Raw | str | None = None,
    ) -> None:
        self.shapes = shapes or []
        self.connections = connections or []
        self.layers = layers or []
        self.direction = direction
        self.classes = classes or {}
        self.vars = vars
        self.scenarios = scenarios or []
        self.steps = steps or []
        self.comments = comments or []
        self.variables = dict(variables) if variables is not None else {}
        self.legend = legend
        self.raws: list[Raw] = [] if raw is None else [Raw.parse(raw)]

    def add_shape(self, shape: Shape) -> None:
        self.shapes.append(shape)

    def add_connection(self, connection: Connection) -> None:
        self.connections.append(connection)

    def add_layer(self, layer: Layer) -> None:
        self.layers.append(layer)

    def add_scenario(self, scenario: Layer) -> None:
        self.scenarios.append(scenario)

    def add_step(self, step: Layer) -> None:
        self.steps.append(step)

    def add_comment(self, comment: str) -> None:
        self.comments.append(comment)

    def add_raw(self, raw: Raw | str) -> None:
        self.raws.append(Raw.parse(raw))

    def class_lines(self) -> list[str]:
        classes = [
            line
            for name, style in self.classes.items()
            if style.lines()
            for line in indent_lines(
                add_label_and_properties(quote_name(name), None, style.lines())
            )
        ]
        return ["classes: {", *classes, "}"] if classes else []

    def lines(self) -> list[str]:
        comments = [
            f"# {line}" for comment in self.comments for line in comment.split("\n")
        ]
        config = self.vars.lines() if self.vars is not None else []
        direction = (
            [f"direction: {self.direction}"] if self.direction is not None else []
        )
        shapes = [str(shape) for shape in self.shapes]
        connections = [str(connection) for connection in self.connections]

        return (
            comments
            + config
            + var_lines(self.variables)
            + direction
            + self.class_lines()
            + shapes
            + connections
            + (self.legend.lines() if self.legend is not None else [])
            + board_lines("layers", self.layers)
            + board_lines("scenarios", self.scenarios)
            + board_lines("steps", self.steps)
            + [line for raw in self.raws for line in raw.lines()]
        )

    @override
    def __repr__(self) -> str:
        lines = self.lines()
        return "\n".join(lines)
