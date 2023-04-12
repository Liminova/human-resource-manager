from __future__ import annotations
import re
import sys
import textwrap
from datetime import datetime
from option import Result, Ok, Err
from pydantic import BaseModel, Field
from database import PyObjectId
from bson.objectid import ObjectId

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from .attendance_check import Attendance
from .benefits import BenefitPlan
from .payroll import Payroll
from .performance import Performance

class Employee(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(default_factory=str)
    dob: datetime = Field(default_factory=datetime.now)
    email: str = Field(default_factory=str)
    employee_id: str = Field(default_factory=str)
    phone: str = Field(default_factory=str)
    department_id: str = Field(default_factory=str)
    benefits: list[BenefitPlan] = Field(default_factory=list)
    payroll: Payroll = Field(default_factory=Payroll)
    attendance: Attendance = Field(default_factory=Attendance)
    performance: Performance = Field(default_factory=Performance)

    def set_name(self, name: str) -> Result[Self, str]:
        if name == "":
            return Err("Name cannot be empty!")
        if any(char.isdigit() for char in name):
            return Err("Name cannot contain numbers!")
        self.name = name
        return Ok(self)

    def set_dob(self, dob: str) -> Result[Self, str]:
        try:
            dob = datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            return Err("Invalid date of birth format!")
        self.dob = dob
        return Ok(self)

    def set_email(self, email: str = "") -> Result[Self, str]:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, email):
            return Err("Invalid email format!")
        self.email = email
        return Ok(self) if email else Err("Email cannot be empty!")

    def set_id(self, id: str) -> Result[Self, str]:
        if id == "":
            return Err("ID cannot be empty!")
        self.employee_id = id
        return Ok(self)

    def set_phone(self, phone: str) -> Result[Self, str]:
        if any(char.isalpha() for char in phone):
            return Err("Phone number cannot contain letters!")
        self.phone = phone
        return Ok(self) if phone else Err("Phone number cannot be empty!")

    def set_payroll(self, payroll: Payroll) -> Result[Self, str]:
        self.payroll = payroll
        return Ok(self)

    def set_performance(self, performance: Performance) -> Result[Self, str]:
        self.performance = performance
        return Ok(self)

    def request_enrollment(self, benefit: BenefitPlan) -> Result[Self, str]:
        if benefit in self.benefits:
            return Err("Employee is already enrolled in this plan!")
        # request enrollment
        benefit.add_pending_enrollment_request(self)
        return Ok(self)

    def __str__(self) -> str:
        data = textwrap.dedent(f"""\
            - Name: {self.name}
            - DoB: {self.dob}
            - ID: {self.employee_id}
            - Phone: {self.phone}
            - Department ID: {self.department_id}
            - Benefit plans:
        """)
        for (i, benefit) in enumerate(self.benefits, 1):
            data += f"{i}. {benefit.name}\n"
        return data

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
