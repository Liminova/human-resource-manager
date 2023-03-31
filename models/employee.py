from __future__ import annotations
import re
import sys
import textwrap
from datetime import datetime
from option import Result, Ok, Err

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from .attendance_check import Attendance
from .benefits import BenefitPlan
from .department import Department
from .payroll import Payroll
from .performance import Performance

# NOTE: possible abstraction: split name and id into its own Entity class or
# something, though i don't like that approach very much tbh - Rylie

class Employee:
    def __init__(self) -> None:
        self.__name = ""
        self.__dob: datetime = None
        self.__email = ""
        self.__id = ""
        self.__phone = ""
        self.__department = None
        self.__benefits = []
        self.__payroll = None
        self.__attendance = Attendance() # inside contains lists of attendance
        self.__performance = Performance() # inside contains lists of sales

    @property
    def name(self) -> str:
        return self.__name

    @property
    def dob(self) -> datetime:
        return self.__dob

    @property
    def email(self) -> str:
        return self.__email

    @property
    def id(self) -> str:
        return self.__id

    @property
    def phone(self) -> str:
        return self.__phone

    @property
    def department(self) -> Department | None:
        return self.__department

    @property
    def benefits(self) -> list[BenefitPlan]:
        return self.__benefits

    @property
    def payroll(self) -> Payroll | None:
        return self.__payroll

    @property
    def attendance(self) -> Attendance:
        return self.__attendance

    @property
    def performance(self) -> Performance:
        return self.__performance

    def set_name(self, name: str) -> Result[Self, str]:
        if name == "":
            return Err("Name cannot be empty!")
        if any(char.isdigit() for char in name):
            return Err("Name cannot contain numbers!")
        self.__name = name
        return Ok(self)

    def set_dob(self, dob: str) -> Result[Self, str]:
        try:
            dob = datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            return Err("Invalid date of birth format!")
        self.__dob = dob
        return Ok(self)

    def set_email(self, email: str = "") -> Result[Self, str]:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, email):
            return Err("Invalid email format!")
        self.__email = email
        return Ok(self) if email else Err("Email cannot be empty!")

    def set_id(self, id: str = "") -> Result[Self, str]:
        self.__id = id
        return Ok(self) if id else Err("ID cannot be empty!")

    def set_phone(self, phone: str = "") -> Result[Self, str]:
        if any(char.isalpha() for char in phone):
            return Err("Phone number cannot contain letters!")
        self.__phone = phone
        return Ok(self) if phone else Err("Phone number cannot be empty!")

    def set_department(self, department: Department) -> Result[Self, str]:
        self.__department = department
        return Ok(self)

    def set_payroll(self, payroll: Payroll) -> Result[Self, str]:
        self.__payroll = payroll
        return Ok(self)

    def set_performance(self, performance: Performance) -> Result[Self, str]:
        self.__performance = performance
        return Ok(self)

    def is_enrolled_in_plan(self, benefit: BenefitPlan) -> bool:
        return benefit in self.__benefits

    def __str__(self) -> str:
        data = textwrap.dedent(f"""\
            - Name: {self.__name}
            - DoB: {self.__dob}
            - ID: {self.__id}
            - Phone: {self.__phone}
            - Department: {self.__department}
            - Benefit plans:
        """)
        for (i, benefit) in enumerate(self.__benefits, 1):
            data += f"{i}. {benefit.name}\n"
        return data
