import sys
from option import Result, Ok, Err
import textwrap

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class Payroll:
    """Monthly payroll for an employee."""
    salary = 0
    bonus = 0
    tax = 0
    punish = 0
    total = 0

    def set_salary(self, salary: int) -> Result[Self, str]:
        self.salary = salary
        self.calculate_total()
        return Ok(self) if salary >= 0 else Err("Salary cannot be negative.")

    def set_bonus(self, bonus: int) -> Result[Self, str]:
        self.bonus = bonus
        self.calculate_total()
        return Ok(self) if bonus >= 0 else Err("Bonus cannot be negative.")

    def set_tax(self, tax: int) -> Result[Self, str]:
        self.tax = tax
        self.calculate_total()
        return Ok(self) if tax >= 0 else Err("Tax cannot be negative.")

    def set_punish(self, punish: int) -> Result[Self, str]:
        self.punish = punish
        self.calculate_total()
        return Ok(self) if punish >= 0 else Err("Punish cannot be negative.")

    def calculate_total(self) -> None:
        self.total = self.salary + self.bonus - self.tax - self.punish
        return None

    def __str__(self) -> str:
        self.calculate_total()
        return textwrap.dedent(f"""\
            - Salary: {self.salary}
            - Bonus: {self.bonus}
            - Tax: {self.tax}
            - Punish: {self.punish}
            - Total: {self.total}\
        """)

    class Config:
        arbitrary_types_allowed = True
