from __future__ import annotations

import sys
import os
import textwrap

from frontend.helpers import *
from frontend.tui import *
from models import Company, Employee, BenefitPlan, Department
from dotenv import load_dotenv
from database.mongo import employee_repo, department_repo, benefit_repo
from option import Result, Ok

load_dotenv()

the_company = Company()


def initialize_data():
    os.environ["HRMGR_DB"] = "TRUE"

    if not employee_repo.find({}):
        pass
    else:
        for employee in employee_repo.find({}):
            the_company.employees.append(Employee.parse_obj(employee))

    if not department_repo.find({}):
        pass
    else:
        for department in department_repo.find({}):
            the_company.departments.append(Department.parse_obj(department))

    if not benefit_repo.find({}):
        pass
    else:
        for benefit in benefit_repo.find({}):
            the_company.benefits.append(BenefitPlan.parse_obj(benefit))


def main():
    last_msg: str = ""
    if (
        not os.getenv("MONGO_USER")
        or not os.getenv("MONGO_PASS")
        or not os.getenv("MONGO_URI")
    ):
        os.environ["HRMGR_DB"] = "FALSE"
        input(
            textwrap.dedent(
                """\
            It seems like your environment variables are not set up.
            The program will now run in memory-only mode.
            Press any key to continue."""
            )
        )
    else:
        initialize_data()

    # ======================
    #    WELCOME SCREEN
    # ======================

    if len(the_company.employees) == 0:
        print(
            textwrap.dedent(
                """\
            Welcome to HR Manager!
            It seems like this is your first time using this program.
            You will be asked to create an admin account."""
            )
        )
        input(ENTER_TO_CONTINUE_MSG)
    else:
        first_account_is_admin = the_company.employees[0].is_admin
        first_account_name_is_owner = the_company.employees[0].name == "Owner"
        only_one_owner = (
            len(
                [
                    employee
                    for employee in the_company.employees
                    if employee.name == "Owner"
                ]
            )
            == 1
        )
        if not first_account_is_admin:
            print(
                FCOLORS.RED
                + "WARNING: The first account is not an admin! Contact the IT department immediately!"
                + FCOLORS.END
            )
            raise KeyboardInterrupt
        if not first_account_name_is_owner:
            print(
                FCOLORS.RED
                + "WARNING: The first account's name is not 'Owner'! Contact the IT department immediately!"
                + FCOLORS.END
            )
            raise KeyboardInterrupt
        elif not only_one_owner:
            print(
                FCOLORS.RED
                + "WARNING: There are more than one owner accounts! Contact the IT department immediately!"
                + FCOLORS.END
            )
            raise KeyboardInterrupt

    # ==========================
    #       LOGIN/SIGNUP
    # ==========================

    menu_login_signup = MenuLoginSignup()
    is_logged_in = False
    if len(the_company.employees) == 0:
        is_logged_in = menu_login_signup.signup_admin()
    else:
        is_logged_in = menu_login_signup.login()
    if not is_logged_in:
        raise KeyboardInterrupt

    # ==========================
    #        MAIN MENU
    # ==========================

    while is_logged_in:
        clrscr()
        last_msg: str = ""
        if last_msg:
            print(last_msg)
            last_msg: str = ""
        main_menu = [
            "[1] Employee management",
            "[2] Benefit plan management",
            "[3] Attendance management",
            "[4] Payroll management",
            "[5] Department management",
            "[6] Performance management",
            "[7] Exit",
        ]
        user_choice = get_user_option_from_menu("Main menu", main_menu)

        if user_choice in [3, 4, 6] and not the_company.employees:
            last_msg: str = NO_EMPLOYEE_MSG
            continue

        respond: Result[None, str] = Ok(None)
        match user_choice:
            case 1:
                respond = MenuEmployee().mainloop()
            case 2:
                respond = MenuBenefits().mainloop()
            case 3:
                respond = MenuAttendance().mainloop()
            case 4:
                respond = MenuPayroll().mainloop()
            case 5:
                respond = MenuDepartment().mainloop()
            case 6:
                respond = MenuPerformance().mainloop()
            case 7:
                break
            case _:
                last_msg: str = FCOLORS.RED + "Invalid choice!" + FCOLORS.END
        try:
            respond.unwrap()
        except (ValueError, TypeError) as e:
            last_msg: str = str(e)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
