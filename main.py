import sys
import os

from pymongo.database import Database
from frontend.helpers import *
from frontend.menu import *
from models import Company, BenefitPlan, Department, Employee
from database import mongo
from pymongo import MongoClient
from dotenv import load_dotenv
from database.mongo import employee_repo, department_repo, benefit_repo

load_dotenv()
# from option import Result, Ok, Err

the_company = Company()

def initialize_data():
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
    last_msg = ""
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

        respond: tuple[bool, str] = (True, "")
        match user_choice:
            case 1: respond = MenuEmployee(the_company).start()
            case 2: respond = MenuBenefits(the_company).start()
            case 3: respond = MenuAttendance(the_company).start()
            case 4: respond = MenuPayroll(the_company).start()
            case 5: respond = MenuDepartment(the_company).start()
            case 6: respond = MenuPerformance(the_company).start()
            case 7: break
            case _: last_msg = FCOLORS.RED + "Invalid choice!" + FCOLORS.END

        if not respond[0]:
            last_msg = FCOLORS.RED + respond[1] + FCOLORS.END

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
