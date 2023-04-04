from __future__ import annotations
import re
import sys
import textwrap
from datetime import datetime
from option import Result, Ok, Err
from pydantic import BaseModel

if sys.version_info >= (3, 11):
    from typing import Self, TYPE_CHECKING
else:
    from typing_extensions import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from .company import Company

from .attendance_check import Attendance
from .benefits import BenefitPlan
from .department import Department
from .payroll import Payroll
from .performance import Performance

# NOTE: possible abstraction: split name and id into its own Entity class or
# something, though i don't like that approach very much tbh - Rylie

class Employee(BaseModel):
    name = ""
    dob: datetime | None = None
    email = ""
    id = ""
    phone = ""
    department: Department | None = None
    benefits: list[BenefitPlan] = []
    payroll: Payroll | None = None
    attendance: Attendance = Attendance()
    performance: Performance = Performance()

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

    def set_id(self, id: str, company: Company) -> Result[Self, str]:
        if id == "":
            return Err("ID cannot be empty!")
        if company.is_id_taken(id):
            return Err("ID is already taken!")
        self.id = id
        return Ok(self)

    def set_phone(self, phone: str = "") -> Result[Self, str]:
        if any(char.isalpha() for char in phone):
            return Err("Phone number cannot contain letters!")
        self.phone = phone
        return Ok(self) if phone else Err("Phone number cannot be empty!")

    def set_department(self, department: Department) -> Result[Self, str]:
        self.department = department
        return Ok(self)

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
            - ID: {self.id}
            - Phone: {self.phone}
            - Department: {self.department}
            - Benefit plans:
        """)
        for (i, benefit) in enumerate(self.benefits, 1):
            data += f"{i}. {benefit.name}\n"
        return data

    class Config:
        arbitrary_types_allowed = True
