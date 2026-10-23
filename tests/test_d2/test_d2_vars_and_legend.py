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
        "  x: 1",
        "}",
    ]


def test_diagram__legend() -> None:
    diagram = d2.Diagram(
        legend=d2.Legend(
            label="Key",
            shapes=[d2.Shape(name="k", label="Service")],
            connections=[d2.Connection("a", "b", "calls")],
        )
    )

    assert str(diagram).split("\n") == [
        "vars: {",
        "  d2-legend: Key {",
        "    k: Service",
        '    a: "" {',
        "      style: {",
        "        opacity: 0",
        "      }",
        "    }",
        '    b: "" {',
        "      style: {",
        "        opacity: 0",
        "      }",
        "    }",
        "    a -> b: calls",
        "  }",
        "}",
    ]


def test_diagram__legend_without_label() -> None:
    diagram = d2.Diagram(legend=d2.Legend(shapes=[d2.Shape(name="k")]))

    assert str(diagram) == "vars: {\n  d2-legend: {\n    k\n  }\n}"


def test_diagram__one_vars_block() -> None:
    diagram = d2.Diagram(
        vars=d2.Config(layout_engine="tala"),
        variables={"x": 1},
        legend=d2.Legend(shapes=[d2.Shape(name="k")]),
    )

    assert str(diagram).split("\n") == [
        "vars: {",
        "  d2-config: {",
        "    layout-engine: tala",
        "  }",
        "  x: 1",
        "  d2-legend: {",
        "    k",
        "  }",
        "}",
    ]
