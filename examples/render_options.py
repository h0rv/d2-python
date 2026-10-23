from pathlib import Path

import d2


def main() -> None:
    diagram = d2.Diagram(
        shapes=[d2.Shape(name="a"), d2.Shape(name="b")],
        connections=[d2.Connection("a", "b", "hello")],
    )
    Path("render_options.svg").write_bytes(
        d2.render(
            diagram,
            theme=4,
            dark_theme=200,
            sketch=True,
            pad=20,
            scale=1,
            salt="one",
            omit_version=True,
            no_xml_tag=True,
        )
    )
    Path("render_options.pptx").write_bytes(d2.render(diagram, "pptx"))
    Path("render_options.gif").write_bytes(d2.render(diagram, "gif"))
    print(d2.render(diagram, "txt", ascii_mode="standard").decode())


if __name__ == "__main__":
    main()
