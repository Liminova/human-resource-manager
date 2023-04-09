from __future__ import annotations
import sys
from ..helpers import *
from models import Employee
from database.mongo import employee_repo

if sys.version_info >= (3, 11):
    from typing import TYPE_CHECKING
else:
    from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from ...models.company import Company

class MenuEmployee:
    def __init__(self, company: Company):
        self.__company = company

    def start(self) -> tuple[bool, str]:
        depts = self.__company.departments
        employees = self.__company.employees

        if not depts:
            return False, "No departments available! Please add a department first."

        last_msg = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg = ""

            employee_menu = [
                "[1] Add employee",
                "[2] Remove employee",
                "[3] Update employee",
                "[4] View employee",
                "[5] View all employees",
                "[6] Back",
            ]
            choice = get_user_option_from_menu("Employee management", employee_menu)

            if (choice not in [1, 6]) and (not employees):
                last_msg = "No employees available! Please add an employee first."
                continue

            match choice:
                case 1: last_msg = self.__add()
                case 2: last_msg = self.__remove()
                case 3: last_msg = self.__update()
                case 4: last_msg = self.__view()
                case 5: last_msg = self.__view_all()
                case _:
                    return True, ""

    def __add(self) -> str:
        # create a new, empty employee
        employee = Employee()

        # get user input for employee name, date of birth, ID, phone number, and email
        fields_data = [
            ("Enter employee name: ", employee.set_name),
            ("Enter employee date of birth (YYYY-MM-DD): ", employee.set_dob),
            ("Enter employee ID: ", employee.set_id),
            ("Enter employee phone number: ", employee.set_phone),
            ("Enter employee email: ", employee.set_email),
        ]
        for (field, setter) in fields_data:
            loop_til_valid_input(field, setter)

        # a list containing the string representation of each department
        dept_items = [f"{dept.name} ({dept.id})" for dept in self.__company.departments]

        # get the index of the department to add the employee to
        dept_index = get_user_option_from_list("Select a department to add the employee to", dept_items)
        if dept_index == -1:
            return ""

        # add the employee to the department's members
        self.__company.departments[dept_index].members.append(employee)

        # add the department id to the employee's department_id
        employee.department_id = self.__company.departments[dept_index].dept_id

        # append the employee to the company's employees
        self.__company.employees.append(employee)

        # add employee to mongodb database
        employee_repo.insert_one(employee.dict(by_alias=True))

        return f"Employee {employee.name} ({employee.employee_id}) added successfully!"

    def __remove(self) -> str:
        employees = self.__company.employees
        depts = self.__company.departments
        benefits = self.__company.benefits

        # a list containing the string representation of each employee
        employee_items = [f"{employee.name} ({employee.employee_id})" for employee in employees]

        # get the index of the employee to remove
        employee_index = get_user_option_from_list("Select an employee to remove", employee_items)
        if employee_index == -1:
            return ""

        employee = employees[employee_index - 1]

        # remove from whatever department they're in
        for dept in depts:
            if employee in dept.members:
                dept.members.remove(employees[employee_index])

        # remove from whatever benefit plan they're in
        for benefit in benefits:
            if employee in benefit.enrolled_employees:
                benefit.enrolled_employees.remove(employees[employee_index])

        # remove from the company
        employee_repo.delete_one({ "_id": employee.id })
        del employees[employee_index - 1]

        return f"Employee {employee.name} ({employee.employee_id}) removed successfully!"

    def __update(self) -> str:
        employees = self.__company.employees

        # a list containing the string representation of each employee
        employee_items = [f"{employee.name} ({employee.employee_id})" for employee in employees]

        # get the employee to update
        selected_employee_index = get_user_option_from_list("Select an employee to update", employee_items)
        if selected_employee_index == -1:
            return ""

        # get the actual employee object
        employee = employees[selected_employee_index]

        # get the new data
        fields_data = [
            ("Enter employee name: ", employee.set_name),
            ("Enter employee date of birth (YYYY-MM-DD): ", employee.set_dob),
            ("Enter employee ID: ", employee.set_id),
            ("Enter employee phone number: ", employee.set_phone),
            ("Enter employee email: ", employee.set_email),
        ]
        for (field, setter) in fields_data:
            loop_til_valid_input(field, setter)

        employee_repo.update_one({ "_id": employee.id }, employee.dict(exclude={"id"}, by_alias=True))

        return f"Employee {employee.name} ({employee.employee_id}) updated successfully!"

    def __view(self) -> str:
        employees = self.__company.employees

        # a list containing the string representation of each employee
        employee_items = [f"{employee.name} ({employee.employee_id})" for employee in employees]

        # get the employee to view
        selected_employee_index = get_user_option_from_list("Select an employee to view", employee_items)
        if selected_employee_index == -1:
            return ""

        # print the employee
        print(employees[selected_employee_index])
        input("\nPress enter to continue...")
        return ""

    def __view_all(self) -> str:
        employees = self.__company.employees

        # a list containing the string representation of each employee
        employee_items = [f"{employee.name} ({employee.employee_id})" for employee in employees]

        # print the list
        listing("Employees", employee_items)
        return ""
