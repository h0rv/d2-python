from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from d2._syntax import Field, Key, Quoted, Statement, emit
from d2.shape import Shape, ShapeType

if TYPE_CHECKING:
    from d2.style import Style

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


Visibility = Literal["+", "-", "#"]


def member(name: str, visibility: Visibility | None, type_: str | None) -> Field:
    key = Key(name if visibility is None else f"{visibility}{name}")
    return Field(key, None if type_ is None else Quoted(type_))


@dataclass(frozen=True)
class ClassField:
    name: str
    type: str | None = None
    visibility: Visibility | None = None

    def statement(self) -> Field:
        return member(self.name, self.visibility, self.type)

    def lines(self) -> list[str]:
        return emit((self.statement(),))


@dataclass(frozen=True)
class ClassMethod:
    name: str
    parameters: str = ""
    return_type: str | None = None
    visibility: Visibility | None = None

    def statement(self) -> Field:
        return member(
            f"{self.name}({self.parameters})", self.visibility, self.return_type
        )

    def lines(self) -> list[str]:
        return emit((self.statement(),))


class ClassShape(Shape):
    def __init__(
        self,
        name: str,
        fields: list[ClassField] | None = None,
        methods: list[ClassMethod] | None = None,
        label: str | None = None,
        style: Style | None = None,
        icon: str | None = None,
        near: str | None = None,
        link: str | None = None,
    ) -> None:
        super().__init__(
            name=name,
            label=label,
            shape=ShapeType.classs,
            style=style,
            icon=icon,
            near=near,
            link=link,
        )
        self.fields = fields or []
        self.methods = methods or []

    def add_field(self, field: ClassField) -> None:
        self.fields.append(field)

    def add_method(self, method: ClassMethod) -> None:
        self.methods.append(method)

    @override
    def members(self) -> tuple[Statement, ...]:
        return tuple(item.statement() for item in (*self.fields, *self.methods))
