from __future__ import annotations
import sys
from option import Result, Ok, Err

if sys.version_info >= (3, 11):
    from typing import Self, TYPE_CHECKING
else:
    from typing_extensions import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from .employee import Employee

class BenefitPlan:
    def __init__(
            self, name: str, description: str,
            cost: float, enrolled_employees: list[Employee]) -> None:
        self.__name = name
        self.__description = description
        self.__cost = cost
        self.__enrolled_employees = enrolled_employees

    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> str:
        return self.__description

    @property
    def cost(self) -> float:
        return self.__cost

    @property
    def enrolled_employees(self) -> list:
        return self.__enrolled_employees

    @name.setter
    def name(self, name: str) -> Result[Self, str]:
        self.__name = name
        return Ok(self) if name else Err("Name cannot be empty.")

    @description.setter
    def description(self, description: str) -> Result[Self, str]:
        self.__description = description
        return Ok(self) if description else Err("Description cannot be empty.")

    @cost.setter
    def cost(self, cost: float) -> Result[Self, str]:
        self.__cost = cost
        return Ok(self) if cost else Err("Cost cannot be empty.")

    @enrolled_employees.setter
    def enrolled_employees(self, enrolled_employees: list) -> Result[Self, str]:
        self.__enrolled_employees = enrolled_employees
        return Ok(self) if enrolled_employees else Err("Enrolled employees cannot be empty.")

    # NOTE: same note as department's display method. - Rylie
    def display(self) -> None:
        print(f"- Name: {self.__name}")
        print(f"- Description: {self.__description}")
        print(f"- Cost: {self.__cost}")
        print("- Enrolled employees:")
        for (i, employee) in enumerate(self.__enrolled_employees, 1):
            print(f"Employee {i}:")
            print(employee)
            print()
