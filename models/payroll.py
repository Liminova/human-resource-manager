import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class Payroll:
    """Monthly payroll for an employee."""
    def __init__(self) -> None:
        self.__salary = 0
        self.__bonus = 0
        self.__tax = 0
        self.__punish = 0
        self.__total = 0

    @property
    def salary(self) -> int:
        return self.__salary

    @property
    def bonus(self) -> int:
        return self.__bonus

    @property
    def tax(self) -> int:
        return self.__tax

    @property
    def punish(self) -> int:
        return self.__punish

    @property
    def total(self) -> int:
        return self.__total

    @salary.setter
    def salary(self, salary: int) -> Self:
        self.__salary = salary
        self.calculate_total()
        return self

    @bonus.setter
    def bonus(self, bonus: int) -> Self:
        self.__bonus = bonus
        self.calculate_total()
        return self

    @tax.setter
    def tax(self, tax: int) -> Self:
        self.__tax = tax
        self.calculate_total()
        return self

    @punish.setter
    def punish(self, punish: int) -> Self:
        self.__punish = punish
        self.calculate_total()
        return self

    def calculate_total(self) -> Self:
        self.__total = self.__salary + self.__bonus - self.__tax - self.__punish
        return self

    def display(self) -> None:
        print(f"Salary: {self.__salary}")
        print(f"Bonus: {self.__bonus}")
        print(f"Tax: {self.__tax}")
        print(f"Punish: {self.__punish}")
        print(f"Total: {self.__total}")
