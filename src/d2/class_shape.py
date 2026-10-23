from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from d2.helpers import quote
from d2.shape import Shape
from d2.shape import ShapeType
from d2.style import Style


Visibility = Literal["+", "-", "#"]


def member_line(name: str, visibility: Visibility | None, type_: str | None) -> str:
    key = f"{visibility or ''}{name}"
    if visibility == "#":
        key = quote(key)
    return key if type_ is None else f"{key}: {quote(type_)}"


@dataclass(frozen=True)
class ClassField:
    name: str
    type: str | None = None
    visibility: Visibility | None = None

    def lines(self) -> list[str]:
        return [member_line(self.name, self.visibility, self.type)]


@dataclass(frozen=True)
class ClassMethod:
    name: str
    parameters: str = ""
    return_type: str | None = None
    visibility: Visibility | None = None

    def lines(self) -> list[str]:
        return [member_line(f"{self.name}({self.parameters})", self.visibility, self.return_type)]


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
    ):
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

    def add_field(self, field: ClassField):
        self.fields.append(field)

    def add_method(self, method: ClassMethod):
        self.methods.append(method)

    def member_lines(self) -> list[str]:
        return [line for member in (*self.fields, *self.methods) for line in member.lines()]
