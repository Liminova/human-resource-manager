from __future__ import annotations
import sys
from ..helpers import *
from models import Department
if sys.version_info >= (3, 11):
    from typing import TYPE_CHECKING
else:
    from typing_extensions import TYPE_CHECKING
if TYPE_CHECKING:
    from ...models.company import Company

class MenuDepartment:
    def __init__(self, company: Company) -> None:
        self.__company = company

    def start(self) -> tuple[bool, str]:
        depts = self.__company.departments

        last_msg = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg = ""
            department_menu = [
                "[1] Add department",
                "[2] Remove department",
                "[3] Update department",
                "[4] View department",
                "[5] View all departments",
                "[6] Back",
            ]

            choice = get_user_option_from_menu("Department management", department_menu)
            if (choice in range(2, 6)) and (not depts):
                last_msg = "No departments to manage, please add a department first!"
                continue

            match choice:
                case 1: last_msg = self.__add()
                case 2: last_msg = self.__remove()
                case 3: last_msg = self.__update()
                case 4: last_msg = self.__view()
                case 5: listing("Departments", [f"{dept.name} ({dept.id})" for dept in depts])
                case 6: return True, ""
                case _: continue

    def __add(self) -> str:
        # create a new, empty department
        dept = Department()

        # get user input for department name and ID
        loop_til_valid_input("Enter department name: ", dept.set_name)
        loop_til_valid_input("Enter department ID: ", dept.set_id)

        # add the department to the company
        self.__company.departments.append(dept)
        return f"Department {FCOLORS.GREEN}{dept.name}{FCOLORS.END} added successfully!"

    def __remove(self) -> str:
        depts = self.__company.departments
        employees = self.__company.employees

        # a list containing the string representation of each department
        dept_items = [f"{dept.name} ({dept.id})" for dept in self.__company.departments]
        dept_selected_index = get_user_option_from_list("Select a department to remove", dept_items)
        dept = depts[dept_selected_index - 1]
        if dept_selected_index == -1:
            return ""

        # remove the department from whatever employee it's applied to
        for employee in employees:
            if employee.department == depts[dept_selected_index]:
                employee.set_department(None)

        depts.pop(dept_selected_index)
        return "Department removed successfully!"

    def __update(self) -> str:
        depts = self.__company.departments

        # a list containing the string representation of each department
        dept_items = [f"{dept.name} ({dept.id})" for dept in self.__company.departments]

        # get the index of the department to update
        dept_selected_index = get_user_option_from_list("Select a department to update", dept_items)
        if dept_selected_index == -1:
            return ""

        # get the department object to update
        dept = depts[dept_selected_index - 1]
        
        department_repo.update_one({ "_id": dept.id }, dept.dict(exclude={"id"}, by_alias=True))

        # re-assign the department name and ID
        loop_til_valid_input("Enter department name: ", dept.set_name)
        loop_til_valid_input("Enter department ID: ", dept.set_id)
        return f"Department {FCOLORS.GREEN}{dept.name}{FCOLORS.END} updated successfully!"

    def __view(self) -> str:
        depts = self.__company.departments

        # a list containing the string representation of each department
        dept_items = [f"{dept.name} ({dept.id})" for dept in self.__company.departments]

        # get the index of the department to update
        dept_selected_index = get_user_option_from_list("Select a department to view info", dept_items)
        if dept_selected_index == -1:
            return ""

        # print the department info
        print(depts[dept_selected_index])
        input("Press enter to continue...")