from d2.connection import Direction
from d2.diagram import Diagram
from d2.shape import Shape
from d2.sql_table import (
    SQLConstraint,
    SQLField,
    SQLFieldSpec,
    SQLTable,
    create_foreign_key_connection,
)
from d2.style import Style


def test_sql_field_simple() -> None:
    """Test creating a simple SQL field without constraints."""
    field = SQLField("name", "varchar(255)")
    assert field.to_d2_format() == "name: varchar(255)"


def test_sql_field_with_constraint() -> None:
    """Test creating a SQL field with a single constraint."""
    field = SQLField("id", "int", SQLConstraint.PRIMARY_KEY)
    assert field.to_d2_format() == "id: int {constraint: primary_key}"


def test_sql_field_with_string_constraint() -> None:
    """Test creating a SQL field with a string constraint."""
    field = SQLField("status", "varchar(50)", "not null")
    assert field.to_d2_format() == "status: varchar(50) {constraint: not null}"


def test_sql_field_with_multiple_constraints() -> None:
    """Test creating a SQL field with multiple constraints."""
    field = SQLField("email", "varchar(255)", [SQLConstraint.UNIQUE, "not null"])
    assert (
        field.to_d2_format() == "email: varchar(255) {constraint: [unique; not null]}"
    )


def test_sql_table_empty() -> None:
    """Test creating an empty SQL table."""
    table = SQLTable("users")
    assert str(table) == "users: {\n  shape: sql_table\n}"


def test_sql_table_with_fields() -> None:
    """Test creating a SQL table with fields."""
    table = SQLTable("users")
    table.add_field("id", "int", SQLConstraint.PRIMARY_KEY)
    table.add_field("name", "varchar(255)")
    table.add_field("email", "varchar(255)", SQLConstraint.UNIQUE)

    expected_lines = [
        "users: {",
        "  shape: sql_table",
        "  id: int {constraint: primary_key}",
        "  name: varchar(255)",
        "  email: varchar(255) {constraint: unique}",
        "}",
    ]
    expected = "\n".join(expected_lines)

    assert str(table) == expected


def test_sql_table_with_fields_dict() -> None:
    """Test creating a SQL table with fields provided as a dictionary."""
    fields: dict[str, str | SQLFieldSpec] = {
        "id": {"type": "int", "constraint": SQLConstraint.PRIMARY_KEY},
        "name": "varchar(255)",
        "email": {"type": "varchar(255)", "constraint": SQLConstraint.UNIQUE},
    }

    table = SQLTable("users", fields=fields)

    expected_lines = [
        "users: {",
        "  shape: sql_table",
        "  id: int {constraint: primary_key}",
        "  name: varchar(255)",
        "  email: varchar(255) {constraint: unique}",
        "}",
    ]
    expected = "\n".join(expected_lines)

    assert str(table) == expected


def test_sql_table_with_label_and_style() -> None:
    """Test creating a SQL table with a label and style."""

    table = SQLTable("users", label="User Table", style=Style(fill="lightblue"))
    table.add_field("id", "int", SQLConstraint.PRIMARY_KEY)

    expected_lines = [
        "users: User Table {",
        "  shape: sql_table",
        "  id: int {constraint: primary_key}",
        "  style: {",
        "    fill: lightblue",
        "  }",
        "}",
    ]
    expected = "\n".join(expected_lines)

    assert str(table) == expected


def test_foreign_key_connection() -> None:
    """Test creating a foreign key connection between tables."""
    connection = create_foreign_key_connection("orders", "user_id", "users", "id")

    assert connection.shape_1 == "orders.user_id"
    assert connection.shape_2 == "users.id"
    assert connection.direction == Direction.TO
    assert str(connection) == "orders.user_id -> users.id"


def test_foreign_key_connection_with_label() -> None:
    """Test creating a foreign key connection with a label."""
    connection = create_foreign_key_connection(
        "orders", "user_id", "users", "id", "belongs to"
    )

    assert connection.label == "belongs to"
    assert str(connection) == "orders.user_id -> users.id: belongs to"


def test_complex_sql_table_relationship() -> None:
    """Test creating multiple SQL tables with relationships."""
    # Create tables
    users = SQLTable("users")
    users.add_field("id", "int", SQLConstraint.PRIMARY_KEY)
    users.add_field("name", "varchar(255)")

    orders = SQLTable("orders")
    orders.add_field("id", "int", SQLConstraint.PRIMARY_KEY)
    orders.add_field("user_id", "int", SQLConstraint.FOREIGN_KEY)
    orders.add_field("total", "decimal(10,2)")

    # Create connection
    fk = create_foreign_key_connection("orders", "user_id", "users", "id")

    diagram = Diagram()
    diagram.add_shape(users)
    diagram.add_shape(orders)
    diagram.add_connection(fk)

    expected_lines = [
        "users: {",
        "  shape: sql_table",
        "  id: int {constraint: primary_key}",
        "  name: varchar(255)",
        "}",
        "orders: {",
        "  shape: sql_table",
        "  id: int {constraint: primary_key}",
        "  user_id: int {constraint: foreign_key}",
        "  total: decimal(10,2)",
        "}",
        "orders.user_id -> users.id",
    ]
    expected = "\n".join(expected_lines)

    assert str(diagram) == expected


def test_nested_sql_tables() -> None:
    """Test creating nested SQL tables within a container."""
    # Create container

    cloud = Shape("cloud", label="Cloud Infrastructure")

    # Create SQL tables
    disks = SQLTable("disks")
    disks.add_field("id", "int", SQLConstraint.PRIMARY_KEY)

    blocks = SQLTable("blocks")
    blocks.add_field("id", "int", SQLConstraint.PRIMARY_KEY)
    blocks.add_field("disk", "int", SQLConstraint.FOREIGN_KEY)
    blocks.add_field("blob", "blob")

    # Create connection
    fk = create_foreign_key_connection("blocks", "disk", "disks", "id")

    # Add tables to container
    cloud.add_shape(disks)
    cloud.add_shape(blocks)
    cloud.add_connection(fk)

    expected_lines = [
        "cloud: Cloud Infrastructure {",
        "  disks: {",
        "    shape: sql_table",
        "    id: int {constraint: primary_key}",
        "  }",
        "  blocks: {",
        "    shape: sql_table",
        "    id: int {constraint: primary_key}",
        "    disk: int {constraint: foreign_key}",
        "    blob: blob",
        "  }",
        "  blocks.disk -> disks.id",
        "}",
    ]
    expected = "\n".join(expected_lines)

    assert str(cloud) == expected
