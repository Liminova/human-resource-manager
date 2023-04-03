from __future__ import annotations
import sys
import textwrap
from option import Result, Ok, Err
from pydantic import BaseModel

if sys.version_info >= (3, 11):
    from typing import Self, TYPE_CHECKING
else:
    from typing_extensions import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from .employee import Employee

class BenefitPlan(BaseModel):
    name = ""
    description = ""
    cost = 0.0
    enrolled_employees: list[Employee] = []
    pending_requests: list[Employee] = []

    def set_name(self, name: str = "") -> Result[Self, str]:
        self.name = name
        return Ok(self) if name else Err("Name cannot be empty.")

    def set_description(self, description: str = "") -> Result[Self, str]:
        self.description = description
        return Ok(self) if description else Err("Description cannot be empty.")

    def set_cost(self, cost: float = 0.0) -> Result[Self, str]:
        self.cost = cost
        return Ok(self) if cost else Err("Cost cannot be empty.")

    def add_pending_enrollment_request(self, employee: Employee) -> Result[Self, str]:
        if employee in self.pending_requests:
            return Err("Employee is already pending enrollment.")
        self.pending_requests.append(employee)
        return Ok(self)

    def __str__(self) -> str:
        data = textwrap.dedent(f"""\
            - Name: {self.name}
            - Description: {self.description}
            - Cost: {self.cost}
            - Enrolled employees:
        """)
        for (i, employee) in enumerate(self.enrolled_employees, 1):
            data += f"{i}: {employee}\n"
        return data

    class Config:
        arbitrary_types_allowed = True
