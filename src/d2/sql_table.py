from __future__ import annotations

import sys
from enum import Enum
from typing import TYPE_CHECKING, TypeAlias, TypedDict

from d2._syntax import (
    Field,
    Key,
    Keyword,
    Label,
    Statement,
    Url,
    emit,
    one_or_array,
    properties,
)
from d2.connection import Connection, Direction
from d2.shape import Shape, ShapeType

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

    def statement(self) -> Field:
        constraints = [
            Label(c.value if isinstance(c, SQLConstraint) else c)
            for c in self.constraints
        ]
        body = (
            (Field(Keyword("constraint"), one_or_array(constraints)),)
            if constraints
            else ()
        )
        return Field(Key(self.name), Label(self.data_type), body, inline=True)

    def to_d2_format(self) -> str:
        return emit((self.statement(),))[0]


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
    def body(self) -> tuple[Statement, ...]:
        return (
            *properties((("shape", self.shape),)),
            *(field.statement() for field in self.fields),
            *properties((("near", Keyword.of(self.near)), ("link", Url.of(self.link)))),
            *(self.style.statements() if self.style is not None else ()),
            *properties((("icon", Url.of(self.icon)),)),
            *(s for shape in self.shapes for s in shape.statements()),
            *(s for connection in self.connections for s in connection.statements()),
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
