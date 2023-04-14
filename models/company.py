from __future__ import annotations
import sys
from threading import Lock
from option import Result, Ok, Err
from .employee import Employee

if sys.version_info >= (3, 11):
    from typing import Self, TYPE_CHECKING
else:
    from typing_extensions import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from .benefits import BenefitPlan
    from .department import Department


# thread-safe singleton implementation, there should only be one instance of
# Company existing at all times.
class CompanyMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):  # type: ignore
        with cls._lock:
            if cls not in cls._instances:  # type: ignore
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance  # type: ignore
        return cls._instances[cls]  # type: ignore


class Company(metaclass=CompanyMeta):
    def __init__(self) -> None:
        self.__name = ""
        self.departments: list[Department] = []
        self.employees: list[Employee] = []
        self.benefits: list[BenefitPlan] = []

        # don't add these to database
        self.logged_in_employee: Employee = Employee()
        self.admins: list[Employee] = [
            employee for employee in self.employees if employee.is_admin
        ]

    @property
    def is_owner(self) -> bool:
        if self.logged_in_employee.name == "":
            return False
        is_first_account = self.employees.index(self.logged_in_employee) == 0
        has_admin_rights = self.logged_in_employee.is_admin
        valid_name = self.logged_in_employee.name == "Owner"
        if is_first_account and has_admin_rights and valid_name:
            return True
        return False

    @property
    def name(self) -> str:
        return self.__name

    def can_modify(self, type: str, input_employee: Employee) -> bool:
        """Check if the logged in employee can modify the given employee's data. Available types are:
        - attendance
        - benefits
        - department
        - employee
        - payroll
        - performance
        - password
        """
        if self.is_owner:
            return True
        if self.logged_in_employee.name == "":
            return False

        is_logged_in_admin = self.logged_in_employee.is_admin
        is_input_admin = input_employee.is_admin
        is_self: bool = self.logged_in_employee == input_employee

        if (type == "password") and (is_self) and (not is_logged_in_admin):
            return True

        if not is_logged_in_admin:
            return False

        # + everyone
        match type:
            # - themselves, other admins (owner included)
            case "attendance" | "department" | "payroll" | "performance":
                if (not is_self) and (not is_input_admin):
                    return True
            # - themselves, owner
            case "benefits":
                if (not is_self) and (not self.is_owner):
                    return True
            # - other admins (owner included)
            case "employee" | "password":
                if not is_input_admin:
                    return True
            case _:
                raise ValueError(f"Invalid type for system.can_modify: {type}")
        return False

    def set_name(self, name: str) -> Result[Self, str]:
        if name == "":
            return Err("Name cannot be empty!")
        self.__name = name
        return Ok(self)

    def is_id_taken(self, id: str) -> bool:
        for employee in self.employees:
            if employee.id == id:
                return True
        return False
