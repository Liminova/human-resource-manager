from __future__ import annotations

import os

from option import Ok, Result

from database.mongo import benefit_repo, employee_repo  # type: ignore
from models import BenefitPlan, Company

from ..helpers_tui import *

the_company: Company = Company()


class MenuBenefits:
    def __init__(self):
        self.mainloop = self.admin if the_company.logged_in_employee.is_admin else self.employee

    def admin(self) -> Result[None, str]:
        last_msg = ""
        while True:
            last_msg = refresh(last_msg)
            benefit_plan_menu = [
                "[1] Add/remove/modify benefits",
                "[2] Apply/remove one to/from employees",
                "[3] Request to enroll",
                "[4] Resolve requests",
                "[5] View details",
                "[6] List empls w/o benefit",
                "[7] Back",
            ]

            title = "Benefit plan management"
            pending_reqs = [e for b in the_company.benefits for e in b.pending_requests]
            pending_request_count = len(pending_reqs)
            if pending_request_count > 0:
                title += f" ({FCOLORS.BLUE}{pending_request_count}{FCOLORS.END} pending requests)"

            choice = get_user_option_from_menu(title, benefit_plan_menu)
            match choice:
                case 1:  # Add/remove/modify benefits
                    clrscr()
                    # fmt: off
                    sub_choice = get_user_option_from_menu(
                        "Add/remove/modify benefits",
                        [
                            "[1] Add",
                            "[2] Remove",
                            "[3] Modify",
                            "[else] Back"
                        ]
                    )
                    # fmt: on
                    match sub_choice:
                        case 1:
                            last_msg = self.__add()
                        case 2:
                            last_msg = self.__remove()
                        case 3:
                            last_msg = self.__update()
                        case _:
                            last_msg = FCOLORS.RED + "Invalid option!" + FCOLORS.END

                case 2:  # Apply/remove benefits from employees
                    clrscr()
                    sub_choice = get_user_option_from_menu(
                        "Apply/remove benefits from employees", ["[1] Apply", "[2] Remove", "[else] Back"]
                    )
                    match sub_choice:
                        case 1:
                            last_msg = self.__apply_to_employee()
                        case 2:
                            last_msg = self.__remove_from_employee()
                        case _:
                            last_msg = ""
                case 3:
                    last_msg = self.__request_enroll()
                case 4:
                    last_msg = self.__resolve_pending_requests()
                case 5:
                    last_msg = self.__view()
                case 6:
                    last_msg = self.__list_employees_without_benefits()
                case 7:
                    return Ok(None)
                case _:
                    last_msg = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def employee(self) -> Result[None, str]:
        logged_in_employee = the_company.logged_in_employee
        last_msg = ""
        while True:
            last_msg = refresh(last_msg)
            # fmt: off
            benefit_plan_menu = [
                "[1] View details",
                "[2] Request to enroll",
                "[3] Back"
            ]
            # fmt: on
            choice = get_user_option_from_menu("Benefit plan management for " + logged_in_employee.name, benefit_plan_menu)
            match choice:
                case 1:
                    last_msg = self.__view()
                case 2:
                    last_msg = self.__request_enroll()
                case 3:
                    return Ok(None)
                case _:
                    last_msg = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def __add(self) -> str:
        # create a blank benefit plan object
        benefit = BenefitPlan()

        # assign values to the benefit plan object
        input_fields = (
            ("Enter benefit plan name", benefit.set_name),
            ("Enter benefit plan description", benefit.set_description),
            ("Enter benefit plan cost", benefit.set_cost),
        )
        for prompt, setter in tuple(input_fields):
            if (msg := loop_til_valid_input(prompt, setter)) != "":
                return msg

        # add the benefit plan to the company
        the_company.benefits.append(benefit)
        if os.getenv("HRMGR_DB") == "TRUE":
            benefit_repo.insert_one(benefit.dict(by_alias=True))  # type: ignore

        return f"Benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} added successfully!"

    def __remove(self) -> str:
        benefits = the_company.benefits
        employees = the_company.employees

        # get the index of the benefit selected by the user
        benefit_idx_select = get_user_option_from_list(
            "Select a benefit plan to remove", tuple(f"{b.name}" for b in benefits)
        )
        if benefit_idx_select in (-1, -2):
            return NO_BENEFIT_MSG if benefit_idx_select == -1 else ""
        _bnf = benefits[benefit_idx_select]

        # remove the benefit plan from all employees that have it applied to them
        for employee in employees:
            if _bnf.name not in employee.benefits:
                continue
            employee.benefits.remove(_bnf.name)
            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.update_one({"_id": employee.id}, {"$set": employee.dict(include={"benefits"})}, upsert=True)

        # remove the benefit from the company's list of benefits
        benefits.remove(_bnf)
        if os.getenv("HRMGR_DB") == "TRUE":
            benefit_repo.delete_one({"_id": _bnf.id})

        return f"Benefit {FCOLORS.RED}{_bnf.name}{FCOLORS.END} removed successfully!"

    def __update(self) -> str:
        benefits = the_company.benefits

        # get the index of the benefit selected by the user
        benefit_idx_select = get_user_option_from_list(
            "Select a benefit plan to update", tuple(f"{b.name} ({b.cost})" for b in benefits)
        )
        if benefit_idx_select in (-1, -2):
            return NO_BENEFIT_MSG if benefit_idx_select == -1 else ""
        _bnf = benefits[benefit_idx_select]

        # assigning the new values to the benefit object
        fields_data = (
            ("Enter benefit plan name", _bnf.set_name),
            ("Enter benefit plan description", _bnf.set_description),
            ("Enter benefit plan cost", _bnf.set_cost),
        )
        for field, setter in fields_data:
            if (msg := loop_til_valid_input(field, setter)) != "":
                return msg

        if os.getenv("HRMGR_DB") == "TRUE":
            benefit_repo.update_one(
                {"_id": _bnf.id}, {"$set": _bnf.dict(include={"name", "description", "cost"})}, upsert=True
            )
        return f"Benefit {FCOLORS.GREEN}{_bnf.name}{FCOLORS.END} updated successfully!"

    def __view(self) -> str:
        benefit_idx_select = get_user_option_from_list(
            "Select a benefit plan to view", tuple(f"{b.name} ({b.cost})" for b in the_company.benefits)
        )
        if benefit_idx_select in (-1, -2):
            return NO_BENEFIT_MSG if benefit_idx_select == -1 else ""

        clrscr()
        print(the_company.benefits[benefit_idx_select])
        input(ENTER_TO_CONTINUE_MSG)

        return ""

    def __apply_to_employee(self) -> str:
        empls = the_company.employees
        benefits = the_company.benefits

        # get the index of the employee selected by the user
        empl_idx_select = get_user_option_from_list(
            "Select an employee to apply benefit plan to", tuple(f"{e.name} ({e.employee_id})" for e in empls)
        )
        if empl_idx_select in (-1, -2):
            return NO_EMPLOYEE_MSG if empl_idx_select == -1 else ""

        if not the_company.can_modify("benefits", empls[empl_idx_select]):
            return "Only other admins can manage your benefits!"

        # get the index of the benefit selected by the user
        benefit_idx_select = get_user_option_from_list(
            "Select a benefit plan to apply to employee", tuple(f"{b.name}" for b in benefits)
        )
        if benefit_idx_select in (-1, -2):
            return NO_BENEFIT_MSG if benefit_idx_select == -1 else ""

        _bnf, _empl = benefits[benefit_idx_select], empls[empl_idx_select]

        # check if the employee already has the benefit applied to them
        if _bnf.name in _empl.benefits:
            return "Employee {}{}{} already has benefit {}{}{} applied to them!".format(
                FCOLORS.GREEN, _empl.name, FCOLORS.END, FCOLORS.GREEN, _bnf.name, FCOLORS.END
            )

        # apply the benefit to the employee and vice versa
        _empl.benefits.append(_bnf.name)
        _bnf.enrolled_employees.append(_empl)

        # update DB
        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one({"_id": _empl.id}, {"$set": _empl.dict(by_alias=True, include={"benefits"})})
            benefit_repo.update_one({"_id": _bnf.id}, {"$set": _bnf.dict(by_alias=True, include={"enrolled_employees"})})

        return "Benefit {}{}{} applied to employee {}{}{} successfully!".format(
            FCOLORS.GREEN, _bnf.name, FCOLORS.END, FCOLORS.GREEN, _empl.name, FCOLORS.END
        )

    def __remove_from_employee(self) -> str:
        empls = the_company.employees
        benefits = the_company.benefits

        # get the index of the employee selected by the user
        empl_idx_select = get_user_option_from_list(
            "Select an employee to remove benefit plan from", tuple(f"{e.name} ({e.employee_id})" for e in empls)
        )
        if empl_idx_select in (-1, -2):
            return NO_EMPLOYEE_MSG if empl_idx_select == -1 else ""

        if not the_company.can_modify("benefits", empls[empl_idx_select]):
            return "Only other admins can manage your benefits!"

        # get the index of the benefit selected by the user
        benefit_idx_select = get_user_option_from_list(
            "Select a benefit plan to remove from employee", tuple(f"{b.name}" for b in benefits)
        )
        if benefit_idx_select in (-1, -2):
            return NO_BENEFIT_MSG if benefit_idx_select == -1 else ""

        _bnf, _empl = benefits[benefit_idx_select], empls[empl_idx_select]

        # check if the employee already has the benefit applied to them
        if _bnf.name not in _empl.benefits:
            return "Employee {}{}{} does not have benefit {}{}{} applied to them!".format(
                FCOLORS.GREEN, _empl.name, FCOLORS.END, FCOLORS.GREEN, _bnf.name, FCOLORS.END
            )

        # remove the benefit from the employee and vice versa
        _empl.benefits.remove(_bnf.name)
        _bnf.enrolled_employees.remove(_empl)

        # update DB
        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one({"_id": _empl.id}, {"$set": _empl.dict(by_alias=True, include={"benefits"})})
            benefit_repo.update_one({"_id": _bnf.id}, {"$set": _bnf.dict(by_alias=True, include={"enrolled_employees"})})

        return "Benefit {}{}{} removed from employee {}{}{} successfully!".format(
            FCOLORS.GREEN, _bnf.name, FCOLORS.END, FCOLORS.GREEN, _empl.name, FCOLORS.END
        )

    def __request_enroll(self) -> str:
        logged_in_employee = the_company.logged_in_employee
        benefits = the_company.benefits

        benefit_idx_select = get_user_option_from_list(
            "Select a benefit plan to request enrollment", tuple(f"{b.name} ({b.cost})" for b in benefits)
        )
        if benefit_idx_select in (-1, -2):
            return NO_BENEFIT_MSG if benefit_idx_select == -1 else ""
        _bnf = benefits[benefit_idx_select]

        if logged_in_employee in _bnf.enrolled_employees:
            return f"You are already enrolled in benefit {FCOLORS.GREEN}{_bnf.name}{FCOLORS.END}!"

        if logged_in_employee in _bnf.pending_requests:
            return f"You have already requested enrollment in benefit {FCOLORS.GREEN}{_bnf.name}{FCOLORS.END}!"

        benefits[benefit_idx_select].pending_requests.append(logged_in_employee)
        if os.getenv("HRMGR_DB") == "TRUE":
            benefit_repo.update_one(
                {"_id": _bnf.id}, {"$set": _bnf.dict(by_alias=True, include={"pending_requests"})}, upsert=True
            )

        return f"Request for benefit {FCOLORS.GREEN}{_bnf.name}{FCOLORS.END} sent to HR successfully!"

    def __resolve_pending_requests(self):
        benefits = the_company.benefits

        # getting the index of the benefit selected by the user
        benefit_idx_select = get_user_option_from_list(
            "Select a benefit plan to resolve pending requests for",
            tuple(f"{benefit.name} ({benefit.cost})" for benefit in benefits if len(benefit.pending_requests) > 0),
        )
        if benefit_idx_select in (-1, -2):
            return NO_BENEFIT_MSG if benefit_idx_select == -1 else ""

        # getting the index of the employee selected by the user
        empl_idx_select = get_user_option_from_list(
            "Select an employee to resolve their pending request",
            tuple(f"{employee.name} ({employee.id})" for employee in benefits[benefit_idx_select].pending_requests),
        )
        if empl_idx_select in (-1, -2):
            return NO_EMPLOYEE_MSG if empl_idx_select == -1 else ""

        if not the_company.can_modify("benefits", the_company.employees[empl_idx_select]):
            return "You cannot approve or deny your own request!"

        _bnf = benefits[benefit_idx_select]
        _empl = the_company.employees[empl_idx_select]
        empl_name = FCOLORS.GREEN + _empl.name + FCOLORS.END
        empl_id = FCOLORS.GREEN + _empl.employee_id + FCOLORS.END
        benefit_name = FCOLORS.GREEN + benefits[benefit_idx_select].name + FCOLORS.END

        # get the user's decision
        decision = get_user_option_from_menu(
            f"Select an option for employee {empl_name} ({empl_id})'s pending request for benefit {benefit_name}",
            ["[1] Approve", "[2] Deny", "[3] Cancel"],
        )

        if decision in (-1, -2, 3):
            return "Invalid option!" if decision == -1 else ""

        _bnf.pending_requests.remove(_empl)

        # if admin aprv rqst, add empl to benefit's enrolled empls list
        if decision == 1:
            _bnf.enrolled_employees.append(_empl)
            _empl.benefits.append(_bnf.name)

        # update DB
        if os.getenv("HRMGR_DB") == "TRUE":
            benefit_repo.update_one(
                {"_id": _bnf.id},
                {"$set": _bnf.dict(by_alias=True, include={"pending_requests", "enrolled_employees"})},
                upsert=True,
            )
            employee_repo.update_one(
                {"_id": _empl.id}, {"$set": _empl.dict(include={"benefits"})}, upsert=True
            ) if decision == 1 else None

        return "Employee {}{}{} ({}{}{}) {}{}{} for benefit {}{}{}!".format(
            FCOLORS.GREEN,
            _empl.name,
            FCOLORS.END,
            FCOLORS.GREEN,
            _empl.employee_id,
            FCOLORS.END,
            FCOLORS.GREEN if decision == 1 else FCOLORS.RED,
            "approved" if decision == 1 else "denied",
            FCOLORS.END,
            FCOLORS.GREEN,
            benefits[benefit_idx_select].name,
            FCOLORS.END,
        )

    def __list_employees_without_benefits(self) -> str:
        clrscr()
        print("Employees without benefits:")
        for employee in the_company.employees:
            if len(employee.benefits) == 0:
                print(employee)
        input(ENTER_TO_CONTINUE_MSG)
        return ""
