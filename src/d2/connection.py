from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from enum import StrEnum

from d2.helpers import add_label_and_properties
from d2.helpers import indent_lines
from d2.helpers import quote_label
from d2.style import Style


class Direction(Enum):
    TO = "->"
    FROM = "<-"
    BOTH = "<->"
    NONE = "--"


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

    def lines(self, key: str) -> list[str]:
        properties = [f"shape: {self.shape.value}"]
        if self.label:
            properties.append(f"label: {quote_label(self.label)}")
        if self.filled is not None:
            properties.append(f"style.filled: {'true' if self.filled else 'false'}")
        return [f"{key}: {{", *indent_lines(properties), "}"]


class Connection:
    def __init__(
        self,
        shape_1: str,
        shape_2: str,
        label: str | None = None,
        direction: Direction = Direction.TO,
        *,
        style: Style | None = None,
        source_arrowhead: Arrowhead | None = None,
        target_arrowhead: Arrowhead | None = None,
        tooltip: str | None = None,
    ):
        self.shape_1 = shape_1
        self.shape_2 = shape_2
        self.label = label
        self.direction = direction
        self.style = style
        self.source_arrowhead = source_arrowhead
        self.target_arrowhead = target_arrowhead
        self.tooltip = tooltip

    def lines(self) -> list[str]:
        properties: list[str] = []
        if self.tooltip:
            properties.append(f"tooltip: {quote_label(self.tooltip)}")
        if self.source_arrowhead:
            properties += self.source_arrowhead.lines("source-arrowhead")
        if self.target_arrowhead:
            properties += self.target_arrowhead.lines("target-arrowhead")
        if self.style:
            properties += self.style.lines()

        base = f"{self.shape_1} {self.direction.value} {self.shape_2}"
        return add_label_and_properties(base, self.label or None, properties)

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
        )

    def __hash__(self):
        return hash((self.shape_1, self.shape_2, self.label, self.direction))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Connection):
            return NotImplemented
        return self._key() == other._key()
