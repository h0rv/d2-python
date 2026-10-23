from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

from d2._limits import bounded
from d2._syntax import (
    Comment,
    Field,
    Key,
    Keyword,
    Label,
    Statement,
    Value,
    emit,
    properties,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from d2.connection import Connection
    from d2.shape import LayoutDirection, NearPosition, Shape
    from d2.style import Style

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


LayoutEngine = Literal["dagre", "elk", "tala"]


@dataclass(frozen=True, kw_only=True)
class Config:
    layout_engine: LayoutEngine | None = None
    theme_id: int | None = None
    dark_theme_id: int | None = None
    pad: int | None = None
    sketch: bool | None = None
    center: bool | None = None

    def __post_init__(self) -> None:
        bounded("theme_id", self.theme_id, 0)
        bounded("dark_theme_id", self.dark_theme_id, 0)

    def statements(self) -> tuple[Field, ...]:
        entries: tuple[tuple[str, Value | None], ...] = (
            ("layout-engine", Keyword.of(self.layout_engine)),
            ("theme-id", self.theme_id),
            ("dark-theme-id", self.dark_theme_id),
            ("pad", self.pad),
            ("sketch", self.sketch),
            ("center", self.center),
        )
        config = properties(entries)
        if not config:
            return ()
        return (
            Field(Keyword("vars"), body=(Field(Keyword("d2-config"), body=config),)),
        )

    def lines(self) -> list[str]:
        return emit(self.statements())


VarValue = str | int | float | bool


@dataclass(frozen=True, kw_only=True)
class Legend:
    shapes: list[Shape] = field(default_factory=list)
    connections: list[Connection] = field(default_factory=list)
    label: str | None = None
    near: NearPosition | None = None

    def statements(self) -> tuple[Field, ...]:
        body: tuple[Statement, ...] = (
            *properties((("near", Keyword.of(self.near)),)),
            *(s for shape in self.shapes for s in shape.statements()),
            *(s for connection in self.connections for s in connection.statements()),
        )
        return (Field(Keyword("legend"), Label.of(self.label), body),)

    def lines(self) -> list[str]:
        return emit(self.statements())


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

    def statements(self) -> tuple[Field, ...]:
        body = self.diagram.statements()
        if not body:
            return ()
        return (Field(Key(self.name), Label.of(self.label), body),)

    def lines(self, depth: int = 1) -> list[str]:
        return emit(self.statements(), depth)

    @override
    def __repr__(self) -> str:
        return "\n".join(self.lines())


def boards(key: str, layers: list[Layer]) -> tuple[Field, ...]:
    body = tuple(s for layer in layers for s in layer.statements())
    return (Field(Keyword(key), body=body),) if body else ()


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

    def class_statements(self) -> tuple[Field, ...]:
        body = tuple(
            Field(Key(name), body=style.statements())
            for name, style in self.classes.items()
            if style.statements()
        )
        return (Field(Keyword("classes"), body=body),) if body else ()

    def variable_statements(self) -> tuple[Field, ...]:
        body = tuple(
            Field(Key(name), Label(value) if isinstance(value, str) else value)
            for name, value in self.variables.items()
        )
        return (Field(Keyword("vars"), body=body),) if body else ()

    def statements(self) -> tuple[Statement, ...]:
        return (
            *(Comment(comment) for comment in self.comments),
            *(self.vars.statements() if self.vars is not None else ()),
            *self.variable_statements(),
            *properties((("direction", Keyword.of(self.direction)),)),
            *self.class_statements(),
            *(s for shape in self.shapes for s in shape.statements()),
            *(s for connection in self.connections for s in connection.statements()),
            *(self.legend.statements() if self.legend is not None else ()),
            *boards("layers", self.layers),
            *boards("scenarios", self.scenarios),
            *boards("steps", self.steps),
        )

    def lines(self) -> list[str]:
        return emit(self.statements())

    @override
    def __repr__(self) -> str:
        return "\n".join(self.lines())
