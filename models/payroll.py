import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class Payroll:          # tính lương theo tháng của mỗi nhân viên
    def __init__(self, salary: int, tax: int) -> None:
        self.__salary = salary    # lương cứng
        self.__bonus = 0          # thưởng
        self.__tax = tax          # thuế
        self.__punish = 0         # phạt
        self.__total = 0          # tổng lương

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
        return self

    @bonus.setter
    def bonus(self, bonus: int) -> Self:
        self.__bonus = bonus
        return self

    @tax.setter
    def tax(self, tax: int) -> Self:
        self.__tax = tax
        return self

    @punish.setter
    def punish(self, punish: int) -> Self:
        self.__punish = punish
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
