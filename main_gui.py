# Connect to MongoDB and run the GUI

import pymongo
import os
import sys
import tkinter

from frontend.gui import Login
from frontend.gui import Signup
from frontend.helpers import *
from frontend.menu import *
from models import Company, Employee, BenefitPlan, Department
from dotenv import load_dotenv
from database.mongo import employee_repo, benefit_repo, department_repo
from option import Result, Ok
from tkinter import messagebox


load = load_dotenv()

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


def main_gui():
    # client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    # db = client[os.getenv("MONGO_DB")]
    if not os.getenv("MONGO_USER") or not os.getenv("MONGO_PASS") or not os.getenv("MONGO_URI"):
        os.environ["HRMGR_DB"] = "FALSE"
        messagebox.showinfo("Error", "It seems like your environment variables are not set up. The program will now run in memory-only mode. Press OK to continue", type="ok")
    else:
        initialize_data()
    # ======================
    # Welcome to the GUI
    # ======================

    if len(the_company.employees) == 0:
        messagebox.showinfo("Welcome", "Welcome to HR Manager! It seems like you are new here. Please create an account to get started.", type="ok")
        window1 = Signup()
        window1.run()
    else:
        messagebox.showinfo("Welcome", "Welcome back to HR Manager! Please log in to continue.", type="ok")
        window = Login()
        window.run()

if __name__ == "__main__":
    try:
        main_gui()
    except KeyboardInterrupt:
        sys.exit(0)