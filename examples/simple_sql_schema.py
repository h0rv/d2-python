import os
import subprocess

from py_d2.diagram import D2Diagram
from py_d2.sql_table import SQLConstraint, SQLTable, create_foreign_key_connection

FILE_NAME = "simple_sql_schema"

# Create a new diagram
diagram = D2Diagram()

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
with open(f"{FILE_NAME}.d2", "w") as f:
    f.write(str(diagram))

print(f"D2 diagram file created: {FILE_NAME}.d2")
print(str(diagram))

try:
    subprocess.run(["d2", "--layout", "elk", f"{FILE_NAME}.d2", f"{FILE_NAME}.svg"], check=True)
    print(f"SVG diagram generated: {os.path.abspath(f'{FILE_NAME}.svg')}")
except Exception as e:
    print(f"Error generating SVG: {e}")
