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

The format can be `"svg"` (the default), `"png"`, `"pdf"` or `"txt"`, which is ASCII art. You can also pass `layout="dagre" | "elk" | "tala"` and `theme=<id>`. A source string works in place of a diagram. If d2 fails, `d2.D2Error` is raised with the message from d2. PNG and PDF make d2 download a headless browser the first time you use them.

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
- [ ] Class shapes
- [ ] Comments

## Examples

See [`examples/`](examples/):

```sh
uv run python examples/simple_sql_schema.py
```

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
