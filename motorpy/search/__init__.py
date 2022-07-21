"Advanced Search"
from typing import Any, Set
import datetime

OPS = {
    "eq",
    "ne",
    "gt",
    "gte",
    "lt",
    "lte",
    "like",
    "ilike"
}

class Search:
    "Advanced Search"
    def __init__(self, value: Any, operator: str = "eq") -> None:
        if operator not in OPS:
            raise ValueError(f"Invalid operator: {operator} - can be one of {OPS}")
        self.value = value
        self.operator = operator
    
    def _get_value_str(self) -> str:
        "Checks the type and returns the value as a string. Datetime is converted to ISO format."
        if isinstance(self.value, datetime.datetime):
            return self.value.isoformat()
        if isinstance(self.value, datetime.date):
            return self.value.isoformat()
        if isinstance(self.value, datetime.time):
            return self.value.isoformat()
        return str(self.value)
    
    @property
    def available_operators(self) -> Set[str]:
        "Returns a list of available operators for the given value type."
        return OPS
    
    def __str__(self) -> str:
        return f"{self.operator}.{self._get_value_str()}"
    
    def __repr__(self) -> str:
        return f"Search({self.value}, {self.operator})"
    
    