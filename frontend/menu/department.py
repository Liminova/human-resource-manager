from __future__ import annotations
import sys
import os

from ..helpers import *
from models import Department
from database.mongo import department_repo, employee_repo # type: ignore
from option import Result, Ok

if sys.version_info >= (3, 11):
    from typing import TYPE_CHECKING
else:
    from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from ...models.company import Company

class MenuDepartment:
    def __init__(self, company: Company) -> None:
        self.__company = company

    def start(self) -> Result[None, str]:
        last_msg = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg = ""
            department_menu = [
                "[1] Add",
                "[2] Remove",
                "[3] Update information for one",
                "[4] Add employee to one",
                "[5] Remove employee from one",
                "[6] View details of one",
                "[7] List all",
                "[8] Back",
            ]

            choice = get_user_option_from_menu("Department management", department_menu)
            if (choice in range(2, 6)) and (not self.__company.departments):
                last_msg = NO_DEPARTMENT_MSG
                continue

            match choice:
                case 1: last_msg = self.__add()
                case 2: last_msg = self.__remove()
                case 3: last_msg = self.__update()
                case 4: last_msg = self.__add_employee()
                case 5: last_msg = self.__remove_employee()
                case 6: last_msg = self.__view()
                case 7: last_msg = self.__view_all()
                case 8: return Ok(None)
                case _: last_msg = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def __add(self) -> str:
        # create a new, empty department
        dept = Department()

        # get user input for department name and ID
        if (msg := loop_til_valid_input("Enter department name", dept.set_name)) != "":
            return msg
        if (msg := loop_til_valid_input("Enter department ID", dept.set_id)) != "":
            return msg

        if os.getenv("HRMGR_DB") == "TRUE":
            department_repo.insert_one(dept.dict(by_alias=True)) # type: ignore

        # add the department to the company
        self.__company.departments.append(dept)
        return f"Department {FCOLORS.GREEN}{dept.name}{FCOLORS.END} added successfully!"

    def __remove(self) -> str:
        # a list containing the string representation of each department
        dept_items = [f"{dept.name} ({dept.dept_id})" for dept in self.__company.departments]
        dept_selected_index = get_user_option_from_list("Select a department to remove", dept_items)
        if dept_selected_index == -1:
            return NO_DEPARTMENT_MSG
        elif dept_selected_index == -2:
            return ""

        # get the department name and ID to return a message before removing it
        dept_name = self.__company.departments[dept_selected_index].name
        dept_id = self.__company.departments[dept_selected_index].dept_id

        # remove the department id from all employees in the department
        for employee in self.__company.employees:
            if employee.department_id == self.__company.departments[dept_selected_index].dept_id:
                employee.department_id = ""
                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one(
                        { "_id": employee.id },
                        { "$set": employee.dict(exclude={"id"}, by_alias=True) },
                        upsert=True,
                    )

        # remove the department from the company
        del self.__company.departments[dept_selected_index]
        if os.getenv("HRMGR_DB") == "TRUE":
            department_repo.delete_one({ "_id": self.__company.departments[dept_selected_index].id })

        return f"Department {FCOLORS.RED}{dept_name}{FCOLORS.END} ({FCOLORS.RED}{dept_id}{FCOLORS.END}) removed successfully!"

    def __update(self) -> str:
        depts = self.__company.departments

        # a list containing the string representation of each department
        dept_items = [f"{dept.name} ({dept.dept_id})" for dept in self.__company.departments]

        # get the index of the department to update
        dept_selected_index = get_user_option_from_list("Select a department to update", dept_items)
        if dept_selected_index == -1:
            return NO_DEPARTMENT_MSG
        elif dept_selected_index == -2:
            return ""

        # get the department object to update
        dept = self.__company.departments[dept_selected_index]

        # re-assign the department name and ID
        if (msg := loop_til_valid_input("Enter department name", dept.set_name)) != "":
            return msg
        if (msg := loop_til_valid_input("Enter department ID", dept.set_id)) != "":
            return msg

        if os.getenv("HRMGR_DB") == "TRUE":
            department_repo.update_one(
                { "_id": dept.id },
                { "$set": dept.dict(exclude={"id"}, by_alias=True) },
                upsert=True
            )

        return f"Department {FCOLORS.GREEN}{dept.name}{FCOLORS.END} updated successfully!"

    def __add_employee(self) -> str:
        # a list containing the string representation of each department
        dept_items = [f"{dept.name} ({dept.dept_id})" for dept in self.__company.departments]

        # get the index of the department to update
        dept_selected_index = get_user_option_from_list("Select a department to add an employee to", dept_items)
        if dept_selected_index == -1:
            return NO_DEPARTMENT_MSG
        elif dept_selected_index == -2:
            return ""

        # get the index of the employee to add
        employee_items = [f"{employee.name} ({employee.employee_id})" for employee in self.__company.employees]
        employee_selected_index = get_user_option_from_list("Select an employee to add to the department", employee_items)
        if employee_selected_index == -1:
            return NO_EMPLOYEE_MSG
        elif employee_selected_index == -2:
            return ""

        # add the employee to the department, department ID to the employee
        self.__company.employees[employee_selected_index].department_id = self.__company.departments[dept_selected_index].dept_id
        self.__company.departments[dept_selected_index].members.append(self.__company.employees[employee_selected_index])
        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one(
                { "_id": self.__company.employees[employee_selected_index].id },
                { "$set": self.__company.employees[employee_selected_index].dict(exclude={"id"}, by_alias=True) },
                upsert=True,
            )
            department_repo.update_one(
                { "_id": self.__company.departments[dept_selected_index].id },
                { "$set": self.__company.departments[dept_selected_index].dict(exclude={"id"}, by_alias=True) },
                upsert=True,
            )

        employee_name = self.__company.employees[employee_selected_index].name
        employee_id = self.__company.employees[employee_selected_index].employee_id
        dept_name = self.__company.departments[dept_selected_index].name
        dept_id = self.__company.departments[dept_selected_index].dept_id
        return f"Employee {FCOLORS.GREEN}{employee_name}{FCOLORS.END} ({FCOLORS.GREEN}{employee_id}{FCOLORS.END}) added to department {FCOLORS.GREEN}{dept_name}{FCOLORS.END} ({FCOLORS.GREEN}{dept_id}{FCOLORS.END}) successfully!"

    def __remove_employee(self) -> str:
        # a list containing the string representation of each department
        dept_items = [f"{dept.name} ({dept.dept_id})" for dept in self.__company.departments]

        # get the index of the department to update
        dept_selected_index = get_user_option_from_list("Select a department to remove an employee from", dept_items)
        if dept_selected_index == -1:
            return NO_DEPARTMENT_MSG
        elif dept_selected_index == -2:
            return ""

        # get the index of the employee to remove
        employee_items = [f"{employee.name} ({employee.employee_id})" for employee in self.__company.employees if employee.department_id == self.__company.departments[dept_selected_index].dept_id]
        employee_selected_index = get_user_option_from_list("Select an employee to remove from the department", employee_items)
        if employee_selected_index == -1:
            return NO_EMPLOYEE_MSG
        elif employee_selected_index == -2:
            return ""

        # get the actual employee, department names, and IDs to print before removing
        employee_name = self.__company.employees[employee_selected_index].name
        employee_id = self.__company.employees[employee_selected_index].employee_id
        dept_name = self.__company.departments[dept_selected_index].name
        dept_id = self.__company.departments[dept_selected_index].dept_id

        # remove the employee from the department
        self.__company.employees[employee_selected_index].department_id = ""
        self.__company.departments[dept_selected_index].members.remove(self.__company.employees[employee_selected_index])
        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one(
                { "_id": self.__company.employees[employee_selected_index].id },
                { "$set": self.__company.employees[employee_selected_index].dict(exclude={"id"}, by_alias=True) },
                upsert=True,
            )
            department_repo.update_one(
                { "_id": self.__company.departments[dept_selected_index].id },
                { "$set": self.__company.departments[dept_selected_index].dict(exclude={"id"}, by_alias=True) },
                upsert=True,
            )

        return f"Employee {FCOLORS.GREEN}{employee_name}{FCOLORS.END} ({FCOLORS.GREEN}{employee_id}{FCOLORS.END}) removed from department {FCOLORS.GREEN}{dept_name}{FCOLORS.END} ({FCOLORS.GREEN}{dept_id}{FCOLORS.END}) successfully!"


    def __view(self) -> str:
        # a list containing the string representation of each department
        dept_items = [f"{dept.name} ({dept.dept_id})" for dept in self.__company.departments]

        # get the index of the department to update
        dept_selected_index = get_user_option_from_list("Select a department to view info", dept_items)
        if dept_selected_index == -1:
            return NO_DEPARTMENT_MSG
        elif dept_selected_index == -2:
            return ""

        # print the department info
        print(self.__company.departments[dept_selected_index])
        input(ENTER_TO_CONTINUE_MSG)

    def __view_all(self) -> str:
        dept_items = [f"{dept.name} ({dept.dept_id})" for dept in self.__company.departments]
        if len(dept_items) == 0:
            return NO_DEPARTMENT_MSG
        listing("Departments", dept_items)
        return ""