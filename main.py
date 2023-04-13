import sys
import os
import textwrap

from frontend.helpers import *
from frontend.menu import *
from models import Company, BenefitPlan, Department, Employee
from dotenv import load_dotenv
from database.mongo import employee_repo, department_repo, benefit_repo # type: ignore
from option import Result, Ok

load_dotenv()

the_company = Company()

def initialize_data():
    os.environ["HRMGR_DB"] = "TRUE"

    if not employee_repo.find({}):
        pass
    else:
        for employee in employee_repo.find({}): # type: ignore
            the_company.employees.append(Employee.parse_obj(employee))

    if not department_repo.find({}):
        pass
    else:
        for department in department_repo.find({}): # type: ignore
            the_company.departments.append(Department.parse_obj(department))

    if not benefit_repo.find({}):
        pass
    else:
        for benefit in benefit_repo.find({}): # type: ignore
            the_company.benefits.append(BenefitPlan.parse_obj(benefit))

def main_tui():
    last_msg: str = ""
    if not os.getenv("MONGO_USER") or not os.getenv("MONGO_PASS") or not os.getenv("MONGO_URI"):
        os.environ["HRMGR_DB"] = "FALSE"
        input(textwrap.dedent("""\
            It seems like your environment variables are not set up.
            The program will now run in memory-only mode.
            Press any key to continue."""))
    else:
        initialize_data()

    while True:
        clrscr()
        if last_msg:
            print(last_msg)
            last_msg = ""
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
            last_msg = NO_EMPLOYEE_MSG
            continue

        respond: Result[bool, str] = Ok(None)
        match user_choice:
            case 1: respond = MenuEmployee(the_company).start()
            case 2: respond = MenuBenefits(the_company).start()
            case 3: respond = MenuAttendance(the_company).start()
            case 4: respond = MenuPayroll(the_company).start()
            case 5: respond = MenuDepartment(the_company).start()
            case 6: respond = MenuPerformance(the_company).start()
            case 7: break
            case _: last_msg = FCOLORS.RED + "Invalid choice!" + FCOLORS.END

        try:
            respond.unwrap() # type: ignore
        except (ValueError, TypeError) as e:
            last_msg = str(e)

if __name__ == "__main__":
    try:
        main_tui()
    except KeyboardInterrupt:
        sys.exit(0)
