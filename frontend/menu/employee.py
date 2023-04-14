from __future__ import annotations
import sys
import os

from ..helpers import *
from models import Employee, hash
from database.mongo import employee_repo, benefit_repo, department_repo  # type: ignore
from option import Result, Ok

if sys.version_info >= (3, 11):
    from typing import TYPE_CHECKING
else:
    from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Company


class MenuEmployee:
    def __init__(self, company: Company):
        self.__company = company

    def admin(self) -> Result[None, str]:
        last_msg: str = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg: str = ""

            employee_menu = [
                "[1] Add employee",
                "[2] Remove employee",
                "[3] Update information",
                "[4] View details of employee",
                "[5] Change password",
                "[6] List all employees",
                "[7] Back",
            ]
            choice = get_user_option_from_menu("Employee management", employee_menu)

            if (choice not in [1, 6]) and (not self.__company.employees):
                last_msg: str = NO_EMPLOYEE_MSG
                continue

            match choice:
                case 1:
                    last_msg: str = self.__add()
                case 2:
                    last_msg: str = self.__remove()
                case 3:
                    last_msg: str = self.__update()
                case 4:
                    last_msg: str = self.__view()
                case 5:
                    last_msg: str = self.__view_all()
                case 6:
                    last_msg: str = self.__change_password()
                case 7:
                    return Ok(None)
                case _:
                    last_msg: str = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def employee(self) -> Result[None, str]:
        logged_in_employee = self.__company.logged_in_employee
        last_msg: str = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg: str = ""

            employee_menu = [
                "[1] View details",
                "[2] Change password",
                "[3] Back",
            ]
            choice = get_user_option_from_menu(
                "Employee management for " + logged_in_employee.name, employee_menu
            )
            match choice:
                case 1:
                    last_msg: str = self.__view()
                case 2:
                    last_msg: str = self.__change_password()
                case 3:
                    return Ok(None)
                case _:
                    last_msg: str = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def __add(self) -> str:
        depts = self.__company.departments

        # create a new, empty employee
        employee = Employee()

        # get user input for employee name, date of birth, ID, phone number, and email
        fields_data = [
            ("Enter employee name", employee.set_name),
            ("Enter employee date of birth (YYYY-MM-DD)", employee.set_dob),
            ("Enter employee ID", employee.set_id),
            ("Enter employee phone number", employee.set_phone),
            ("Enter employee email", employee.set_email),
            ("Enter employee password", employee.set_password),
        ]
        for field, setter in fields_data:
            if (msg := loop_til_valid_input(field, setter)) != "":
                return msg
        employee.is_admin = False

        # a list containing the string representation of each department
        dept_items = [f"{dept.name} ({dept.dept_id})" for dept in depts]

        if len(dept_items) > 0:
            # get the index of the department to add the employee to
            dept_index = get_user_option_from_list(
                "Select a department to add the employee to", dept_items
            )
            dept = depts[dept_index]
            if dept_index == -1:
                return NO_DEPARTMENT_MSG
            elif dept_index == -2:
                return ""

            # add the employee to the department's members
            dept.members.append(employee)
            if os.getenv("HRMGR_DB") == "TRUE":
                department_repo.update_one(
                    {"_id": dept.id},
                    {"$set": dept.dict(include={"members"})},
                    upsert=True,
                )

            # add the department id to the employee's department_id
            employee.set_department(depts[dept_index].dept_id).unwrap()

        # append the employee to the company's employees
        self.__company.employees.append(employee)

        # add employee to mongodb database
        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.insert_one(employee.dict(by_alias=True))  # type: ignore

        return f"Employee {FCOLORS.GREEN}{employee.name}{FCOLORS.END} ({FCOLORS.GREEN}{employee.employee_id}{FCOLORS.END}) added successfully!"

    def __remove(self) -> str:
        # a list containing the string representation of each employee that isn't an admin
        employee_items = [
            f"{e.name} ({e.employee_id})"
            for e in self.__company.employees
            if not e.is_admin
        ]

        # get the index of the employee to remove
        employee_index = get_user_option_from_list(
            "Select an employee to remove", employee_items
        )
        if employee_index == -1:
            return NO_EMPLOYEE_MSG
        elif employee_index == -2:
            return ""

        # get the actual employee
        employee = self.__company.employees[employee_index]

        # if employee.is_admin and not self.__company.owner:
        if not self.__company.can_modify("employee", employee):
            return "Only the owner can remove admins!"

        # remove employee from the department they're in
        for dept in self.__company.departments:
            if employee in dept.members:
                dept.members.remove(employee)
                if os.getenv("HRMGR_DB") == "TRUE":
                    department_repo.update_one(
                        {"_id": dept.id},
                        {"$set": dept.dict(exclude={"id"}, by_alias=True)},
                        upsert=True,
                    )

        # remove employee from the benefits they're enrolled in
        for benefit in self.__company.benefits:
            if employee in benefit.enrolled_employees:
                benefit.enrolled_employees.remove(employee)
                if os.getenv("HRMGR_DB") == "TRUE":
                    benefit_repo.update_one(
                        {"_id": benefit.id},
                        {"$set": benefit.dict(exclude={"id"}, by_alias=True)},
                        upsert=True,
                    )

        # remove from the company
        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.delete_one({"_id": employee.id})
        del self.__company.employees[employee_index]

        return f"Employee {FCOLORS.RED}{employee.name}{FCOLORS.END} ({FCOLORS.RED}{employee.employee_id}{FCOLORS.END}) removed successfully!"

    def __update(self) -> str:
        # a list containing the string representation of each employee
        employee_items = [
            f"{e.name} ({e.employee_id})" for e in self.__company.employees
        ]

        # get the employee to update
        selected_employee_index = get_user_option_from_list(
            "Select an employee to update", employee_items
        )
        if selected_employee_index == -1:
            return NO_EMPLOYEE_MSG
        elif selected_employee_index == -2:
            return ""

        # get the actual employee object
        employee = self.__company.employees[selected_employee_index]

        # get the new data
        fields_data = [
            ("Enter employee name", employee.set_name),
            ("Enter employee date of birth (YYYY-MM-DD)", employee.set_dob),
            ("Enter employee ID", employee.set_id),
            ("Enter employee phone number", employee.set_phone),
            ("Enter employee email", employee.set_email),
            ("Enter employee password", employee.set_password),
        ]
        for field, setter in fields_data:
            if (msg := loop_til_valid_input(field, setter)) != "":
                return msg

        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one(
                {"_id": employee.id},
                {"$set": employee.dict(exclude={"id"}, by_alias=True)},
                upsert=True,
            )

        return f"Employee {FCOLORS.GREEN}{employee.name}{FCOLORS.END} ({FCOLORS.GREEN}{employee.employee_id}{FCOLORS.END}) updated successfully!"

    def __view(self) -> str:
        empls = self.__company.employees

        logged_in_employee = self.__company.logged_in_employee
        if not logged_in_employee.is_admin:
            print(logged_in_employee)
            input(ENTER_TO_CONTINUE_MSG)
            return ""

        # a list containing the string representation of each employee
        employee_items = [f"{e.name} ({e.employee_id})" for e in empls]

        # get the employee to view
        selected_employee_index = get_user_option_from_list(
            "Select an employee to view", employee_items
        )
        if selected_employee_index == -1:
            return NO_EMPLOYEE_MSG
        elif selected_employee_index == -2:
            return ""

        # print the employee
        print(empls[selected_employee_index])
        input(ENTER_TO_CONTINUE_MSG)
        return ""

    def __view_all(self) -> str:
        # a list containing the string representation of each employee
        employee_items = [
            f"{e.name} ({e.employee_id})" for e in self.__company.employees
        ]

        # print the list
        listing("Employees", employee_items)
        return ""

    def __change_password(self) -> str:
        empls = self.__company.employees

        # as an admin
        logged_in_employee = self.__company.logged_in_employee
        if logged_in_employee.is_admin:
            # return "You must be logged in to change your password"
            empl_items = [
                f"{e.name} ({e.employee_id})" for e in empls if not e.is_admin
            ]
            empl_index = get_user_option_from_list(
                "Select an employee to change the password of", empl_items
            )
            if empl_index == -1:
                return NO_EMPLOYEE_MSG
            elif empl_index == -2:
                return ""

            # get the employee
            employee = empls[empl_index]

            if not self.__company.can_modify("password", employee):
                return "Only the owner or an admin can change another admin's password"

            # get the new password
            new_password = input("Enter new password, or leave blank to cancel")
            if new_password == "":
                return ""

            # re-enter the new password
            new_password_verify = input(
                "Re-enter new password, or leave blank to cancel"
            )
            if new_password_verify == "":
                return ""

            # check if the new passwords match
            if new_password != new_password_verify:
                return "Passwords do not match"

            # confirm
            if (
                input(
                    f"Are you sure you want to change {employee.name}'s password? (y/n): "
                ).lower()
                != "y"
            ):
                return ""

            # change the password
            employee.set_password(new_password)
            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.update_one(
                    {"_id": employee.id},
                    {"$set": employee.dict(include={"hashed_password"})},
                    upsert=True,
                )

        # as an employee
        else:
            # get the old password
            old_password = input("Enter old password, or leave blank to cancel: ")
            if old_password == "":
                return ""

            # check if the old password is correct
            empl_id = logged_in_employee.employee_id
            if hash(empl_id, old_password) != logged_in_employee.hashed_password:
                return "Incorrect password"

            # get the new password
            new_password = input("Enter new password, or leave blank to cancel")
            if new_password == "":
                return ""

            # re-enter the new password
            new_password_verify = input(
                "Re-enter new password, or leave blank to cancel"
            )
            if new_password_verify == "":
                return ""

            # check if the new passwords match
            if new_password != new_password_verify:
                return "Passwords do not match"

            # confirm
            if (
                input("Are you sure you want to change your password? (y/n): ").lower()
                != "y"
            ):
                return ""

            # change the password
            logged_in_employee.hashed_password = hash(
                logged_in_employee.employee_id, new_password
            )
            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.update_one(
                    {"_id": logged_in_employee.id},
                    {"$set": logged_in_employee.dict(include={"hashed_password"})},
                    upsert=True,
                )
