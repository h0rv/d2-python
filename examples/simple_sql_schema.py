from pathlib import Path

from d2 import D2Error, render
from d2.diagram import Diagram
from d2.sql_table import SQLConstraint, SQLTable, create_foreign_key_connection

FILE_NAME = "simple_sql_schema"

# Create a new diagram
diagram = Diagram()

# Create Users table
users = SQLTable("users")
users.add_field("id", "int", SQLConstraint.PRIMARY_KEY)
users.add_field("name", "varchar(255)")

# Create Orders table
orders = SQLTable("orders")
orders.add_field("id", "int", SQLConstraint.PRIMARY_KEY)
orders.add_field("user_id", "int", SQLConstraint.FOREIGN_KEY)
orders.add_field("total", "decimal(10,2)")

# Create connection
fk = create_foreign_key_connection("orders", "user_id", "users", "id")

# Add tables and connections to the diagram
diagram.add_shape(users)
diagram.add_shape(orders)
diagram.add_connection(fk)

# Write the diagram to a file
d2_path = Path(f"{FILE_NAME}.d2")
d2_path.write_text(str(diagram), encoding="utf-8")

print(f"D2 diagram file created: {d2_path}")
print(str(diagram))

try:
    svg_path = Path(f"{FILE_NAME}.svg")
    svg_path.write_bytes(render(diagram, layout="elk"))
    print(f"SVG diagram generated: {svg_path.resolve()}")
except (D2Error, FileNotFoundError) as e:
    print(f"Error generating SVG: {e}")
