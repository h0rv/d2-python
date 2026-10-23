from pathlib import Path

import d2


def main() -> None:
    diagram = d2.Diagram(
        shapes=[
            d2.Shape(
                name="backend",
                shapes=[
                    d2.Shape(name="api"),
                    d2.Shape(name="worker"),
                    d2.Shape(name="cache", shapes=[d2.Shape(name="redis")]),
                ],
                connections=[d2.Connection("api", "worker", "enqueue")],
            ),
            d2.Shape(name="frontend"),
        ],
        connections=[
            d2.Connection("frontend", "backend.api", "HTTP"),
            d2.Connection("backend.worker", "backend.cache.redis", "reads"),
        ],
    )
    Path("containers.svg").write_bytes(d2.render(diagram))


if __name__ == "__main__":
    main()
