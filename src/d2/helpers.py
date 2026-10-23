import re

RESERVED_KEYWORDS = frozenset(
    {
        "shape",
        "style",
        "label",
        "near",
        "layers",
        "scenarios",
        "steps",
        "vars",
        "classes",
        "class",
        "direction",
        "icon",
        "link",
        "tooltip",
        "width",
        "height",
        "constraint",
        "grid-rows",
        "grid-columns",
        "grid-gap",
        "source-arrowhead",
        "target-arrowhead",
    }
)

QUOTED_PATTERN = re.compile(r'"(?:[^"\\\n]|\\.)*"')
NAME_SPECIAL_PATTERN = re.compile(r"[.:{}#;|\"'\\\n]|->|<-|--|^\s|\s$")
LABEL_SPECIAL_PATTERN = re.compile(r"[:{}#;|\"\n]|^\s|\s$|^'")


def non_empty(value: str | None) -> str | None:
    if value is None or value == "":
        return None
    return value


def quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


def quote_name(name: str) -> str:
    if QUOTED_PATTERN.fullmatch(name):
        return name
    if (
        not name
        or name.lower() in RESERVED_KEYWORDS
        or NAME_SPECIAL_PATTERN.search(name)
    ):
        return quote(name)
    return name


def quote_label(label: str) -> str:
    if QUOTED_PATTERN.fullmatch(label):
        return label
    if LABEL_SPECIAL_PATTERN.search(label):
        return quote(label)
    return label


def indent(line: str, n: int = 2) -> str:
    return f"{' ' * n}{line}"


def indent_lines(items: list[str], n: int = 2) -> list[str]:
    return [indent(item, n) for item in items]


def add_label_and_properties(
    name: str, label: str | None = None, properties: list[str] | None = None
) -> list[str]:
    has_properties: bool = properties is not None and len(properties) > 0

    first_line = name
    if label is not None or has_properties:
        first_line += ":"

    if label == "":
        first_line += ' ""'
    elif label is not None:
        first_line += f" {quote_label(label)}"

    if has_properties:
        first_line += " {"

    if properties is not None and has_properties:
        return [first_line, *indent_lines(properties), "}"]

    return [first_line]


def flatten(items: list[list[str]]) -> list[str]:
    return [item for sublist in items for item in sublist]
