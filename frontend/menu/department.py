from __future__ import annotations
import sys
import os

from ..helpers import *
from models import Department
from database.mongo import department_repo, employee_repo
from option import Result, Ok

if sys.version_info >= (3, 11):
    from typing import TYPE_CHECKING
else:
    from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Company


class MenuDepartment:
    def __init__(self, company: Company) -> None:
        self.__company = company
        self.__logged_in_employee = company.logged_in_employee

    def admin(self) -> Result[None, str]:
        last_msg: str = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg: str = ""
            department_menu = [
                "[1] Add department",
                "[2] Remove department",
                "[3] Update information for department",
                "[4] Add employee to department",
                "[5] Remove employee from department",
                "[6] View details of department",
                "[7] List all departments",
                "[8] List employees without a department",
                "[9] Back",
            ]

            choice = get_user_option_from_menu("Department management", department_menu)
            match choice:
                case 1:
                    last_msg: str = self.__add()
                case 2:
                    last_msg: str = self.__remove()
                case 3:
                    last_msg: str = self.__update()
                case 4:
                    last_msg: str = self.__add_employee()
                case 5:
                    last_msg: str = self.__remove_employee()
                case 6:
                    last_msg: str = self.__view()
                case 7:
                    last_msg: str = self.__view_all()
                case 8:
                    last_msg: str = self.__view_employees_not_belong_to_any_department()
                case 9:
                    return Ok(None)
                case _:
                    last_msg: str = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def employee(self) -> Result[None, str]:
        last_msg: str = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg: str = ""
            department_menu = [
                "[1] View details of one",
                "[2] List all",
                "[3] Back",
            ]

            choice = get_user_option_from_menu("Department management", department_menu)
            match choice:
                case 1:
                    last_msg: str = self.__view()
                case 2:
                    last_msg: str = self.__view_all()
                case 3:
                    return Ok(None)
                case _:
                    last_msg: str = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def __add(self) -> str:
        # create a new, empty department
        dept = Department()

        # get user input for department name and ID
        if (msg := loop_til_valid_input("Enter department name", dept.set_name)) != "":
            return msg
        if (msg := loop_til_valid_input("Enter department ID", dept.set_id)) != "":
            return msg

        if os.getenv("HRMGR_DB") == "TRUE":
            department_repo.insert_one(dept.dict(by_alias=True))

        # add the department to the company
        self.__company.departments.append(dept)
        return f"Department {FCOLORS.GREEN}{dept.name}{FCOLORS.END} added successfully!"

    def __remove(self) -> str:
        depts = self.__company.departments
        empls = self.__company.employees

        # a list containing the string representation of each department
        dept_items = [f"{dept.name} ({dept.dept_id})" for dept in depts]
        dept_selected_index = get_user_option_from_list(
            "Select a department to remove", dept_items
        )
        if dept_selected_index == -1:
            return NO_DEPARTMENT_MSG
        elif dept_selected_index == -2:
            return ""

        # get the department name and ID to return a message before removing it
        dept_name = depts[dept_selected_index].name
        dept_id = depts[dept_selected_index].dept_id

        # remove the department id from all employees in the department
        for employee in empls:
            if employee.department_id == depts[dept_selected_index].dept_id:
                employee.set_department("").unwrap()
                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one(
                        {"_id": employee.id},
                        {"$set": employee.dict(include={"department_id"})},
                        upsert=True,
                    )

        # remove the department from the company
        del depts[dept_selected_index]
        if os.getenv("HRMGR_DB") == "TRUE":
            department_repo.delete_one({"_id": depts[dept_selected_index].id})

        return f"Department {FCOLORS.RED}{dept_name}{FCOLORS.END} ({FCOLORS.RED}{dept_id}{FCOLORS.END}) removed successfully!"

    def __update(self) -> str:
        depts = self.__company.departments

        # a list containing the string representation of each department
        dept_items = [f"{dept.name} ({dept.dept_id})" for dept in depts]

        # get the index of the department to update
        dept_selected_index = get_user_option_from_list(
            "Select a department to update", dept_items
        )
        if dept_selected_index == -1:
            return NO_DEPARTMENT_MSG
        elif dept_selected_index == -2:
            return ""

        # get the department object to update
        dept = depts[dept_selected_index]

        # re-assign the department name and ID
        if (msg := loop_til_valid_input("Enter department name", dept.set_name)) != "":
            return msg
        if (msg := loop_til_valid_input("Enter department ID", dept.set_id)) != "":
            return msg

        if os.getenv("HRMGR_DB") == "TRUE":
            department_repo.update_one(
                {"_id": dept.id},
                {"$set": dept.dict(exclude={"id"}, by_alias=True)},
                upsert=True,
            )

        return (
            f"Department {FCOLORS.GREEN}{dept.name}{FCOLORS.END} updated successfully!"
        )

    def __add_employee(self) -> str:
        depts = self.__company.departments
        empls = self.__company.employees

        # a list containing the string representation of each department
        dept_items = [f"{dept.name} ({dept.dept_id})" for dept in depts]

        # get the index of the department to update
        dept_selected_index = get_user_option_from_list(
            "Select a department to add an employee to", dept_items
        )
        match dept_selected_index:
            case -1:
                return NO_DEPARTMENT_MSG
            case -2:
                return ""

        # get the index of the employee to add
        employee_items = [
            f"{employee.name} ({employee.employee_id})" for employee in empls
        ]
        employee_selected_index = get_user_option_from_list(
            "Select an employee to add to the department", employee_items
        )
        match employee_selected_index:
            case -1:
                return NO_EMPLOYEE_MSG
            case -2:
                return ""

        if not self.__company.can_modify("department", empls[employee_selected_index]):
            return "You do not have permission to modify this employee's department!"

        # add the employee to the department, department ID to the employee
        employee = empls[employee_selected_index]
        department = depts[dept_selected_index]

        employee.set_department(department.dept_id).unwrap()
        department.members.append(employee)
        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one(
                {"_id": employee.id},
                {"$set": employee.dict(include={"department_id"})},
                upsert=True,
            )
            department_repo.update_one(
                {"_id": department.id},
                {"$set": department.dict(include={"members"})},
                upsert=True,
            )

        return f"Employee {FCOLORS.GREEN}{employee.name}{FCOLORS.END} ({FCOLORS.GREEN}{employee.id}{FCOLORS.END}) added to department {FCOLORS.GREEN}{department.name}{FCOLORS.END} ({FCOLORS.GREEN}{department.id}{FCOLORS.END}) successfully!"

    def __remove_employee(self) -> str:
        depts = self.__company.departments
        empls = self.__company.employees

        # a list containing the string representation of each department
        dept_items = [f"{dept.name} ({dept.dept_id})" for dept in depts]

        # get the index of the department to update
        dept_selected_index = get_user_option_from_list(
            "Select a department to remove an employee from", dept_items
        )
        match dept_selected_index:
            case -1:
                return NO_DEPARTMENT_MSG
            case -2:
                return ""

        department = depts[dept_selected_index]

        # get the index of the employee to remove
        employee_items = [
            f"{employee.name} ({employee.employee_id})"
            for employee in empls
            if employee.department_id == department.dept_id
        ]
        employee_selected_index = get_user_option_from_list(
            "Select an employee to remove from the department", employee_items
        )
        if employee_selected_index == -1:
            return NO_EMPLOYEE_MSG
        elif employee_selected_index == -2:
            return ""

        if not self.__company.can_modify("department", empls[employee_selected_index]):
            return "Only the company owner can manage admins! You can only manage employees."

        employee = empls[employee_selected_index + 1]

        # remove the employee from the department
        employee.set_department("").unwrap()
        department.members.remove(employee)
        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one(
                {"_id": employee.id},
                {"$set": employee.dict(include={"department_id"})},
                upsert=True,
            )
            department_repo.update_one(
                {"_id": department.id},
                {"$set": department.dict(include={"members"})},
                upsert=True,
            )

        return f"Employee {FCOLORS.GREEN}{employee.name}{FCOLORS.END} ({FCOLORS.GREEN}{employee.employee_id}{FCOLORS.END}) removed from department {FCOLORS.GREEN}{department.name}{FCOLORS.END} ({FCOLORS.GREEN}{department.dept_id}{FCOLORS.END}) successfully!"

    def __view(self) -> str:
        depts = self.__company.departments

        if not self.__logged_in_employee.is_admin:
            dept = [
                dept
                for dept in depts
                if dept.dept_id == self.__logged_in_employee.department_id
            ]
            if len(dept) == 0:
                return NO_DEPARTMENT_MSG
            print(dept[0])
        else:
            # a list containing the string representation of each department
            dept_items = [f"{dept.name} ({dept.dept_id})" for dept in depts]

            # get the index of the department to view
            dept_selected_index = get_user_option_from_list(
                "Select a department to view info", dept_items
            )
            if dept_selected_index == -1:
                return NO_DEPARTMENT_MSG
            elif dept_selected_index == -2:
                return ""

            # print the department info
            print(depts[dept_selected_index])
        input(ENTER_TO_CONTINUE_MSG)

    def __view_all(self) -> str:
        dept_items = [
            f"{dept.name} ({dept.dept_id})" for dept in self.__company.departments
        ]
        if len(dept_items) == 0:
            return NO_DEPARTMENT_MSG
        listing("Departments", dept_items)
        return ""

    def __view_employees_not_belong_to_any_department(self) -> str:
        employee_items = [
            f"{employee.name} ({employee.employee_id})"
            for employee in self.__company.employees
            if employee.department_id == ""
        ]
        if len(employee_items) == 0:
            return NO_EMPLOYEE_MSG
        listing("Employees not belong to any department", employee_items)
        return ""
