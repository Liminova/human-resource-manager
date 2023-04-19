from __future__ import annotations
import sys
import textwrap
from option import Result, Ok, Err
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from frontend.helpers import styling

from database.pyobjectid import PyObjectId

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from .employee import Employee


class BenefitPlan(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(default_factory=str)
    description: str = Field(default_factory=str)
    cost: float = Field(default_factory=float)
    enrolled_employees: list[Employee] = Field(default_factory=list)
    pending_requests: list[Employee] = Field(default_factory=list)

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
        data = textwrap.dedent(
            f"""\
            {styling('Name', self.name)}
            {styling('Description', self.description)}
            {styling('Cost', self.cost)}
            {styling('Enrolled employees', len(self.enrolled_employees))}
        """
        )
        for i, employee in enumerate(self.enrolled_employees, 1):
            data += f"  {styling(i, employee.name)} ({employee.employee_id})\n"
        return data

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
