def indent(line, n: int = 2) -> str:
    return f"{' ' * n}{line}"


def indent_lines(items: list[str], n: int = 2) -> list[str]:
    return [indent(item, n) for item in items]


def add_label_and_properties(name: str, label: str | None = None, properties: list[str] | None = None) -> list[str]:
    has_properties: bool = properties is not None and len(properties) > 0

    first_line = name
    if label is not None or has_properties:
        first_line += ":"

    if label is not None and len(label) == 0:
        first_line += ' ""'

    if label and len(label) > 0:
        first_line += f" {label}"

    if has_properties:
        first_line += " {"

    if properties and has_properties:
        return [first_line, *indent_lines(properties), "}"]

    return [first_line]


def flatten(items: list[list[str]]) -> list[str]:
    return [item for sublist in items for item in sublist]
