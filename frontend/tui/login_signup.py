from __future__ import annotations
import os

from ..helpers import *
from models import Employee, Company, validate, hash
from database.mongo import employee_repo
from getpass import getpass

the_company: Company = Company()


class MenuLoginSignup:
    def login(self) -> bool:
        last_msg = ""
        while True:
            last_msg = refresh(last_msg)
            print(f"{FCOLORS.PURPLE}Employee login{FCOLORS.END}")
            print("Please contact the admin if you don't have an account yet.")
            print(FCOLORS.CYAN + ("=" * 58) + FCOLORS.END)

            employee_id = input("Employee ID, or leave blank to go back: ")
            if not employee_id:
                return False

            # key = employee_id, value = employee object
            employees: dict[str, Employee] = {}
            for employee in the_company.employees:
                employees[employee.employee_id] = employee

            if employee_id not in employees.keys():
                last_msg: str = FCOLORS.RED + "Employee ID not found!" + FCOLORS.END
                continue

            input_password = getpass("Password, or leave blank to go back: ")
            if not input_password:
                return False

            # validate password
            if not validate(employee_id, input_password, employees[employee_id].hashed_password):
                last_msg: str = FCOLORS.RED + "Invalid password!" + FCOLORS.END
                continue

            # login
            the_company.logged_in_employee = employees[employee_id]
            return True

    def signup_admin(self) -> bool:
        # the admin is the first employee to be added to the company so no need to check if there are any employees
        if the_company.employees:
            return False

        last_msg = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg = ""
            print(f"{FCOLORS.PURPLE}Admin signup{FCOLORS.END}")
            print(FCOLORS.CYAN + ("=" * 12) + FCOLORS.END)

            admin_username = input("Admin username, or leave blank to go back: ")
            if not admin_username:
                return False

            password = getpass("Password, or leave blank to go back: ")
            if not password:
                return False

            password_confirm = getpass("Confirm password, or leave blank to go back: ")
            if not password_confirm:
                return False

            if password != password_confirm:
                last_msg: str = FCOLORS.RED + "Passwords do not match!" + FCOLORS.END
                continue

            # create the owner
            owner = Employee()
            owner.employee_id = admin_username
            owner.hashed_password = hash(admin_username, password)
            owner.is_admin = True
            owner.name = "Owner"

            the_company.employees.append(owner)
            the_company.logged_in_employee = owner

            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.insert_one(owner.dict(by_alias=True))
            return True
