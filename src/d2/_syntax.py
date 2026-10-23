from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Final, TypeAlias, TypeVar, assert_never

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


INDENT: Final = "  "

RESERVED_KEYWORDS: Final = frozenset(
    {
        "label",
        "shape",
        "icon",
        "constraint",
        "tooltip",
        "link",
        "near",
        "width",
        "height",
        "direction",
        "top",
        "left",
        "grid-rows",
        "grid-columns",
        "grid-gap",
        "vertical-gap",
        "horizontal-gap",
        "class",
        "vars",
        "style",
        "source-arrowhead",
        "target-arrowhead",
        "classes",
        "opacity",
        "stroke",
        "fill",
        "fill-pattern",
        "stroke-width",
        "stroke-dash",
        "border-radius",
        "font",
        "font-size",
        "font-color",
        "bold",
        "italic",
        "underline",
        "text-transform",
        "shadow",
        "multiple",
        "double-border",
        "3d",
        "animated",
        "filled",
        "layers",
        "scenarios",
        "steps",
    }
)

CSS_COLORS: Final = frozenset(
    [
        "aliceblue",
        "antiquewhite",
        "aqua",
        "aquamarine",
        "azure",
        "beige",
        "bisque",
        "black",
        "blanchedalmond",
        "blue",
        "blueviolet",
        "brown",
        "burlywood",
        "cadetblue",
        "chartreuse",
        "chocolate",
        "coral",
        "cornflowerblue",
        "cornsilk",
        "crimson",
        "cyan",
        "darkblue",
        "darkcyan",
        "darkgoldenrod",
        "darkgray",
        "darkgreen",
        "darkgrey",
        "darkkhaki",
        "darkmagenta",
        "darkolivegreen",
        "darkorange",
        "darkorchid",
        "darkred",
        "darksalmon",
        "darkseagreen",
        "darkslateblue",
        "darkslategray",
        "darkslategrey",
        "darkturquoise",
        "darkviolet",
        "deeppink",
        "deepskyblue",
        "dimgray",
        "dimgrey",
        "dodgerblue",
        "firebrick",
        "floralwhite",
        "forestgreen",
        "fuchsia",
        "gainsboro",
        "ghostwhite",
        "gold",
        "goldenrod",
        "gray",
        "green",
        "greenyellow",
        "grey",
        "honeydew",
        "hotpink",
        "indianred",
        "indigo",
        "ivory",
        "khaki",
        "lavender",
        "lavenderblush",
        "lawngreen",
        "lemonchiffon",
        "lightblue",
        "lightcoral",
        "lightcyan",
        "lightgoldenrodyellow",
        "lightgray",
        "lightgreen",
        "lightgrey",
        "lightpink",
        "lightsalmon",
        "lightseagreen",
        "lightskyblue",
        "lightslategray",
        "lightslategrey",
        "lightsteelblue",
        "lightyellow",
        "lime",
        "limegreen",
        "linen",
        "magenta",
        "maroon",
        "mediumaquamarine",
        "mediumblue",
        "mediumorchid",
        "mediumpurple",
        "mediumseagreen",
        "mediumslateblue",
        "mediumspringgreen",
        "mediumturquoise",
        "mediumvioletred",
        "midnightblue",
        "mintcream",
        "mistyrose",
        "moccasin",
        "navajowhite",
        "navy",
        "oldlace",
        "olive",
        "olivedrab",
        "orange",
        "orangered",
        "orchid",
        "palegoldenrod",
        "palegreen",
        "paleturquoise",
        "palevioletred",
        "papayawhip",
        "peachpuff",
        "peru",
        "pink",
        "plum",
        "powderblue",
        "purple",
        "rebeccapurple",
        "red",
        "rosybrown",
        "royalblue",
        "saddlebrown",
        "salmon",
        "sandybrown",
        "seagreen",
        "seashell",
        "sienna",
        "silver",
        "skyblue",
        "slateblue",
        "slategray",
        "slategrey",
        "snow",
        "springgreen",
        "steelblue",
        "tan",
        "teal",
        "thistle",
        "tomato",
        "turquoise",
        "violet",
        "wheat",
        "white",
        "whitesmoke",
        "yellow",
        "yellowgreen",
        "transparent",
        "currentcolor",
    ]
)

KEY_SPECIAL: Final = re.compile(
    r"""^$|[.:{}\[\]#;|"'\\&<>\n]|--|^\s|\s$|^[@(!]|-$|^_$"""
)
LABEL_SPECIAL: Final = re.compile(
    r"""^$|[:{}\[\]#;|"\\$\n]|^\s|\s$|^['@]|^(?i:null)$"""
)
URL_SPECIAL: Final = re.compile(r"""^$|[{}\[\]#;|"\\$\n]|^\s|\s$|^['@]""")
LONE_DOLLAR: Final = re.compile(r"\$(?!\{)")
PIPE_RUN: Final = re.compile(r"\|+")
BLOCK_TAG_SPECIAL: Final = re.compile(r"[\s|`]")
QUOTED_COLOR: Final = re.compile(r'"(.*)"', re.DOTALL)
HEX_COLOR: Final = re.compile(r"#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})")
GRADIENT_COLOR: Final = re.compile(
    r"""(?:linear|radial)-gradient\([^()"\\\n]+(?:\([^()"\\\n]*\)[^()"\\\n]*)*\)"""
)
VARIABLE_COLOR: Final = re.compile(r"\$\{[^{}\"\\\n]+\}")


def quote(text: str) -> str:
    escaped = text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    escaped = LONE_DOLLAR.sub(r"\\$", escaped)
    return f'"{escaped}"'


class Direction(Enum):
    TO = "->"
    FROM = "<-"
    BOTH = "<->"
    NONE = "--"


@dataclass(frozen=True, slots=True)
class Key:
    name: str

    @override
    def __str__(self) -> str:
        if self.name.lower() in RESERVED_KEYWORDS or KEY_SPECIAL.search(self.name):
            return quote(self.name)
        return self.name


@dataclass(frozen=True, slots=True)
class Keyword:
    text: str

    @classmethod
    def of(cls, text: str | None) -> Keyword | None:
        return None if text is None else cls(text)

    @override
    def __str__(self) -> str:
        return self.text


@dataclass(frozen=True, slots=True)
class Label:
    text: str

    @classmethod
    def of(cls, text: str | None) -> Label | None:
        return None if text is None else cls(text)

    @override
    def __str__(self) -> str:
        return quote(self.text) if LABEL_SPECIAL.search(self.text) else self.text


@dataclass(frozen=True, slots=True)
class Url:
    text: str

    @classmethod
    def of(cls, text: str | None) -> Url | None:
        return None if text is None else cls(text)

    @override
    def __str__(self) -> str:
        return quote(self.text) if URL_SPECIAL.search(self.text) else self.text


@dataclass(frozen=True, slots=True)
class Quoted:
    text: str

    @override
    def __str__(self) -> str:
        return quote(self.text)


@dataclass(frozen=True, slots=True)
class Color:
    value: str

    def __post_init__(self) -> None:
        text = self.value.strip()
        if (unquoted := QUOTED_COLOR.fullmatch(text)) is not None:
            text = unquoted.group(1)
        if text.lower() in CSS_COLORS:
            parsed = text.lower()
        elif (hex_digits := HEX_COLOR.fullmatch(text)) is not None:
            parsed = f"#{hex_digits.group(1).lower()}"
        elif GRADIENT_COLOR.fullmatch(text) or VARIABLE_COLOR.fullmatch(text):
            parsed = text
        else:
            raise ValueError(
                f"{self.value!r} is not a D2 color: use a CSS color name, "
                "a 3 or 6 digit hex code, a linear-gradient(...) or "
                "radial-gradient(...), or a ${variable}"
            )
        object.__setattr__(self, "value", parsed)

    @classmethod
    def of(cls, value: str | Color | None) -> Color | None:
        if value is None or value == "":
            return None
        return value if isinstance(value, Color) else cls(value)

    @override
    def __str__(self) -> str:
        return self.value if self.value.isalpha() else quote(self.value)


Scalar: TypeAlias = (
    Key | Keyword | Label | Url | Quoted | Color | Enum | bool | int | float
)


@dataclass(frozen=True, slots=True)
class Array:
    items: tuple[Scalar, ...]

    @override
    def __str__(self) -> str:
        return f"[{'; '.join(render(item) for item in self.items)}]"


Value: TypeAlias = Scalar | Array

Item = TypeVar("Item", bound=Scalar)


def render(value: Value) -> str:
    match value:
        case bool():
            return "true" if value else "false"
        case int() | float():
            return str(value)
        case Enum():
            return str(value.value)
        case Key() | Keyword() | Label() | Url() | Quoted() | Color() | Array():
            return str(value)
        case _:
            assert_never(value)


def one_or_array(items: Sequence[Item]) -> Item | Array:
    return items[0] if len(items) == 1 else Array(tuple(items))


@dataclass(frozen=True, slots=True, repr=False)
class Text:
    text: str
    formatting: str
    pipes: int = 1

    def __post_init__(self) -> None:
        if BLOCK_TAG_SPECIAL.search(self.formatting):
            raise ValueError(
                f"formatting must not have whitespace, | or `: {self.formatting!r}"
            )
        longest = max((len(run) for run in PIPE_RUN.findall(self.text)), default=0)
        object.__setattr__(self, "pipes", max(self.pipes, longest + 1))

    def lines(self) -> list[str]:
        bar = "|" * self.pipes
        return [f"{bar}{self.formatting}", *self.text.split("\n"), bar]

    def block_lines(self, key: str) -> list[str]:
        return emit((BlockField(Keyword(key), self),))

    @override
    def __repr__(self) -> str:
        return "\n".join(self.lines())


@dataclass(frozen=True, slots=True)
class Field:
    key: Key | Keyword
    value: Value | None = None
    body: tuple[Statement, ...] = ()
    inline: bool = False


@dataclass(frozen=True, slots=True)
class BlockField:
    key: Key | Keyword
    text: Text


@dataclass(frozen=True, slots=True)
class Edge:
    source: Keyword
    operator: Direction
    target: Keyword
    label: Label | None = None
    body: tuple[Statement, ...] = ()


@dataclass(frozen=True, slots=True)
class Comment:
    text: str


Statement: TypeAlias = Field | BlockField | Edge | Comment


def properties(entries: Iterable[tuple[str, Value | None]]) -> tuple[Field, ...]:
    return tuple(
        Field(Keyword(key), value) for key, value in entries if value is not None
    )


def split_label(
    label: str | Text | None,
) -> tuple[Label | None, tuple[BlockField, ...]]:
    if isinstance(label, Text):
        return None, (BlockField(Keyword("label"), label),)
    return Label.of(label), ()


def class_references(names: Sequence[str]) -> tuple[Field, ...]:
    if not names:
        return ()
    return (Field(Keyword("class"), one_or_array([Key(name) for name in names])),)


def nest(
    head: str, body: Sequence[Statement], depth: int, *, inline: bool
) -> list[str]:
    pad = INDENT * depth
    if not body:
        return [f"{pad}{head}"]
    if inline:
        return [f"{pad}{head} {{{'; '.join(emit(body))}}}"]
    return [f"{pad}{head} {{", *emit(body, depth + 1), f"{pad}}}"]


def emit(statements: Iterable[Statement], depth: int = 0) -> list[str]:
    pad = INDENT * depth
    lines: list[str] = []
    for statement in statements:
        match statement:
            case Comment(text):
                lines += [f"{pad}# {line}" for line in text.split("\n")]
            case BlockField(key, text):
                opening, *content, closing = text.lines()
                lines += [
                    f"{pad}{key}: {opening}",
                    *(f"{pad}{INDENT}{line}" for line in content),
                    f"{pad}{closing}",
                ]
            case Field(key, value, body, inline):
                head = str(key)
                if value is not None:
                    head += f": {render(value)}"
                elif body:
                    head += ":"
                lines += nest(head, body, depth, inline=inline)
            case Edge(source, operator, target, label, body):
                head = f"{source} {operator.value} {target}"
                if label is not None:
                    head += f": {label}"
                elif body:
                    head += ":"
                lines += nest(head, body, depth, inline=False)
            case _:
                assert_never(statement)
    return lines
