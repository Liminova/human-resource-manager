from __future__ import annotations
import os

from ..helpers_tui import *
from models import Department, Company
from database.mongo import department_repo, employee_repo  # type: ignore
from option import Result, Ok

the_company: Company = Company()


class MenuDepartment:
    def __init__(self) -> None:
        self.mainloop = self.admin if the_company.logged_in_employee.is_admin else self.employee

    def admin(self) -> Result[None, str]:
        last_msg = ""
        while True:
            last_msg = refresh(last_msg)
            department_menu = [
                "[1] Add/remove/update",
                "[2] Add/remove employee from department",
                "[3] View details",
                "[4] List empls w/o benefit	",
                "[5] Back",
            ]

            choice = get_user_option_from_menu("Department management", department_menu)
            match choice:
                case 1:
                    clrscr()
                    # fmt: off
                    sub_choice = get_user_option_from_menu(
                        "Add/remove/update department",
                        [
                            "[1] Add",
                            "[2] Remove",
                            "[3] Update",
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
                            last_msg = ""
                case 2:
                    clrscr()
                    # fmt: off
                    sub_choice = get_user_option_from_menu(
                        "Add/remove employee from department",
                        [
                            "[1] Add",
                            "[2] Remove",
                            "[else] Back"
                        ]
                    )
                    # fmt: on
                    match sub_choice:
                        case 1:
                            last_msg = self.__add_employee()
                        case 2:
                            last_msg = self.__remove_employee()
                        case _:
                            last_msg = ""
                case 3:
                    last_msg = self.__view()
                case 4:
                    last_msg = self.__view_employees_without_dept()
                case 5:
                    return Ok(None)
                case _:
                    last_msg = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def employee(self) -> Result[None, str]:
        last_msg: str = ""
        while True:
            last_msg = refresh(last_msg)
            # fmt: off
            department_menu = [
                "[1] View details",
                "[3] Back"
            ]
            # fmt: on
            choice = get_user_option_from_menu("Department management", department_menu)
            match choice:
                case 1:
                    last_msg = self.__view()
                case 2:
                    return Ok(None)
                case _:
                    last_msg = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def __add(self) -> str:
        # create a new, empty department
        dept = Department()

        # assign values to the department object
        input_fields = [("Enter department name", dept.set_name), ("Enter department ID", dept.set_id)]
        for promt, setter in input_fields:
            if (msg := loop_til_valid_input(promt, setter)) != "":
                return msg

        # add the department to the company
        the_company.departments.append(dept)
        if os.getenv("HRMGR_DB") == "TRUE":
            department_repo.insert_one(dept.dict(by_alias=True))  # type: ignore

        return f"Department {FCOLORS.GREEN}{dept.name}{FCOLORS.END} added successfully!"

    def __remove(self) -> str:
        depts = the_company.departments
        empls = the_company.employees

        # get the index of the department selected by the user
        dept_idx_select = get_user_option_from_list(
            # "Select a department to remove", [f"{dept.name} ({dept.dept_id})" for dept in depts]
            "Select a department to remove",
            tuple(f"{dept.name} ({dept.dept_id})" for dept in depts),
        )
        if dept_idx_select in (-1, -2):
            return NO_DEPARTMENT_MSG if dept_idx_select == -1 else ""
        _dept = depts[dept_idx_select]

        # remove the department id from all employees in the department
        for emp in empls:
            if emp.department_id != _dept.dept_id:
                continue
            emp.department_id = ""
            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.update_one({"_id": emp.id}, {"$set": emp.dict(exclude={"id"}, by_alias=True)}, upsert=True)

        # remove the department from the company
        depts.remove(_dept)
        if os.getenv("HRMGR_DB") == "TRUE":
            department_repo.delete_one({"_id": _dept.id})

        return f"Department {FCOLORS.RED}{_dept.name}{FCOLORS.END} removed successfully!"

    def __update(self) -> str:
        depts = the_company.departments

        # get the index of the department to update
        dept_idx_select = get_user_option_from_list(
            "Select a department to update", tuple(f"{dept.name} ({dept.dept_id})" for dept in depts)
        )
        if dept_idx_select in (-1, -2):
            return NO_DEPARTMENT_MSG if dept_idx_select == -1 else ""
        _dept = depts[dept_idx_select]

        # get the new values for the department
        input_fields = [("Enter new department name", _dept.set_name), ("Enter new department ID", _dept.set_id)]
        for promt, setter in input_fields:
            if (msg := loop_til_valid_input(promt, setter)) != "":
                return msg

        # update the department in the company
        if os.getenv("HRMGR_DB") == "TRUE":
            department_repo.update_one({"_id": _dept.id}, {"$set": _dept.dict(exclude={"id"}, by_alias=True)}, upsert=True)

        return f"Department {FCOLORS.GREEN}{_dept.name}{FCOLORS.END} updated successfully!"

    def __add_employee(self) -> str:
        depts = the_company.departments
        empls = the_company.employees

        # get the index of the employee selected by the user
        empl_idx_select = get_user_option_from_list(
            "Select an employee to add to a department",
            tuple(f"{employee.name} ({employee.employee_id})" for employee in empls),
        )
        if empl_idx_select in (-1, -2):
            return NO_EMPLOYEE_MSG if empl_idx_select == -1 else ""

        if not the_company.can_modify("department", empls[empl_idx_select]):
            return "Only other admins can manage departments!"

        # get the index of the department selected by the user
        dept_idx_select = get_user_option_from_list(
            "Select a department to add the employee to", tuple(f"{dept.name} ({dept.dept_id})" for dept in depts)
        )
        if dept_idx_select in (-1, -2):
            return NO_DEPARTMENT_MSG if dept_idx_select == -1 else ""

        _dept = depts[dept_idx_select]
        _empl = empls[empl_idx_select]

        # check if the employee is already in the department
        if _empl.department_id == _dept.dept_id:
            return "Employee {}{}{} is already in department {}{}{}!".format(
                FCOLORS.GREEN, _empl.name, FCOLORS.END, FCOLORS.GREEN, _dept.name, FCOLORS.END
            )

        # add the employee to the department and vice versa
        _empl.department_id = _dept.dept_id
        _dept.members.append(_empl)

        # update DB
        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one({"_id": _empl.id}, {"$set": _empl.dict(exclude={"id"}, by_alias=True)}, upsert=True)
            department_repo.update_one({"_id": _dept.id}, {"$set": _dept.dict(exclude={"id"}, by_alias=True)}, upsert=True)

        return f"Employee {FCOLORS.GREEN}{_empl.name}{FCOLORS.END} added to department {FCOLORS.GREEN}{_dept.name}{FCOLORS.END} successfully!"

    def __remove_employee(self) -> str:
        depts = the_company.departments
        empls = the_company.employees

        # get the index of the employee selected by the user
        empl_idx_select = get_user_option_from_list(
            "Select an employee to remove from a department",
            tuple(f"{employee.name} ({employee.employee_id})" for employee in empls),
        )
        if empl_idx_select in (-1, -2):
            return NO_EMPLOYEE_MSG if empl_idx_select == -1 else ""

        # get the index of the department selected by the user
        dept_idx_select = get_user_option_from_list(
            "Select a department to remove the employee from", tuple(f"{dept.name} ({dept.dept_id})" for dept in depts)
        )
        if dept_idx_select in (-1, -2):
            return NO_DEPARTMENT_MSG if dept_idx_select == -1 else ""

        _empl = empls[empl_idx_select]
        _dept = depts[dept_idx_select]

        # remove the employee from the department and vice versa
        if _empl.department_id == "":
            return "Employee {}{}{} is not in a department!".format(FCOLORS.GREEN, _empl.name, FCOLORS.END)
        else:
            _empl.department_id = ""
            _dept.members.remove(_empl)

        # update DB
        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one({"_id": _empl.id}, {"$set": _empl.dict(exclude={"id"}, by_alias=True)}, upsert=True)
            department_repo.update_one({"_id": _dept.id}, {"$set": _dept.dict(exclude={"id"}, by_alias=True)}, upsert=True)

        return "Employee {}{}{} removed from department {}{}{} successfully!".format(
            FCOLORS.GREEN, _empl.name, FCOLORS.END, FCOLORS.GREEN, _dept.name, FCOLORS.END
        )

    def __view(self) -> str:
        depts = the_company.departments

        # get the index of the department from the user
        dept_idx_select = get_user_option_from_list(
            "Select a department to view info", tuple(f"{dept.name} ({dept.dept_id})" for dept in depts)
        )
        if dept_idx_select in (-1, -2):
            return NO_DEPARTMENT_MSG if dept_idx_select == -1 else ""
        _dept = the_company.departments[dept_idx_select]

        # print the department info
        clrscr()
        print(_dept)
        input(ENTER_TO_CONTINUE_MSG)

        return ""

    def __view_employees_without_dept(self) -> str:
        empls = the_company.employees
        if len(empls) == 0:
            return NO_EMPLOYEE_MSG

        clrscr()
        for empl in empls:
            if empl.department_id == "":
                print(empl)
                print("")
        input(ENTER_TO_CONTINUE_MSG)

        return ""
