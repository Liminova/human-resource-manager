from __future__ import annotations
import sys
from ..helpers import *
from models import BenefitPlan
from database.mongo import benefit_repo, employee_repo
if sys.version_info >= (3, 11):
    from typing import TYPE_CHECKING
else:
    from typing_extensions import TYPE_CHECKING
if TYPE_CHECKING:
    from ...models.company import Company

class MenuBenefits:
    def __init__(self, company: Company):
        self.__company = company

    def start(self) -> tuple[bool, str]:
        benefits = self.__company.benefits

        last_msg = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg = ""
            benefit_plan_menu = [
                "[1] Add benefit plan",
                "[2] Apply benefit plan to employee",
                "[3] Remove benefit plan",
                "[4] Update benefit plan",
                "[5] View benefit plan",
                "[6] Exit",
            ]
            choice = get_user_option_from_menu("Benefit plan management", benefit_plan_menu)

            if (choice not in [1, 6]) and (not benefits):
                last_msg = "No benefits available! Please add a benefit plan first."
                continue

            match choice:
                case 1: last_msg = self.__add()
                case 2: last_msg = self.__apply()
                case 3: last_msg = self.__remove()
                case 4: last_msg = self.__update()
                case 5: last_msg = self.__view()
                case _: return True, ""

    def __add(self) -> str:
        benefits = self.__company.benefits

        # create a blank benefit plan object
        benefit = BenefitPlan()

        # assign values to the benefit plan object
        input_fields = [
            ("Enter benefit plan name: ", benefit.set_name),
            ("Enter benefit plan description: ", benefit.set_description),
            ("Enter benefit plan cost: ", benefit.set_cost),
        ]
        for prompt, setter in input_fields:
            loop_til_valid_input(prompt, setter)

        # add the benefit plan to the company
        benefits.append(benefit)
        benefit_repo.insert_one(benefit.dict(by_alias=True))

        return f"Benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} added successfully!"

    def __apply(self) -> str:
        employees = self.__company.employees
        benefits = self.__company.benefits

        # a list containing the string representation of each employee
        employee_items = [f"{employee.name} ({employee.id})" for employee in employees]

        # get the index of the employee selected by the user
        employee_index_selected = get_user_option_from_list("Select an employee to apply benefit plan to", employee_items)
        if employee_index_selected == -1:
            return ""

        # a list containing the string representation of each benefit
        benefit_items = [f"{benefit.name} ({benefit.cost})" for benefit in benefits]

        # get the index of the benefit selected by the user
        benefit_index_selected = get_user_option_from_list("Select a benefit plan to apply to employee", benefit_items)
        if benefit_index_selected == -1:
            return ""

        # get the actual employee and benefit objects
        benefit = benefits[benefit_index_selected]
        employee = employees[employee_index_selected]

        # check if the employee already has the benefit applied to them
        if benefit in employee.benefits:
            return f"Employee {FCOLORS.GREEN}{employee.name}{FCOLORS.END} already has benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} applied to them!"

        # apply the benefit to the employee
        employee.benefits.append(benefit)
        employee_repo.update_one(
            { "_id": employee.id },
            { "$set": employee.dict(include={"benefits"}) },
            upsert=True,
        )
        benefit.enrolled_employees.append(employee)
        benefit_repo.update_one(
            { "_id": benefit.id },
            { "$set": benefit.dict(include={"enrolled_employees"}) },
            upsert=True,
        )

        return f"Benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} applied to employee {FCOLORS.GREEN}{employee.name}{FCOLORS.END} successfully!"

    def __remove(self) -> str:
        employees = self.__company.employees
        benefits = self.__company.benefits

        # a list containing the string representation of each benefit
        benefit_items = [f"{benefit.name} ({benefit.cost})" for benefit in benefits]

        # get the index of the benefit selected by the user
        benefit_index_selected = get_user_option_from_list("Select a benefit plan to remove", benefit_items)
        if benefit_index_selected == -1:
            return ""

        # get the actual benefit object
        benefit = benefits[benefit_index_selected]

        # remove the benefit from whatever employee it's applied to
        for employee in employees:
            if benefit in employee.benefits:
                employee.benefits.remove(benefit)
                employee_repo.update_one(
                    { "_id": employee.id },
                    { "$set": employee.dict(include={"benefits"}) },
                    upsert=True,
                )

        # remove the benefit from the company's list of benefits
        # benefits.pop(benefit_index_selected)
        benefits.remove(benefit)
        benefit_repo.delete_one({ "_id": benefit.id })

        return f"Benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} removed successfully!"

    def __update(self) -> str:
        benefits = self.__company.benefits

        # a list containing the string representation of each benefit
        benefit_items = [f"{benefit.name} ({benefit.cost})" for benefit in benefits]

        # get the index of the benefit selected by the user
        selected_benefit_index = get_user_option_from_list("Select a benefit plan to update", benefit_items)
        if selected_benefit_index == -1:
            return ""

        # get the actual benefit object
        benefit = benefits[selected_benefit_index]

        # assigning the new values to the benefit object
        fields_data = [
            ("Enter benefit plan name: ", benefit.set_name),
            ("Enter benefit plan description: ", benefit.set_description),
            ("Enter benefit plan cost: ", benefit.set_cost),
        ]
        for (field, setter) in fields_data:
            loop_til_valid_input(field, setter)

        benefit_repo.update_one(
            { "_id": benefit.id },
            { "$set": benefit.dict(exclude={"id"}, by_alias=True) },
            upsert=True,
        )

        return f"Benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} updated successfully!"

    def __view(self) -> str:
        benefits = self.__company.benefits

        # a list containing the string representation of each benefit
        benefit_items = [f"{benefit.name} ({benefit.cost})" for benefit in benefits]

        # get the index of the benefit selected by the user
        selected_benefit_index = get_user_option_from_list("Select a benefit plan to view", benefit_items)
        if selected_benefit_index == -1:
            return ""

        # print the benefit
        print(benefits[selected_benefit_index])
        input("Press enter to continue...")

        return ""
