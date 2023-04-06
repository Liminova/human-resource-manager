from __future__ import annotations
import sys
from ..helpers import *
from models import Payroll
if sys.version_info >= (3, 11):
    from typing import TYPE_CHECKING
else:
    from typing_extensions import TYPE_CHECKING
if TYPE_CHECKING:
    from ...models.company import Company

class MenuPayroll:
    def __init__(self, company: Company):
        self.__company = company

    def start(self) -> tuple[bool, str]:
        employees = self.__company.employees
        if not employees:
            return False, "No employees to manage payroll for!"

        selected_employee_index = get_user_option_from_list("Select an employee to manage payroll for", [f"{employee.name} ({employee.id})" for employee in employees])
        if selected_employee_index == -1:
            return False, "No employee selected!"
        self.__employee = employees[selected_employee_index]

        last_msg = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg = ""
            payroll_menu = [
                "[1] Create payroll",
                "[2] Update payroll",
                "[else] Exit"
            ]
            choice = get_user_option_from_menu("Payroll management", payroll_menu)
            match choice:
                case 1: last_msg = self.__create()
                case 2: last_msg = self.__update()
                case _: return True, ""

    def __create(self) -> str:
        if self.__employee.payroll != None:
            return f"Employee {FCOLORS.GREEN}{self.__employee.name}{FCOLORS.END} already has a payroll!"

        clrscr()
        print(f"== Creating payroll for employee {FCOLORS.GREEN}{self.__employee.name}{FCOLORS.END} ==")

        # create an empty payroll object
        payroll = Payroll()

        # assigning values to the payroll object
        fields_data = [
            ("Enter payroll salary: ", payroll.set_salary),
            ("Enter payroll bonus: ", payroll.set_bonus),
            ("Enter payroll tax: ", payroll.set_tax),
            ("Enter payroll punishment: ", payroll.set_punish)
        ]
        for (field, setter) in fields_data:
            loop_til_valid_input(field, setter)

        # add the payroll object to the employee
        self.__employee.payroll = payroll
        return f"Payroll for employee {FCOLORS.GREEN}{self.__employee.name}{FCOLORS.END} created successfully!"

    def __update(self) -> str:
        payroll = self.__employee.payroll
        if payroll is None:
            return f"Employee {FCOLORS.GREEN}{self.__employee.name}{FCOLORS.END} has no payroll!"

        clrscr()
        print(f"== Updating payroll for employee {FCOLORS.GREEN}{self.__employee.name}{FCOLORS.END} ==")

        # assigning values to the payroll object
        fields_data = [
            ("Enter payroll salary: ", payroll.set_salary),
            ("Enter payroll bonus: ", payroll.set_bonus),
            ("Enter payroll tax: ", payroll.set_tax),
            ("Enter payroll punishment: ", payroll.set_punish)
        ]
        for (field, setter) in fields_data:
            loop_til_valid_input(field, setter)

        return f"Payroll for employee {FCOLORS.GREEN}{self.__employee.name}{FCOLORS.END} updated successfully!"