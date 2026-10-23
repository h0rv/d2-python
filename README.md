# d2-python

![Banner](docs/images/banner.png)

An unofficial, fully typed python interface for building [.d2](https://github.com/terrastruct/d2) diagram files in python.

This is a maintained hard fork of [MrBlenny/py-d2](https://github.com/MrBlenny/py-d2), which is no longer updated.
Coming from py-d2: import `d2` instead of `py_d2`, and drop the `D2` prefix from class names, such as `d2.Shape` for `py_d2.D2Shape`.

## Installation

```bash
pip install d2-python
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
