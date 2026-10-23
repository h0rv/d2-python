from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING, Literal

from d2._syntax import (
    Direction,
    Edge,
    Field,
    Keyword,
    Label,
    Statement,
    Text,
    Url,
    class_references,
    emit,
    properties,
    split_label,
)

if TYPE_CHECKING:
    from d2.style import Style

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

__all__ = [
    "Arrowhead",
    "ArrowheadShape",
    "Connection",
    "Direction",
]


class ArrowheadShape(StrEnum):
    TRIANGLE = "triangle"
    ARROW = "arrow"
    DIAMOND = "diamond"
    CIRCLE = "circle"
    BOX = "box"
    CF_ONE = "cf-one"
    CF_ONE_REQUIRED = "cf-one-required"
    CF_MANY = "cf-many"
    CF_MANY_REQUIRED = "cf-many-required"
    CROSS = "cross"


@dataclass(frozen=True)
class Arrowhead:
    shape: ArrowheadShape
    label: str | None = None
    filled: bool | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "label", self.label or None)

    def statement(self, key: Literal["source-arrowhead", "target-arrowhead"]) -> Field:
        return Field(
            Keyword(key),
            body=properties(
                (
                    ("shape", self.shape),
                    ("label", Label.of(self.label)),
                    ("style.filled", self.filled),
                )
            ),
        )

    def lines(self, key: Literal["source-arrowhead", "target-arrowhead"]) -> list[str]:
        return emit((self.statement(key),))


class Connection:
    def __init__(
        self,
        shape_1: str,
        shape_2: str,
        label: str | Text | None = None,
        direction: Direction = Direction.TO,
        *,
        style: Style | None = None,
        source_arrowhead: Arrowhead | None = None,
        target_arrowhead: Arrowhead | None = None,
        tooltip: str | None = None,
        icon: str | None = None,
        link: str | None = None,
        classes: list[str] | None = None,
    ) -> None:
        self.shape_1 = shape_1
        self.shape_2 = shape_2
        self.label = label or None
        self.direction = direction
        self.style = style
        self.source_arrowhead = source_arrowhead
        self.target_arrowhead = target_arrowhead
        self.tooltip = tooltip or None
        self.icon = icon or None
        self.link = link or None
        self.classes = classes or []

    def statements(self) -> tuple[Edge, ...]:
        label, label_block = split_label(self.label)
        body: tuple[Statement, ...] = (
            *label_block,
            *properties((("tooltip", Label.of(self.tooltip)),)),
            *(
                head.statement(key)
                for key, head in (
                    ("source-arrowhead", self.source_arrowhead),
                    ("target-arrowhead", self.target_arrowhead),
                )
                if head is not None
            ),
            *(self.style.statements() if self.style is not None else ()),
            *properties(
                (("icon", Url.of(self.icon)), ("link", Url.of(self.link))),
            ),
            *class_references(self.classes),
        )
        return (
            Edge(
                Keyword(self.shape_1),
                self.direction,
                Keyword(self.shape_2),
                label,
                body,
            ),
        )

    def lines(self) -> list[str]:
        return emit(self.statements())

    @override
    def __repr__(self) -> str:
        return "\n".join(self.lines())

    def _key(self) -> tuple[object, ...]:
        return (
            self.shape_1,
            self.shape_2,
            self.direction,
            self.label,
            self.style,
            self.source_arrowhead,
            self.target_arrowhead,
            self.tooltip,
            self.icon,
            self.link,
            self.classes,
        )

    @override
    def __hash__(self) -> int:
        return hash((self.shape_1, self.shape_2, self.label, self.direction))

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Connection):
            return NotImplemented
        return self._key() == other._key()
