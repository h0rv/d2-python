from d2.helpers import add_label_and_properties, quote, quote_label, quote_name


def test_add_label_and_properties() -> None:
    assert add_label_and_properties("shape_name", None, []) == ["shape_name"]
    assert add_label_and_properties("shape_name", "shape_label", []) == [
        "shape_name: shape_label"
    ]
    assert add_label_and_properties(
        "shape_name", None, ["style: {", "  fill: red", "}"]
    ) == [
        "shape_name: {",
        "  style: {",
        "    fill: red",
        "  }",
        "}",
    ]
    assert add_label_and_properties(
        "shape_name", "shape_label", ["style: {", "  fill: red", "}"]
    ) == [
        "shape_name: shape_label {",
        "  style: {",
        "    fill: red",
        "  }",
        "}",
    ]


def test_quote_escapes_backslash_quote_and_newline() -> None:
    assert quote('a "b" \\ c\nd') == '"a \\"b\\" \\\\ c\\nd"'


def test_quote_name_leaves_plain_names() -> None:
    assert quote_name("shape_name") == "shape_name"
    assert quote_name("my shape") == "my shape"
    assert quote_name("a-b") == "a-b"


def test_quote_name_quotes_unreadable_names() -> None:
    assert quote_name("a.b") == '"a.b"'
    assert quote_name("a:b") == '"a:b"'
    assert quote_name("a#b") == '"a#b"'
    assert quote_name("a{b}") == '"a{b}"'
    assert quote_name("a;b") == '"a;b"'
    assert quote_name("a|b") == '"a|b"'
    assert quote_name('a"b') == '"a\\"b"'
    assert quote_name(" a") == '" a"'
    assert quote_name("a ") == '"a "'
    assert quote_name("a\nb") == '"a\\nb"'
    assert quote_name("a--b") == '"a--b"'


def test_quote_name_quotes_reserved_keywords() -> None:
    for keyword in [
        "shape",
        "style",
        "label",
        "near",
        "layers",
        "scenarios",
        "steps",
        "vars",
        "classes",
        "direction",
    ]:
        assert quote_name(keyword) == f'"{keyword}"'
    assert quote_name("Shape") == '"Shape"'


def test_quote_name_keeps_already_quoted_names() -> None:
    assert quote_name('"a.b"') == '"a.b"'


def test_quote_label_leaves_plain_labels() -> None:
    assert quote_label("hello world") == "hello world"
    assert quote_label("shape") == "shape"
    assert quote_label("it's") == "it's"
    assert quote_label("a.b") == "a.b"


def test_quote_label_quotes_unreadable_labels() -> None:
    assert quote_label("a: b") == '"a: b"'
    assert quote_label("a # b") == '"a # b"'
    assert quote_label("{a}") == '"{a}"'
    assert quote_label("a;b") == '"a;b"'
    assert quote_label("a|b") == '"a|b"'
    assert quote_label(" a") == '" a"'
    assert quote_label("'a") == '"\'a"'
    assert quote_label("a\nb") == '"a\\nb"'


def test_quote_label_keeps_already_quoted_labels() -> None:
    assert quote_label('"#274e13"') == '"#274e13"'


def test_add_label_and_properties_quotes_label() -> None:
    assert add_label_and_properties("a", "x: y", []) == ['a: "x: y"']
