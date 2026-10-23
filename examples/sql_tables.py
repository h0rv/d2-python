from pathlib import Path

import d2
from d2.sql_table import SQLConstraint, SQLTable, create_foreign_key_connection


def main() -> None:
    users = SQLTable("users")
    users.add_field("id", "int", SQLConstraint.PRIMARY_KEY)
    users.add_field("email", "varchar(255)", SQLConstraint.UNIQUE)

    orders = SQLTable("orders")
    orders.add_field("id", "int", SQLConstraint.PRIMARY_KEY)
    orders.add_field("user_id", "int", SQLConstraint.FOREIGN_KEY)
    orders.add_field("total", "decimal(10,2)")

    diagram = d2.Diagram(
        shapes=[users, orders],
        connections=[create_foreign_key_connection("orders", "user_id", "users", "id")],
    )
    Path("sql_tables.svg").write_bytes(d2.render(diagram, layout="elk"))


if __name__ == "__main__":
    main()
