import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class Payroll:          # tính lương theo tháng của mỗi nhân viên
    def __init__(self) -> Self:
        self.__salary = 0    # lương cứng
        self.__bonus = 0     # thưởng
        self.__tax = 0       # thuế
        self.__punish = 0    # phạt
        self.__total = 0     # tổng lương

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

    def calculate_total(self) -> None:
        self.__total = self.__salary + self.__bonus - self.__tax - self.__punish

    def set_month(self) -> None:
        while True:
            month = int(input("Enter month: "))
            if month >= 1 and month <= 12:
                self.__month = month
                break
            else:
                print("Invalid month! Enter again!")

    def get_month(self) -> int:
        return self.__month

    def set_year(self) -> None:
        while True:
            year = int(input("Enter year: "))
            if year >= 2000:
                self.__year = year
                break
            else:
                print("Invalid year! Enter again!")

    def get_year(self) -> int:
        return self.__year

    def display(self) -> None:
        print(f"Month: {self.__month}")
        print(f"Salary: {self.__salary}")
        print(f"Bonus: {self.__bonus}")
        print(f"Tax: {self.__tax}")
        print(f"Punish: {self.__punish}")
        print(f"Total: {self.__total}")
