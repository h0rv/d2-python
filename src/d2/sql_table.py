from __future__ import annotations

from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from d2.connection import Connection
from d2.connection import Direction
from d2.shape import Shape
from d2.shape import ShapeType


class SQLConstraint(Enum):
    PRIMARY_KEY = "primary_key"
    FOREIGN_KEY = "foreign_key"
    UNIQUE = "unique"


class SQLField:
    def __init__(
        self,
        name: str,
        data_type: str,
        constraint: Optional[Union[SQLConstraint, str, List[Union[SQLConstraint, str]]]] = None,
    ):
        self.name = name
        self.data_type = data_type

        # Handle constraint(s)
        if constraint is None:
            self.constraints = []
        elif isinstance(constraint, list):
            self.constraints = constraint
        else:
            self.constraints = [constraint]

    def to_d2_format(self) -> str:
        """Convert the field to D2 format."""
        if not self.constraints:
            return f"{self.name}: {self.data_type}"

        constraints_str = "; ".join([c.value if isinstance(c, SQLConstraint) else c for c in self.constraints])

        if len(self.constraints) == 1:
            constraint_part = constraints_str
        else:
            constraint_part = f"[{constraints_str}]"

        return f"{self.name}: {self.data_type} {{constraint: {constraint_part}}}"


class SQLTable(Shape):
    def __init__(
        self,
        name: str,
        fields: Optional[Dict[str, Union[str, Dict[str, Any]]]] = None,
        label: Optional[str] = None,
        style: Optional[Any] = None,
        icon: Optional[str] = None,
        near: Optional[str] = None,
        link: Optional[str] = None,
    ):
        super().__init__(
            name=name,
            label=label,
            shape=ShapeType.sql_table,
            style=style,
            icon=icon,
            near=near,
            link=link,
        )

        self.fields: List[SQLField] = []

        # Process fields if provided
        if fields:
            for field_name, field_info in fields.items():
                if isinstance(field_info, str):
                    # Simple case: just a type
                    self.add_field(field_name, field_info)
                elif isinstance(field_info, dict):
                    # Complex case: type and constraints
                    field_type = field_info.get("type", "")
                    constraint = field_info.get("constraint", None)
                    self.add_field(field_name, field_type, constraint)

    def add_field(
        self,
        name: str,
        data_type: str,
        constraint: Optional[Union[SQLConstraint, str, List[Union[SQLConstraint, str]]]] = None,
    ) -> SQLField:
        """Add a field to the SQL table."""
        field = SQLField(name, data_type, constraint)
        self.fields.append(field)
        return field

    def lines(self) -> List[str]:
        """Generate D2 lines for the SQL table."""
        # Get the base properties from parent class
        properties = []

        # Add shape property
        if self.shape:
            properties.append(f"shape: {self.shape.value}")

        # Add fields
        for field in self.fields:
            properties.append(field.to_d2_format())

        # Add other properties
        if self.near:
            properties.append(f"near: {self.near}")

        if self.link:
            properties.append(f"link: {self.link}")

        if self.style:
            properties.extend(self.style.lines())

        if self.icon:
            properties.append(f"icon: {self.icon}")

        # Add child shapes and connections
        shapes = [shape.lines() for shape in self.shapes]
        connections = [connection.lines() for connection in self.connections]

        for shape_lines in shapes:
            properties.extend(shape_lines)

        for connection_lines in connections:
            properties.extend(connection_lines)

        # Create the final lines
        from d2.helpers import add_label_and_properties

        lines = add_label_and_properties(self.name, self.label, properties)

        return lines


def create_foreign_key_connection(
    source_table: str,
    source_field: str,
    target_table: str,
    target_field: str,
    label: Optional[str] = None,
) -> Connection:
    """Create a foreign key connection between two tables."""
    source = f"{source_table}.{source_field}"
    target = f"{target_table}.{target_field}"
    return Connection(source, target, label, Direction.TO)
