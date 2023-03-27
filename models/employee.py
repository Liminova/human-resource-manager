from __future__ import annotations
import sys

if sys.version_info >= (3, 11):
    from typing import Self, TYPE_CHECKING
else:
    from typing_extensions import Self, TYPE_CHECKING

if TYPE_CHECKING:
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

    @name.setter
    def name(self, name: str) -> Self:
        self.__name = name
        return self

    @dob.setter
    def dob(self, dob: str) -> Self:
        self.__dob = dob
        return self
    def email(self, email: str) -> Result[Self, str]:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, email):
            return Err("Invalid email format!")
        self.__email = email
        return Ok(self)

    @id.setter
    def id(self, id: str) -> Self:
        self.__id = id
        return self

    @phone.setter
    def phone(self, phone: str) -> Self:
        self.__phone = phone
        return self

    @department.setter
    def department(self, department: Department) -> Self:
        self.__department = department
        return self

    @benefits.setter
    def benefits(self, benefits: list[BenefitPlan]) -> Self:
        self.__benefits = benefits
        return self

    @payroll.setter
    def payroll(self, payroll: Payroll) -> Self:
        self.__payroll = payroll
        return self

    @attendance.setter
    def attendance(self, attendance: Attendance) -> Self:
        self.__attendance = attendance
        return self

    @performance.setter
    def performance(self, performance: Performance) -> Self:
        self.__performance = performance
        return self

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
