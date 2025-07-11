# py-d2

![Banner](docs/images/banner.png)

An unofficial, fully typed python interface for building [.d2](https://github.com/terrastruct/d2) diagram files in python.

## Installation

```bash
pip install d2-python
```

## Usage

```python
import d2

shapes = [
    d2.Shape(name="shape_name1", style=d2.Style(fill="red")),
    d2.Shape(name="shape_name2", style=d2.Style(fill="blue"))]
connections = [
    d2.Connection(shape_1="shape_name1", shape_2="shape_name2")
]

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

See the [tests](/tests/test_py_d2) for more detailed usage examples.


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

`examples/`

```sh
uv run python examples/<example>.py
```

SQL Table:

```sh
uv run python example/simple_sql_schema.py
# Open diagram:
open simple_sql_schema.svg
```



## Development
### Prerequisite

- [Python 3.8+](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/)
- [pre-commit](https://pre-commit.com/)

### Installation

following the steps below to setup the project:

```bash

```bash
# Clone the repository
git clone git@github.com:h0rv/d2-python.git && cd d2-python

# Install all dependencies
uv sync --all-extras --dev

# install git hook scripts for development
pre-commit install

# Install dev dependencies for development
uv sync --dev
# Only install required dependencies for production
uv sync
```

### Usage

There are some useful commands for development:

```bash
# Run the example
uv run example

# Code test
uv run pytest -s

# Lint and format with ruff
uv run ruff check ./src

# Format code with ruff
uv run ruff format ./src

# Check with mypy
uv run mypy ./src

# Run coverage test
uv run pytest -s --cov=./src --cov-report=term-missing
```
