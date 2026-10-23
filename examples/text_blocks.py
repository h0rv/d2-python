from pathlib import Path

import d2


def main() -> None:
    diagram = d2.Diagram(
        shapes=[
            d2.Shape(
                name="notes",
                explanation=d2.Text("# Notes\n- first\n- **second**", "md"),
            ),
            d2.Shape(
                name="snippet",
                code=d2.Text('print("hello")', "python"),
            ),
        ],
        connections=[d2.Connection("notes", "snippet")],
    )
    Path("text_blocks.svg").write_bytes(d2.render(diagram))


if __name__ == "__main__":
    main()
