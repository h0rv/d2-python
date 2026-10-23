# d2-python

![Banner](docs/images/banner.png)

An unofficial, fully typed python interface for building [.d2](https://github.com/terrastruct/d2) diagram files in python.

This is a maintained hard fork of [MrBlenny/py-d2](https://github.com/MrBlenny/py-d2), which is no longer updated.
Coming from py-d2: import `d2` instead of `py_d2`, and drop the `D2` prefix from class names, such as `d2.Shape` for `py_d2.D2Shape`.

## Installation

```bash
pip install d2-python
```

To render diagrams from Python without installing the d2 command yourself, add the `bin` extra, which brings in the official d2 binary:

```bash
pip install 'd2-python[bin]'
uv add 'd2-python[bin]'
```

## Usage

```python
import d2

shapes = [
    d2.Shape(name="shape_name1", style=d2.Style(fill="red")),
    d2.Shape(name="shape_name2", style=d2.Style(fill="blue")),
]
connections = [d2.Connection(shape_1="shape_name1", shape_2="shape_name2")]

diagram = d2.Diagram(shapes=shapes, connections=connections)

with open("graph.d2", "w", encoding="utf-8") as f:
    f.write(str(diagram))
```

produces the following graph.d2 file:

```d2

shape_name1: {
  style: {
    fill: red
  }
}
shape_name2: {
  style: {
    fill: blue
  }
}
shape_name1 -> shape_name2

```

This can be rendered using `d2 graph.d2 graph.svg && open graph.svg` or [https://play.d2lang.com/](https://play.d2lang.com/) to produce

![example graph](/docs/images/d2.svg)

Pick a shape type with `shape=d2.ShapeType.<name>` and add a tooltip with `tooltip=`:

```python
db = d2.Shape(
    name="db",
    shape=d2.ShapeType.cylinder,
    tooltip="Primary database",
)
```

A tooltip is shown when you hover the shape in the rendered SVG. Connections take `tooltip=` too.

## Rendering

`d2.render` runs the d2 command and returns the image as bytes. It uses the binary from `d2-bin` when that is installed, and otherwise looks for `d2` on your PATH.

```python
import d2

diagram = d2.Diagram(
    shapes=[d2.Shape(name="a"), d2.Shape(name="b")],
    connections=[d2.Connection(shape_1="a", shape_2="b")],
)

with open("graph.svg", "wb") as f:
    f.write(d2.render(diagram))

print(d2.render(diagram, "txt").decode())
```

The format can be `"svg"` (the default), `"png"`, `"pdf"`, `"gif"`, `"pptx"` or `"txt"`, which is ASCII art. You can also pass `layout="dagre" | "elk" | "tala"` and `theme=<id>`. Other keyword options are `dark_theme`, `sketch`, `pad`, `scale`, `center`, `omit_version`, `no_xml_tag`, `salt`, `animate_interval`, `ascii_mode` and `timeout`. An option you leave out is not sent to d2. For a diagram with layers, scenarios or steps, `target=` picks the board: the root by default, or a path such as `"layers.detail"`. A source string works in place of a diagram. If d2 fails, `d2.D2Error` is raised with the message from d2. d2 0.9 renders PNG, PDF, GIF and PPTX itself. Older d2 versions download a headless browser for PNG and PDF the first time.

## Validating and formatting

`d2.validate` checks D2 source with `d2 validate` and raises `d2.D2Error` with d2's message when the source is wrong. `d2.format` returns the source formatted by `d2 fmt`. Both take a `Diagram` or a string, so they suit code or an LLM that writes D2 text and needs to check it.

```python
import d2

d2.validate("a -> b")

try:
    d2.validate("a -> {")
except d2.D2Error as error:
    print(error)

print(d2.format("a->b"))
```

`validate` checks syntax and meaning, but does not lay the diagram out. Some errors, such as `top` and `left` with the dagre layout, only show when you render.

See the [tests](/tests/test_d2) for more detailed usage examples.


## Supported Features

- [x] Shapes (nodes)
- [x] Connections (links)
- [x] Styles
- [x] Containers (nodes/links in nodes)
- [x] Shapes in shapes
- [x] Arrow directions
- [x] Markdown / block strings / code in shapes
- [x] Icons in shapes
- [x] Support for empty labels
- [x] Shape links
- [x] SQL table shapes
- [x] Layers
- [x] Class shapes
- [x] Comments
- [x] Automatic quoting of names and labels
- [x] More style options (font, bold, italic, fill pattern and others)
- [x] Connection styles, arrowheads and tooltips
- [x] Shape tooltips, size, grids, direction and classes
- [x] Diagram direction, classes and `d2-config` vars
- [x] Scenarios and steps
- [x] `d2.validate` and `d2.format` through the d2 command
- [x] Glob shapes such as `Shape(name="*")` to style every shape
- [x] Markdown, LaTeX or code as shape and connection labels (`label=d2.Text(...)`)
- [x] `label_near` and `icon_near` positions, `top` and `left`, grid `vertical_gap` and `horizontal_gap`
- [x] Connection icons, links and classes
- [x] `c4-person` shape and sequence diagrams
- [x] Variables (`variables=`) with `${name}` substitution, and gradient fills
- [x] Legends and board labels
- [x] More render options and gif and pptx output

## More features

Names and labels that D2 cannot read bare (such as `a.b`, `x: y`, or the keyword `shape`) are quoted for you. Connection endpoints are written as given, so they can be dotted paths.
Style values you set are always written, even `0` or `False`. `None` means unset.

```python
import d2

diagram = d2.Diagram(
    comments=["Generated by d2-python"],
    direction="right",
    vars=d2.Config(layout_engine="tala", theme_id=4, sketch=True),
    classes={"hot": d2.Style(fill="orange", bold=True)},
    shapes=[
        d2.Shape(name="api", tooltip="Public API", width=200, classes=["hot"]),
        d2.Shape(
            name="grid", grid_columns=2, shapes=[d2.Shape(name="a"), d2.Shape(name="b")]
        ),
        d2.ClassShape(
            "Animal",
            fields=[d2.ClassField("name", "string", "+")],
            methods=[d2.ClassMethod("eat", "food string", "bool", "+")],
        ),
    ],
    connections=[
        d2.Connection(
            "api",
            "grid",
            label="calls",
            style=d2.Style(stroke="blue", animated=True),
            target_arrowhead=d2.Arrowhead(d2.ArrowheadShape.DIAMOND, filled=True),
            tooltip="HTTP",
        )
    ],
    scenarios=[
        d2.Layer(name="degraded", diagram=d2.Diagram(shapes=[d2.Shape(name="api")]))
    ],
    steps=[
        d2.Layer(name="step_one", diagram=d2.Diagram(shapes=[d2.Shape(name="api")]))
    ],
)
```

Use `layers`, `scenarios` and `steps` for other boards. Use `comments` (or `add_comment`) for `# comment` lines at the top of the file.

## Examples

Runnable examples for every feature are in [`examples/`](examples/README.md).

## Development

Requires [uv](https://docs.astral.sh/uv/).

```bash
git clone git@github.com:h0rv/d2-python.git && cd d2-python
uv sync

uv run pytest
uv run ruff check
uv run ruff format
uv run ty check
```
