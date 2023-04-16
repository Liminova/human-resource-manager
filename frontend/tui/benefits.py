from __future__ import annotations
import sys
import os

from ..helpers import *
from models import BenefitPlan, Company
from database.mongo import benefit_repo, employee_repo
from option import Result, Ok

if sys.version_info >= (3, 11):
    from typing import TYPE_CHECKING
else:
    from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Employee

the_company: Company = Company()


class MenuBenefits:
    def __init__(self):
        if the_company.logged_in_employee.is_admin:
            self.mainloop = self.admin
        else:
            self.mainloop = self.employee

    def admin(self) -> Result[None, str]:
        last_msg: str = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg: str = ""
            benefit_plan_menu = [
                "[1] Add benefit",
                "[2] Apply benefit to employee",
                "[3] Remove benefit",
                "[4] Update benefit",
                "[5] View details of benefit",
                "[6] List all benefits",
                "[7] Request to enroll in benefit",
                "[8] Resolve pending requests",
                "[9] Back",
            ]

            title = "Benefit plan management"
            if (
                pending_request_count := len(
                    [
                        employee
                        for benefit in the_company.benefits
                        for employee in benefit.pending_requests
                    ]
                )
                > 0
            ):
                title += f" ({FCOLORS.BLUE}{pending_request_count}{FCOLORS.END} pending requests)"

            choice = get_user_option_from_menu(title, benefit_plan_menu)
            match choice:
                case 1:
                    last_msg: str = self.__add()
                case 2:
                    last_msg: str = self.__apply()
                case 3:
                    last_msg: str = self.__remove()
                case 4:
                    last_msg: str = self.__update()
                case 5:
                    last_msg: str = self.__view()
                case 6:
                    last_msg: str = self.__view_all()
                case 7:
                    last_msg: str = self.__request_enroll()
                case 8:
                    last_msg: str = self.__resolve_pending_requests()
                case 9:
                    return Ok(None)
                case _:
                    last_msg: str = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def employee(self) -> Result[None, str]:
        logged_in_employee = the_company.logged_in_employee
        last_msg: str = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg: str = ""
            benefit_plan_menu = [
                "[1] View details of one",
                "[2] List all",
                "[3] Request to enroll in one",
                "[4] Back",
            ]
            choice = get_user_option_from_menu(
                "Benefit plan management for " + logged_in_employee.name,
                benefit_plan_menu,
            )
            match choice:
                case 1:
                    last_msg: str = self.__view()
                case 2:
                    last_msg: str = self.__view_all()
                case 3:
                    last_msg: str = self.__request_enroll()
                case 4:
                    return Ok(None)
                case _:
                    last_msg: str = FCOLORS.RED + "Invalid option!" + FCOLORS.END

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
        the_company.benefits.append(benefit)
        if os.getenv("HRMGR_DB") == "TRUE":
            benefit_repo.insert_one(benefit.dict(by_alias=True))

        return f"Benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} added successfully!"

    def __apply(self) -> str:
        employees = the_company.employees
        benefits = the_company.benefits

        # a list containing the string representation of each employee
        employee_items = [f"{e.name} ({e.employee_id})" for e in employees]

        # get the index of the employee selected by the user
        employee_index_selected = get_user_option_from_list(
            "Select an employee to apply benefit plan to", employee_items
        )
        if employee_index_selected == -1:
            return NO_EMPLOYEE_MSG
        elif employee_index_selected == -2:
            return ""

        # get the actual employee object
        employee = employees[employee_index_selected]

        if not the_company.can_modify("benefits", employee):
            return "Only other admins can manage your benefits!"

        # a list containing the string representation of each benefit
        benefit_items = [f"{benefit.name} ({benefit.cost})" for benefit in benefits]

        # get the index of the benefit selected by the user
        benefit_index_selected = get_user_option_from_list(
            "Select a benefit plan to apply to employee", benefit_items
        )
        if benefit_index_selected == -1:
            return NO_BENEFIT_MSG
        elif benefit_index_selected == -2:
            return ""

        # get the actual benefit objects
        benefit = benefits[benefit_index_selected]

        # check if the employee already has the benefit applied to them
        if benefit.name in employee.benefits:
            return f"Employee {FCOLORS.GREEN}{employee.name}{FCOLORS.END} already has benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} applied to them!"

        # apply the benefit to the employee
        employee.benefits.append(benefit.name)
        benefit.enrolled_employees.append(employee)
        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one(
                {"_id": employee.id},
                {"$set": employee.dict(include={"benefits"})},
                upsert=True,
            )
            benefit_repo.update_one(
                {"_id": benefit.id},
                {"$set": benefit.dict(include={"enrolled_employees"})},
                upsert=True,
            )

        return f"Benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} applied to employee {FCOLORS.GREEN}{employee.name}{FCOLORS.END} successfully!"

    def __remove(self) -> str:
        benefits = the_company.benefits
        employees = the_company.employees

        # a list containing the string representation of each benefit
        benefit_items = [f"{benefit.name} ({benefit.cost})" for benefit in benefits]

        # get the index of the benefit selected by the user
        benefit_index_selected = get_user_option_from_list(
            "Select a benefit plan to remove", benefit_items
        )
        if benefit_index_selected == -1:
            return NO_BENEFIT_MSG
        elif benefit_index_selected == -2:
            return ""

        # get the actual benefit object
        benefit = benefits[benefit_index_selected]

        # remove the benefit plan from all employees that have it applied to them
        for employee in employees:
            if benefit.name in employee.benefits:
                employee.benefits.remove(benefit.name)
                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one(
                        {"_id": employee.id},
                        {"$set": employee.dict(include={"benefits"})},
                        upsert=True,
                    )

        # remove the benefit from the company's list of benefits
        del benefits[benefit_index_selected]
        if os.getenv("HRMGR_DB") == "TRUE":
            benefit_repo.delete_one({"_id": benefit.id})

        return (
            f"Benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} removed successfully!"
        )

    def __update(self) -> str:
        benefits = the_company.benefits

        # a list containing the string representation of each benefit
        benefit_items = [f"{benefit.name} ({benefit.cost})" for benefit in benefits]

        # get the index of the benefit selected by the user
        selected_benefit_index = get_user_option_from_list(
            "Select a benefit plan to update", benefit_items
        )
        if selected_benefit_index == -1:
            return NO_BENEFIT_MSG
        elif selected_benefit_index == -2:
            return ""

        # get the actual benefit object
        benefit = benefits[selected_benefit_index]

        # assigning the new values to the benefit object
        fields_data = [
            ("Enter benefit plan name", benefit.set_name),
            ("Enter benefit plan description", benefit.set_description),
            ("Enter benefit plan cost", benefit.set_cost),
        ]
        for field, setter in fields_data:
            if (msg := loop_til_valid_input(field, setter)) != "":
                return msg

        if os.getenv("HRMGR_DB") == "TRUE":
            benefit_repo.update_one(
                {"_id": benefit.id},
                {"$set": benefit.dict(exclude={"id"}, by_alias=True)},
                upsert=True,
            )

        return (
            f"Benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} updated successfully!"
        )

    def __view(self) -> str:
        logged_in_employee = the_company.logged_in_employee

        # a list containing the string representation of each benefit
        benefits: list[BenefitPlan] = []
        if not logged_in_employee.is_admin:
            # restore the benefit objects from the benefit names
            benefits = [
                benefit
                for benefit in the_company.benefits
                if benefit.name in logged_in_employee.benefits
            ]
            benefit_items = [f"{benefit.name} ({benefit.cost})" for benefit in benefits]
        else:
            benefit_items = [
                f"{benefit.name} ({benefit.cost})" for benefit in the_company.benefits
            ]

        # get the index of the benefit selected by the user
        selected_benefit_index = get_user_option_from_list(
            "Select a benefit plan to view", benefit_items
        )
        if selected_benefit_index == -1:
            return NO_BENEFIT_MSG
        elif selected_benefit_index == -2:
            return ""

        # print the benefit plan
        if not logged_in_employee.is_admin:
            print(logged_in_employee.benefits[selected_benefit_index])
        else:
            print(benefits[selected_benefit_index])
        input(ENTER_TO_CONTINUE_MSG)

        return ""

    def __view_all(self) -> str:
        logged_in_employee = the_company.logged_in_employee
        benefits = the_company.benefits

        if not logged_in_employee.is_admin:
            # restore the benefit objects from the benefit names
            benefits: list[BenefitPlan] = [
                benefit
                for benefit in benefits
                if benefit.name in logged_in_employee.benefits
            ]
            benefit_items = [f"{benefit.name} ({benefit.cost})" for benefit in benefits]
        else:
            benefit_items = [f"{benefit.name} ({benefit.cost})" for benefit in benefits]
        if len(benefit_items) == 0:
            return NO_BENEFIT_MSG
        listing("All existing benefit plans", benefit_items)
        return ""

    def __request_enroll(self) -> str:
        logged_in_employee = the_company.logged_in_employee
        benefits = the_company.benefits

        benefit_items = [f"{benefit.name} ({benefit.cost})" for benefit in benefits]
        selected_benefit_index = get_user_option_from_list(
            "Select a benefit plan to request enrollment", benefit_items
        )
        if selected_benefit_index == -1:
            return NO_BENEFIT_MSG
        elif selected_benefit_index == -2:
            return ""
        benefit = benefits[selected_benefit_index]

        if logged_in_employee in benefit.enrolled_employees:
            return f"Employee {FCOLORS.GREEN}{logged_in_employee.name}{FCOLORS.END} already has benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} applied to them!"

        if logged_in_employee in benefit.pending_requests:
            return f"Employee {FCOLORS.GREEN}{logged_in_employee.name}{FCOLORS.END} already has a pending request for benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END}!"

        benefit.pending_requests.append(logged_in_employee)
        if os.getenv("HRMGR_DB") == "TRUE":
            benefit_repo.update_one(
                {"_id": benefit.id},
                {"$set": benefit.dict(include={"pending_requests"})},
                upsert=True,
            )

        return f"Request for benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} sent to HR successfully!"

    def __resolve_pending_requests(self):
        custom_pending_requests: dict[BenefitPlan, list[Employee]] = {}
        benefits = the_company.benefits

        for benefit in benefits:
            if len(benefit.pending_requests) > 0:
                custom_pending_requests[benefit] = benefit.pending_requests

        # a list representing all benefit plans with pending requests
        benefit_items = [
            f"{benefit.name} ({benefit.cost})"
            for benefit in custom_pending_requests.keys()
        ]
        benefit_index_selected = get_user_option_from_list(
            "Select a benefit plan to resolve pending requests for", benefit_items
        )
        if benefit_index_selected == -1:
            return NO_BENEFIT_MSG
        elif benefit_index_selected == -2:
            return ""

        # get the actual benefit object
        benefit = list(custom_pending_requests.keys())[benefit_index_selected]

        # a list representing all employees with pending requests for the selected benefit plan
        employee_items = [
            f"{employee.name} ({employee.id})"
            for employee in custom_pending_requests[benefit]
        ]
        employee_index_selected = get_user_option_from_list(
            "Select an employee to resolve their pending request", employee_items
        )
        if employee_index_selected == -1:
            return NO_EMPLOYEE_MSG
        elif employee_index_selected == -2:
            return ""

        # get the actual employee object
        employee = custom_pending_requests[benefit][employee_index_selected]

        if not the_company.can_modify("benefits", employee):
            return "You cannot approve or deny your own request!"

        empl_name = FCOLORS.GREEN + employee.name + FCOLORS.END
        empl_id = FCOLORS.GREEN + employee.employee_id + FCOLORS.END
        benefit_name = FCOLORS.GREEN + benefit.name + FCOLORS.END

        # get the user's decision
        decision = get_user_option_from_menu(
            f"Select an option for employee {empl_name} ({empl_id})'s pending request for benefit {benefit_name}",
            ["[1] Approve", "[2] Deny", "[3] Cancel"],
        )

        if decision == -1:
            return "Invalid option!"
        elif decision == -2 or decision == 3:
            return ""

        # remove the employee from the pending requests list
        benefit.pending_requests.remove(employee)

        # if the user approved the request, add the employee to the enrolled employees list and update the benefit plan for the employee
        if decision == 0:
            benefit.enrolled_employees.append(employee)
            employee.benefits.append(benefit.name)

        if os.getenv("HRMGR_DB") == "TRUE":
            benefit_repo.update_one(
                {"_id": benefit.id},
                {
                    "$set": benefit.dict(
                        include={"pending_requests", "enrolled_employees"}
                    )
                },
                upsert=True,
            )
            if decision == 1:
                employee_repo.update_one(
                    {"_id": employee.id},
                    {"$set": employee.dict(include={"benefits"})},
                    upsert=True,
                )

        if decision == 0:
            return (
                f"Employee {empl_name} ({empl_id}) approved for benefit {benefit_name}!"
            )
        else:
            return (
                f"Employee {empl_name} ({empl_id}) denied for benefit {benefit_name}!"
            )
