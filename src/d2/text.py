import sys

from d2.helpers import indent_lines

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class Text:
    def __init__(
        self,
        # The actual text body (multiline is fine)
        text: str,
        # The format, eg) md, tex, html, css etc
        formatting: str,
        # The number of pipes to use
        pipes: int = 1,
    ) -> None:
        self.text = text
        self.formatting = formatting
        self.pipes = pipes

    def lines(self) -> list[str]:
        sep = "|" * self.pipes
        return [f"{sep}{self.formatting}", *self.text.split("\n"), sep]

    def block_lines(self, key: str) -> list[str]:
        lines = self.lines()
        return [f"{key}: {lines[0]}", *indent_lines(lines[1:-1]), lines[-1]]

    @override
    def __repr__(self) -> str:
        return "\n".join(self.lines())
