from __future__ import annotations

import sys
from enum import Enum
from typing import TYPE_CHECKING, TypeAlias, TypedDict

from d2.connection import Connection, Direction
from d2.helpers import add_label_and_properties, non_empty, quote_name
from d2.shape import Shape, ShapeType, label_parts

if TYPE_CHECKING:
    from collections.abc import Mapping

    from d2.style import Style

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class SQLConstraint(Enum):
    PRIMARY_KEY = "primary_key"
    FOREIGN_KEY = "foreign_key"
    UNIQUE = "unique"


Constraint: TypeAlias = SQLConstraint | str


class SQLFieldSpec(TypedDict, total=False):
    type: str
    constraint: Constraint | list[Constraint] | None


class SQLField:
    def __init__(
        self,
        name: str,
        data_type: str,
        constraint: Constraint | list[Constraint] | None = None,
    ) -> None:
        self.name = name
        self.data_type = data_type
        self.constraints: list[Constraint]
        if constraint is None:
            self.constraints = []
        elif isinstance(constraint, list):
            self.constraints = constraint
        else:
            self.constraints = [constraint]

    def to_d2_format(self) -> str:
        if not self.constraints:
            return f"{self.name}: {self.data_type}"

        constraints_str = "; ".join(
            c.value if isinstance(c, SQLConstraint) else c for c in self.constraints
        )

        if len(self.constraints) == 1:
            constraint_part = constraints_str
        else:
            constraint_part = f"[{constraints_str}]"

        return f"{self.name}: {self.data_type} {{constraint: {constraint_part}}}"


class SQLTable(Shape):
    def __init__(
        self,
        name: str,
        fields: Mapping[str, str | SQLFieldSpec] | None = None,
        label: str | None = None,
        style: Style | None = None,
        icon: str | None = None,
        near: str | None = None,
        link: str | None = None,
    ) -> None:
        super().__init__(
            name=name,
            label=label,
            shape=ShapeType.sql_table,
            style=style,
            icon=icon,
            near=near,
            link=link,
        )

        self.fields: list[SQLField] = []

        if fields is not None:
            for field_name, field_info in fields.items():
                if isinstance(field_info, str):
                    self.add_field(field_name, field_info)
                else:
                    self.add_field(
                        field_name,
                        field_info.get("type", ""),
                        field_info.get("constraint"),
                    )

    def add_field(
        self,
        name: str,
        data_type: str,
        constraint: Constraint | list[Constraint] | None = None,
    ) -> SQLField:
        field = SQLField(name, data_type, constraint)
        self.fields.append(field)
        return field

    @override
    def lines(self) -> list[str]:
        properties: list[str] = []

        if self.shape is not None:
            properties.append(f"shape: {self.shape.value}")

        properties.extend(field.to_d2_format() for field in self.fields)

        if (near := non_empty(self.near)) is not None:
            properties.append(f"near: {near}")

        if (link := non_empty(self.link)) is not None:
            properties.append(f"link: {link}")

        if self.style is not None:
            properties.extend(self.style.lines())

        if (icon := non_empty(self.icon)) is not None:
            properties.append(f"icon: {icon}")

        for shape in self.shapes:
            properties.extend(shape.lines())

        for connection in self.connections:
            properties.extend(connection.lines())

        label, label_lines = label_parts(self.label)
        return add_label_and_properties(
            quote_name(self.name), label, [*label_lines, *properties]
        )


def create_foreign_key_connection(
    source_table: str,
    source_field: str,
    target_table: str,
    target_field: str,
    label: str | None = None,
) -> Connection:
    """Create a foreign key connection between two tables."""
    source = f"{source_table}.{source_field}"
    target = f"{target_table}.{target_field}"
    return Connection(source, target, label, Direction.TO)
