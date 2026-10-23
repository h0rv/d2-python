from pathlib import Path

import d2


def main() -> None:
    diagram = d2.Diagram(
        shapes=[
            d2.Shape(name="*", style=d2.Style(fill="#dbeafe")),
            d2.Shape(name="api"),
            d2.Shape(name="db"),
            d2.Shape(name="cache"),
        ],
        connections=[d2.Connection("api", "db"), d2.Connection("api", "cache")],
    )

    d2.validate(diagram)
    print(d2.fmt(diagram))

    try:
        d2.validate("api -> {")
    except d2.D2Error as error:
        print(f"invalid: {error}")

    Path("validation.svg").write_bytes(d2.render(diagram))


if __name__ == "__main__":
    main()
