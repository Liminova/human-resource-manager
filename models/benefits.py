from __future__ import annotations
import sys

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
    def name(self, name: str) -> Self:
        self.__name = name
        return self

    @description.setter
    def description(self, description: str) -> Self:
        self.__description = description
        return self

    @cost.setter
    def cost(self, cost: float) -> Self:
        self.__cost = cost
        return self

    @enrolled_employees.setter
    def enrolled_employees(self, enrolled_employees: list) -> Self:
        self.__enrolled_employees = enrolled_employees
        return self

    def display(self):
        print(f"- Name: {self.__name}")
        print(f"- Description: {self.__description}")
        print(f"- Cost: {self.__cost}")
        print("- Enrolled employees:")
        for employee in self.__enrolled_employees:
            employee.display()
