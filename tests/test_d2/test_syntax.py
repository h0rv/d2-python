from collections.abc import Callable

import pytest

import d2
from d2._syntax import (
    Array,
    BlockField,
    Color,
    Comment,
    Direction,
    Edge,
    Field,
    Key,
    Keyword,
    Label,
    Quoted,
    Text,
    Url,
    emit,
    one_or_array,
    quote,
)


def test_quote__escapes_backslash_quote_and_newline() -> None:
    assert quote('a "b" \\ c\nd') == '"a \\"b\\" \\\\ c\\nd"'


def test_quote__escapes_dollars_that_do_not_start_a_substitution() -> None:
    assert quote("cost $5") == '"cost \\$5"'
    assert quote("${env} costs $5") == '"${env} costs \\$5"'


@pytest.mark.parametrize("name", ["shape_name", "my shape", "a-b", "a$b", "*", "1"])
def test_key__leaves_plain_names(name: str) -> None:
    assert str(Key(name)) == name


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("a.b", '"a.b"'),
        ("a:b", '"a:b"'),
        ("a#b", '"a#b"'),
        ("a{b}", '"a{b}"'),
        ("a[0]", '"a[0]"'),
        ("a;b", '"a;b"'),
        ("a|b", '"a|b"'),
        ("a&b", '"a&b"'),
        ("a>b", '"a>b"'),
        ('a"b', '"a\\"b"'),
        ("a'b", '"a\'b"'),
        (" a", '" a"'),
        ("a ", '"a "'),
        ("a\nb", '"a\\nb"'),
        ("a--b", '"a--b"'),
        ("@a", '"@a"'),
        ("(a)", '"(a)"'),
        ("!", '"!"'),
        ("a-", '"a-"'),
        ("_", '"_"'),
        ("", '""'),
    ],
)
def test_key__quotes_unreadable_names(name: str, expected: str) -> None:
    assert str(Key(name)) == expected


@pytest.mark.parametrize(
    "keyword",
    [
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
        "shadow",
        "Shape",
        "Fill",
    ],
)
def test_key__quotes_reserved_keywords(keyword: str) -> None:
    assert str(Key(keyword)) == f'"{keyword}"'


def test_key__does_not_keep_already_quoted_names() -> None:
    assert str(Key('"a.b"')) == '"\\"a.b\\""'


@pytest.mark.parametrize("text", ["hello world", "shape", "it's", "a.b", "a, b", "1"])
def test_label__leaves_plain_labels(text: str) -> None:
    assert str(Label(text)) == text


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("a: b", '"a: b"'),
        ("a # b", '"a # b"'),
        ("{a}", '"{a}"'),
        ("a;b", '"a;b"'),
        ("a|b", '"a|b"'),
        ("a[0]", '"a[0]"'),
        ("a\\b", '"a\\\\b"'),
        ("$5", '"\\$5"'),
        (" a", '" a"'),
        ("'a", '"\'a"'),
        ("@a", '"@a"'),
        ("a\nb", '"a\\nb"'),
        ("null", '"null"'),
        ("NULL", '"NULL"'),
        ("", '""'),
    ],
)
def test_label__quotes_unreadable_labels(text: str, expected: str) -> None:
    assert str(Label(text)) == expected


def test_label__does_not_keep_already_quoted_labels() -> None:
    assert str(Label('"x"')) == '"\\"x\\""'


def test_url__keeps_colons_and_quotes_comment_starts() -> None:
    assert str(Url("https://x.test/i.svg?a=1&b=2")) == "https://x.test/i.svg?a=1&b=2"
    assert str(Url("https://x.test/a#top")) == '"https://x.test/a#top"'
    assert str(Url("")) == '""'


def test_quoted__always_quotes() -> None:
    assert str(Quoted("string")) == '"string"'


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("red", "red"),
        ("Red", "red"),
        ("transparent", "transparent"),
        ("currentColor", "currentcolor"),
        ("#DBEAFE", "#dbeafe"),
        ("dbeafe", "#dbeafe"),
        ("#FFF", "#fff"),
        ("abc", "#abc"),
        ('"#274e13"', "#274e13"),
        ("linear-gradient(#f69d3c, #3f87a6)", "linear-gradient(#f69d3c, #3f87a6)"),
        (
            "radial-gradient(circle, red 10%, blue)",
            "radial-gradient(circle, red 10%, blue)",
        ),
        ("${primary}", "${primary}"),
    ],
)
def test_color__normalizes_valid_colors(text: str, expected: str) -> None:
    assert Color(text).value == expected


@pytest.mark.parametrize(
    "text",
    [
        "",
        "notacolor",
        "#abcd",
        "#aabbccdd",
        "#abcde",
        "#ggg",
        "rgb(1, 2, 3)",
        "linear-gradient(red",
        "linear-gradient()",
        "conic-gradient(red, blue)",
        "LINEAR-GRADIENT(red, blue)",
        "red; blue",
    ],
)
def test_color__rejects_invalid_colors(text: str) -> None:
    with pytest.raises(ValueError, match="is not a D2 color"):
        Color(text)


def test_color__is_written_quoted_unless_it_is_a_name() -> None:
    assert str(Color("red")) == "red"
    assert str(Color("#abc")) == '"#abc"'
    assert str(Color("linear-gradient(red, blue)")) == '"linear-gradient(red, blue)"'


def test_color__of_treats_empty_as_unset() -> None:
    assert Color.of(None) is None
    assert Color.of("") is None
    assert Color.of("red") == Color("red")
    assert Color.of(Color("red")) == Color("red")


def test_style__accepts_colors_and_strings() -> None:
    assert str(d2.Style(fill=d2.Color("#DBEAFE"))) == 'style: {\n  fill: "#dbeafe"\n}'
    assert str(d2.Style(stroke="dbeafe")) == 'style: {\n  stroke: "#dbeafe"\n}'
    assert str(d2.Style(fill="")) == ""


def test_style__rejects_invalid_colors() -> None:
    with pytest.raises(ValueError, match="is not a D2 color"):
        d2.Style(fill="not-a-color")
    with pytest.raises(ValueError, match="is not a D2 color"):
        d2.Style(font_color="#12")


@pytest.mark.parametrize(
    ("option", "build"),
    [
        ("opacity", lambda: d2.Style(opacity=-0.1)),
        ("opacity", lambda: d2.Style(opacity=1.5)),
        ("stroke_width", lambda: d2.Style(stroke_width=-1)),
        ("stroke_width", lambda: d2.Style(stroke_width=16)),
        ("stroke_dash", lambda: d2.Style(stroke_dash=11)),
        ("font_size", lambda: d2.Style(font_size=7)),
        ("font_size", lambda: d2.Style(font_size=101)),
        ("border_radius", lambda: d2.Style(border_radius=-1)),
    ],
)
def test_style__rejects_values_outside_the_d2_range(
    option: str, build: Callable[[], d2.Style]
) -> None:
    with pytest.raises(ValueError, match=option):
        build()


def test_style__accepts_the_ends_of_each_range() -> None:
    style = d2.Style(
        opacity=1, stroke_width=15, stroke_dash=10, font_size=8, border_radius=0
    )

    assert style.lines() == [
        "style: {",
        "  stroke-width: 15",
        "  opacity: 1",
        "  stroke-dash: 10",
        "  border-radius: 0",
        "  font-size: 8",
        "}",
    ]


def test_style__border_radius_parses_numbers_written_as_text() -> None:
    assert d2.Style(border_radius="12").border_radius == 12
    with pytest.raises(ValueError, match="invalid literal"):
        d2.Style(border_radius="round")


def test_shape__rejects_grid_and_position_values_outside_the_d2_range() -> None:
    with pytest.raises(ValueError, match="grid_rows"):
        d2.Shape(name="a", grid_rows=0)
    with pytest.raises(ValueError, match="grid_columns"):
        d2.Shape(name="a", grid_columns=0)
    with pytest.raises(ValueError, match="grid_gap"):
        d2.Shape(name="a", grid_gap=-1)
    with pytest.raises(ValueError, match="top"):
        d2.Shape(name="a", top=-1)
    with pytest.raises(ValueError, match="horizontal_gap"):
        d2.Shape(name="a", horizontal_gap=-1)


def test_config__rejects_negative_theme_ids() -> None:
    with pytest.raises(ValueError, match="theme_id"):
        d2.Config(theme_id=-1)
    with pytest.raises(ValueError, match="dark_theme_id"):
        d2.Config(dark_theme_id=-1)


def test_text__grows_the_pipe_count_so_the_content_cannot_close_it() -> None:
    assert Text("a | b", "md").pipes == 2
    assert Text("a || b", "md").pipes == 3
    assert Text("a || b", "md", pipes=5).pipes == 5
    assert Text("plain", "md").pipes == 1
    assert Text("a | b", "md").lines() == ["||md", "a | b", "||"]


def test_text__rejects_a_format_that_breaks_the_opening_line() -> None:
    with pytest.raises(ValueError, match="formatting"):
        Text("x", "m d")
    with pytest.raises(ValueError, match="formatting"):
        Text("x", "m|d")


def test_emit__indents_nested_fields() -> None:
    statements = (
        Field(
            Key("a"),
            Label("x"),
            (Field(Keyword("width"), 3), Field(Key("b"), None, (Field(Key("c")),))),
        ),
    )

    assert emit(statements) == ["a: x {", "  width: 3", "  b: {", "    c", "  }", "}"]
    assert emit(statements, 1)[0] == "  a: x {"


def test_emit__writes_inline_maps_on_one_line() -> None:
    field = Field(
        Key("id"),
        Label("int"),
        (Field(Keyword("constraint"), Array((Label("unique"), Label("not null")))),),
        inline=True,
    )

    assert emit((field,)) == ["id: int {constraint: [unique; not null]}"]


def test_emit__edges_keep_endpoints_as_given() -> None:
    edge = Edge(Keyword("a.b"), Direction.BOTH, Keyword("c.d"), Label("x: y"))

    assert emit((edge,)) == ['a.b <-> c.d: "x: y"']
    assert emit(
        (Edge(Keyword("a"), Direction.TO, Keyword("b"), None, (Comment("x"),)),)
    ) == [
        "a -> b: {",
        "  # x",
        "}",
    ]


def test_emit__comments_have_one_prefix_per_line() -> None:
    assert emit((Comment("one\ntwo"),)) == ["# one", "# two"]


def test_emit__block_fields_close_at_the_key_indent() -> None:
    field = BlockField(Keyword("label"), Text("a\nb", "md"))

    assert emit((field,), 1) == ["  label: |md", "    a", "    b", "  |"]


def test_one_or_array__writes_a_single_item_bare() -> None:
    assert str(one_or_array([Key("x")])) == "x"
    assert str(one_or_array([Key("x"), Key("shape")])) == '[x; "shape"]'


def test_variables__are_labels_and_quote_dollars() -> None:
    diagram = d2.Diagram(variables={"price": "$5", "n": 2})

    assert diagram.lines() == ["vars: {", '  price: "\\$5"', "  n: 2", "}"]


def test_shape__empty_strings_mean_unset_for_links_and_tooltips() -> None:
    shape = d2.Shape(name="a", icon="", near="", link="", tooltip="")

    assert shape.icon is None
    assert str(shape) == "a"


def test_connection__empty_label_means_no_label() -> None:
    connection = d2.Connection("a", "b", "")

    assert connection.label is None
    assert str(connection) == "a -> b"


def test_class_shape__quotes_member_names_that_are_keywords() -> None:
    shape = d2.ClassShape("A", fields=[d2.ClassField("label", "str")])

    assert str(shape) == 'A: {\n  shape: class\n  "label": "str"\n}'
