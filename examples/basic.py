from pathlib import Path

import d2


def main() -> None:
    diagram = d2.Diagram(
        shapes=[
            d2.Shape(name="client", label="Web client"),
            d2.Shape(name="server", label="API server"),
        ],
        connections=[d2.Connection("client", "server", "request")],
    )
    Path("basic.svg").write_bytes(d2.render(diagram))


if __name__ == "__main__":
    main()
