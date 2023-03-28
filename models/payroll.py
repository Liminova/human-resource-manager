import sys
from option import Result, Ok, Err
import textwrap

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

    def set_salary(self, salary: int) -> Result[Self, str]:
        if not self.verify(salary):
            return Err("Salary cannot be negative.")
        self.__salary = salary
        self.calculate_total()
        return Ok(self)

    def set_bonus(self, bonus: int) -> Result[Self, str]:
        if not self.verify(bonus):
            return Err("Bonus cannot be negative.")
        self.__bonus = bonus
        self.calculate_total()
        return Ok(self)

    def set_tax(self, tax: int) -> Result[Self, str]:
        if not self.verify(tax):
            return Err("Tax cannot be negative.")
        self.__tax = tax
        self.calculate_total()
        return Ok(self)

    def set_punish(self, punish: int) -> Result[Self, str]:
        if not self.verify(punish):
            return Err("Punishment cannot be negative.")
        self.__punish = punish
        self.calculate_total()
        return Ok(self)

    def verify(self, value: int) -> bool:
        if value < 0:
            return False
        return True

    def calculate_total(self) -> Self:
        self.__total = self.__salary + self.__bonus - self.__tax - self.__punish
        return self

    def __str__(self) -> str:
        return textwrap.dedent(f"""\
            - Salary: {self.__salary}
            - Bonus: {self.__bonus}
            - Tax: {self.__tax}
            - Punish: {self.__punish}
            - Total: {self.__total}
        """)