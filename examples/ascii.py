import d2


def main() -> None:
    diagram = d2.Diagram(
        shapes=[d2.Shape(name="a"), d2.Shape(name="b")],
        connections=[d2.Connection("a", "b", "hello")],
    )
    print(d2.render(diagram, "txt").decode())


if __name__ == "__main__":
    main()
