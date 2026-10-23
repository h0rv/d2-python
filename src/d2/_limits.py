from typing import TypeVar

Number = TypeVar("Number", bound=float)


def bounded(
    name: str, value: Number | None, low: float, high: float | None = None
) -> Number | None:
    if value is None or (value >= low and (high is None or value <= high)):
        return value
    if high is None:
        raise ValueError(f"{name} must be at least {low}, got {value}")
    raise ValueError(f"{name} must be between {low} and {high}, got {value}")
