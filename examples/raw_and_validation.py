from pathlib import Path

import d2


def main() -> None:
    diagram = d2.Diagram(
        shapes=[d2.Shape(name="api"), d2.Shape(name="db"), d2.Shape(name="cache")],
        connections=[d2.Connection("api", "db"), d2.Connection("api", "cache")],
        raw="""
            # D2 the object model does not cover yet: a glob and a connection reference
            *.style.fill: "#dbeafe"
            (api -> db)[0].style.stroke: red
        """,
    )

    d2.validate(diagram)
    print(d2.format(diagram))

    try:
        d2.validate("api -> {")
    except d2.D2Error as error:
        print(f"invalid: {error}")

    Path("raw_and_validation.svg").write_bytes(d2.render(diagram))


if __name__ == "__main__":
    main()
