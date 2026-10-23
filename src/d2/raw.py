import sys
import textwrap
from dataclasses import dataclass

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


@dataclass(frozen=True)
class Raw:
    source: str

    @classmethod
    def parse(cls, value: "Raw | str") -> "Raw":
        return cls(value) if isinstance(value, str) else value

    def lines(self) -> list[str]:
        body = textwrap.dedent(self.source).strip("\n")
        return body.split("\n") if body.strip() else []

    @override
    def __str__(self) -> str:
        return "\n".join(self.lines())
