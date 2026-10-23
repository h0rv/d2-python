import d2


def test_diagram__variables() -> None:
    diagram = d2.Diagram(
        variables={"env": "prod", "replicas": 3, "ha": True, "empty": ""},
        shapes=[d2.Shape(name="svc", label="${env} service")],
    )

    assert str(diagram).split("\n") == [
        "vars: {",
        "  env: prod",
        "  replicas: 3",
        "  ha: true",
        '  empty: ""',
        "}",
        'svc: "${env} service"',
    ]


def test_diagram__variables_follow_config() -> None:
    diagram = d2.Diagram(vars=d2.Config(sketch=True), variables={"x": "1"})

    assert str(diagram).split("\n") == [
        "vars: {",
        "  d2-config: {",
        "    sketch: true",
        "  }",
        "}",
        "vars: {",
        "  x: 1",
        "}",
    ]


def test_diagram__legend() -> None:
    diagram = d2.Diagram(
        legend=d2.Legend(
            label="Key",
            near="bottom-center",
            shapes=[d2.Shape(name="k", label="Service")],
            connections=[d2.Connection("k", "k", "calls")],
        )
    )

    assert str(diagram).split("\n") == [
        "legend: Key {",
        "  near: bottom-center",
        "  k: Service",
        "  k -> k: calls",
        "}",
    ]


def test_diagram__legend_without_label() -> None:
    diagram = d2.Diagram(legend=d2.Legend(shapes=[d2.Shape(name="k")]))

    assert str(diagram) == "legend: {\n  k\n}"
