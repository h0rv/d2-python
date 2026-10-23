# Examples

Each script builds one diagram and writes it next to where you run it. Install the d2 binary with the `bin` extra, then run any example:

```bash
uv sync --extra bin
uv run python examples/shapes.py
```

| Example | What it shows |
| --- | --- |
| [basic.py](basic.py) | Shapes, labels and a connection |
| [shapes.py](shapes.py) | Shape types such as cylinder, queue and person, and icons |
| [containers.py](containers.py) | Shapes inside shapes, and connections to nested shapes with dotted paths |
| [styles.py](styles.py) | Fill, stroke, font, bold, opacity, 3d, shadow and border radius |
| [connections.py](connections.py) | Labels, directions, styles and arrowheads, including crow's foot |
| [tooltips_and_links.py](tooltips_and_links.py) | Tooltips on shapes and connections, and shape links |
| [text_blocks.py](text_blocks.py) | Markdown and code text inside a shape |
| [grids.py](grids.py) | Grid layout with columns and gap |
| [classes.py](classes.py) | Reusable style classes |
| [sql_tables.py](sql_tables.py) | SQL tables with constraints and a foreign key |
| [uml_classes.py](uml_classes.py) | UML class shapes with fields, methods and inheritance |
| [boards.py](boards.py) | Layers, scenarios and steps, rendering the root board and one layer |
| [config.py](config.py) | Layout engine, theme, direction and sketch mode through `vars` |
| [ascii.py](ascii.py) | ASCII output printed with `d2.render(diagram, "txt")` |
| [raw_and_validation.py](raw_and_validation.py) | Raw D2 for globs and connection references, `d2.validate` and `d2.format` |
| [labels_and_positions.py](labels_and_positions.py) | Markdown labels on shapes and connections, `label_near`, `icon_near`, connection icons and links |
| [fixed_positions.py](fixed_positions.py) | `top` and `left` positions (tala) and grid `vertical_gap` and `horizontal_gap` |
| [c4_and_sequence.py](c4_and_sequence.py) | The `c4-person` shape and a sequence diagram |
| [variables_and_legend.py](variables_and_legend.py) | `variables` with `${name}` substitution, gradients, a legend and a board label |
| [render_options.py](render_options.py) | Sketch, dark theme, pad, scale, salt, gif and pptx output, ASCII mode |
