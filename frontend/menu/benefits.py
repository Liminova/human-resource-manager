from __future__ import annotations
import sys
import os

from ..helpers import *
from models import BenefitPlan
from database.mongo import benefit_repo, employee_repo # type: ignore
from option import Result, Ok

if sys.version_info >= (3, 11):
    from typing import TYPE_CHECKING
else:
    from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from ...models.company import Company

class MenuBenefits:
    def __init__(self, company: Company):
        self.__company = company

    def start(self) -> Result[None, str]:
        benefits = self.__company.benefits

        last_msg = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg = ""
            benefit_plan_menu = [
                "[1] Add",
                "[2] Apply one to employee",
                "[3] Remove",
                "[4] Update",
                "[5] View details of one",
                "[6] List all",
                "[7] Back",
            ]
            choice = get_user_option_from_menu("Benefit plan management", benefit_plan_menu)

            if (choice not in [1, 6]) and (not benefits):
                last_msg = NO_BENEFIT_MSG
                continue

            match choice:
                case 1: last_msg = self.__add()
                case 2: last_msg = self.__apply()
                case 3: last_msg = self.__remove()
                case 4: last_msg = self.__update()
                case 5: last_msg = self.__view()
                case 6: last_msg = self.__view_all()
                case 7: return Ok(None)
                case _: last_msg = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def __add(self) -> str:
        # create a blank benefit plan object
        benefit = BenefitPlan()

        # assign values to the benefit plan object
        input_fields = [
            ("Enter benefit plan name", benefit.set_name),
            ("Enter benefit plan description", benefit.set_description),
            ("Enter benefit plan cost", benefit.set_cost),
        ]
        for prompt, setter in input_fields:
            if (msg := loop_til_valid_input(prompt, setter)) != "":
                return msg

        # add the benefit plan to the company
        self.__company.benefits.append(benefit)
        if os.getenv("HRMGR_DB") == "TRUE":
            benefit_repo.insert_one(benefit.dict(by_alias=True)) # type: ignore

        return f"Benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} added successfully!"

    def __apply(self) -> str:
        # a list containing the string representation of each employee
        employee_items = [f"{employee.name} ({employee.employee_id})" for employee in self.__company.employees]

        # get the index of the employee selected by the user
        employee_index_selected = get_user_option_from_list("Select an employee to apply benefit plan to", employee_items)
        if employee_index_selected == -1:
            return NO_EMPLOYEE_MSG
        elif employee_index_selected == -2:
            return ""

        # a list containing the string representation of each benefit
        benefit_items = [f"{benefit.name} ({benefit.cost})" for benefit in self.__company.benefits]

        # get the index of the benefit selected by the user
        benefit_index_selected = get_user_option_from_list("Select a benefit plan to apply to employee", benefit_items)
        if benefit_index_selected == -1:
            return NO_BENEFIT_MSG
        elif benefit_index_selected == -2:
            return ""

        # get the actual employee and benefit objects
        employee = self.__company.employees[employee_index_selected]
        benefit = self.__company.benefits[benefit_index_selected]

        # check if the employee already has the benefit applied to them
        if benefit in employee.benefits:
            return f"Employee {FCOLORS.GREEN}{employee.name}{FCOLORS.END} already has benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} applied to them!"

        # apply the benefit to the employee
        employee.benefits.append(benefit)
        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one(
                { "_id": employee.id },
                { "$set": employee.dict(include={"benefits"}) },
                upsert=True,
            )
        benefit.enrolled_employees.append(employee)
        if os.getenv("HRMGR_DB") == "TRUE":
            benefit_repo.update_one(
                { "_id": benefit.id },
                { "$set": benefit.dict(include={"enrolled_employees"}) },
                upsert=True,
            )

        return f"Benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} applied to employee {FCOLORS.GREEN}{employee.name}{FCOLORS.END} successfully!"

    def __remove(self) -> str:
        # a list containing the string representation of each benefit
        benefit_items = [f"{benefit.name} ({benefit.cost})" for benefit in self.__company.benefits]

        # get the index of the benefit selected by the user
        benefit_index_selected = get_user_option_from_list("Select a benefit plan to remove", benefit_items)
        if benefit_index_selected == -1:
            return NO_BENEFIT_MSG
        elif benefit_index_selected == -2:
            return ""

        # get the actual benefit object
        benefit = self.__company.benefits[benefit_index_selected]

        # remove the benefit plan from all employees that have it applied to them
        for employee in self.__company.employees:
            if benefit in employee.benefits:
                employee.benefits.remove(benefit)
                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one(
                        { "_id": employee.id },
                        { "$set": employee.dict(include={"benefits"}) },
                        upsert=True,
                    )

        # remove the benefit from the company's list of benefits
        del self.__company.benefits[benefit_index_selected]
        if os.getenv("HRMGR_DB") == "TRUE":
            benefit_repo.delete_one({ "_id": benefit.id })

        return f"Benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} removed successfully!"

    def __update(self) -> str:
        # a list containing the string representation of each benefit
        benefit_items = [f"{benefit.name} ({benefit.cost})" for benefit in self.__company.benefits]

        # get the index of the benefit selected by the user
        selected_benefit_index = get_user_option_from_list("Select a benefit plan to update", benefit_items)
        if selected_benefit_index == -1:
            return NO_BENEFIT_MSG
        elif selected_benefit_index == -2:
            return ""

        # get the actual benefit object
        benefit = self.__company.benefits[selected_benefit_index]

        # assigning the new values to the benefit object
        fields_data = [
            ("Enter benefit plan name", benefit.set_name),
            ("Enter benefit plan description", benefit.set_description),
            ("Enter benefit plan cost", benefit.set_cost),
        ]
        for (field, setter) in fields_data:
            if (msg := loop_til_valid_input(field, setter)) != "":
                return msg

        if os.getenv("HRMGR_DB") == "TRUE":
            benefit_repo.update_one(
                { "_id": benefit.id },
                { "$set": benefit.dict(exclude={"id"}, by_alias=True) },
                upsert=True,
            )

        return f"Benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} updated successfully!"

    def __view(self) -> str:
        # a list containing the string representation of each benefit
        benefit_items = [f"{benefit.name} ({benefit.cost})" for benefit in self.__company.benefits]

        # get the index of the benefit selected by the user
        selected_benefit_index = get_user_option_from_list("Select a benefit plan to view", benefit_items)
        if selected_benefit_index == -1:
            return NO_BENEFIT_MSG
        elif selected_benefit_index == -2:
            return ""

        # print the benefit
        print(self.__company.benefits[selected_benefit_index])
        input(ENTER_TO_CONTINUE_MSG)

        return ""

    def __view_all(self) -> str:
        benefit_items = [f"{benefit.name} ({benefit.cost})" for benefit in self.__company.benefits]
        if len(benefit_items) == 0:
            return NO_BENEFIT_MSG
        listing("All existing benefit plans", benefit_items)
        return ""