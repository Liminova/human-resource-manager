from __future__ import annotations
import re
import sys
import textwrap
from datetime import datetime
from option import Result, Ok, Err

if sys.version_info >= (3, 11):
    from typing import Self, TYPE_CHECKING
else:
    from typing_extensions import Self, TYPE_CHECKING

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
        self.__dob = ""
        self.__email = ""
        self.__id = ""
        self.__phone = ""
        # TODO: think of some way to decouple department members list and
        # members being a part of departments, it's kinda a circle dependency
        # rn. - Rylie
        self.__department = Department()
        self.__benefits = []
        self.__payroll = Payroll()
        self.__attendance = Attendance()
        self.__performance = Performance()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def dob(self) -> str:
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
    def department(self) -> Department:
        return self.__department

    @property
    def benefits(self) -> list:
        return self.__benefits

    @property
    def payroll(self) -> Payroll:
        return self.__payroll

    @property
    def attendance(self) -> Attendance:
        return self.__attendance

    @property
    def performance(self) -> Performance:
        return self.__performance

    def name(self, name: str) -> Result[Self, str]:
        if name == "":
            return Err("Name cannot be empty!")
        if any(char.isdigit() for char in name):
            return Err("Name cannot contain numbers!")
        self.__name = name
        return Ok(self)

    def dob(self, dob: str) -> Result[Self, str]:
        if (len(dob) != 10) or (dob[4] != "-" or dob[7] != "-"):
            return Err("Invalid date of birth format!")

        year, month, day = dob.split("-")
        year, month, day = int(year), int(month), int(day)

        is_leap_year = (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
        valid_day = month in (1, 3, 5, 7, 8, 10, 12) and 1 <= day <= 31 or \
            month in (4, 6, 9, 11) and 1 <= day <= 30 or \
            month == 2 and 1 <= day <= 29 and is_leap_year or \
            month == 2 and 1 <= day <= 28 and not is_leap_year
        valid_month = 1 <= month <= 12
        valid_year = 1900 <= year <= datetime.now().year

        if not valid_day or not valid_month or not valid_year:
            return Err("Invalid date of birth format!")

        self.__dob = dob
        return Ok(self)

    def set_email(self, email: str) -> Result[Self, str]:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, email):
            return Err("Invalid email format!")
        self.__email = email
        return Ok(self)

    def set_id(self, id: str) -> Result[Self, str]:
        self.__id = id
        return Ok(self)

    def set_phone(self, phone: str) -> Result[Self, str]:
        if len(phone) == 0:
            return Err("Phone number cannot be empty!")
        if any(char.isalpha() for char in phone):
            return Err("Phone number cannot contain letters!")
        self.__phone = phone
        return Ok(self)

    def set_department(self, department: Department) -> Result[Self, str]:
        self.__department = department
        return Ok(self)

    def set_benefits(self, benefits: list[BenefitPlan]) -> Result[Self, str]:
        self.__benefits = benefits
        return Ok(self)

    def set_payroll(self, payroll: Payroll) -> Result[Self, str]:
        self.__payroll = payroll
        return Ok(self)

    def set_attendance(self, attendance: Attendance) -> Result[Self, str]:
        self.__attendance = attendance
        return Ok(self)

    def set_performance(self, performance: Performance) -> Result[Self, str]:
        self.__performance = performance
        return Ok(self)

    def is_enrolled_in_plan(self, benefit: BenefitPlan) -> bool:
        return benefit in self.__benefits

    def __str__(self) -> None:
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