import os
import random
import string

from faker import Faker

from database.mongo import benefit_repo, department_repo, employee_repo
from models import BenefitPlan, Company, Department, Employee

the_company = Company()
__current_employee_count = len(the_company.employees)


def generate_random_data_into_db():
    def rand_id():
        return "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=10))

    def rand_phone():
        return random.choice("123456789") + "".join(random.choices(string.digits, k=9))

    fake = Faker()

    # Generate 20 random employees
    taken_ids, taken_phones = [], []
    for _ in range(20):
        random_id = rand_id()
        while random_id in taken_ids:
            random_id = rand_id()

        random_phone = rand_phone()
        while random_phone in taken_phones:
            random_phone = rand_phone()

        # fmt: off
        employee = (
            Employee()
            .set_name(fake.name()).unwrap()
            .set_dob(fake.date()).unwrap()
            .set_email(fake.email()).unwrap()
            .set_phone(random_phone).unwrap()
            .set_id(random_id).unwrap()
            .set_password("".join(random.choices(string.ascii_letters + string.digits, k=10))).unwrap()
        )
        # fmt: on
        the_company.employees.append(employee)

    # Generate 5 random attendance records for each in employee.attendance.attendances: dict[str<from datetime.strftime("%Y-%m-%d")>, bool<is_present>]
    # each absence has a reason in employee.attendance.absents: dict[str<from datetime.strftime("%Y-%m-%d")>, str<reason>]'
    for employee in the_company.employees:
        for _ in range(5):
            randomized_date = fake.date_between(start_date="-1y", end_date="today")
            employee.attendance.add_attendance(randomized_date, random.choice([True, False])).unwrap()
            if not employee.attendance.attendances[randomized_date.strftime("%Y-%m-%d")]:
                employee.attendance.add_absent_day(randomized_date, random.choice(["Sick", "Vacation", "Personal"])).unwrap()
        # if the employee.attendance.allowed_absent_days{str<year>, int<days>} is negative, then the employee's payroll will be punished. remember to only punish once per year
        years = employee.attendance.get_available_years()
        if not years:
            continue
        for year in years:
            if (
                len([day for day in employee.attendance.absents.values() if day == str(year)])
                > [days for year, days in employee.attendance.allowed_absent_days.items() if year == year][0]
            ):
                # employee.attendance.punish_payroll(year)
                employee.payroll.set_punish("10")

    # Generate 5 random departments
    depts = ["HR", "IT", "Marketing", "Sales", "Finance"]
    for _ in range(5):
        department = (
            Department().set_name(random.choice(depts)).unwrap().set_id(str(random.randint(100000000, 999999999))).unwrap()
        )
        the_company.departments.append(department)
        depts.remove(department.name)

    # Generate 4 random benefit plans
    benfit_plans = ["Health Insurance", "Dental Insurance", "Vision Insurance", "401K"]
    for _ in range(4):
        benefit = BenefitPlan().set_name(random.choice(benfit_plans)).unwrap().set_cost(random.randint(100, 1000)).unwrap()
        the_company.benefits.append(benefit)
        benfit_plans.remove(benefit.name)

    # Randomize assign employees to departments, each employee has 1 department and only contains department_id
    for employee in the_company.employees:
        employee.department_id = random.choice([department.dept_id for department in the_company.departments])

        # append the employee object to the department members' list
        for department in the_company.departments:
            if employee.department_id == department.dept_id:
                department.members.append(employee)

    # Randomize assign employees to benefit plans, each employee has 1-3 benefits and only contains benefit_id
    for employee in the_company.employees:
        employee.benefits = random.choices([benefit.name for benefit in the_company.benefits], k=random.randint(1, 3))
        # append the employee object to the benefit enrolled_employees' list
        for benefit in the_company.benefits:
            if benefit.name in employee.benefits:
                benefit.enrolled_employees.append(employee)

    # Randomize employee's payroll
    for employee in the_company.employees:
        (
            employee.payroll.set_salary(str(random.randint(1000, 10000)))
            .unwrap()
            .set_bonus(str(random.randint(100, 1000)))
            .unwrap()
            .set_tax(str(random.randint(100, 1000)))
            .unwrap()
        )
    if os.getenv("HRMGR_DB") == "TRUE":
        for employee in the_company.employees[__current_employee_count:]:
            employee_repo.insert_one(employee.dict(by_alias=True))

        for department in the_company.departments:
            department_repo.insert_one(department.dict(by_alias=True))

        for benefit in the_company.benefits:
            benefit_repo.insert_one(benefit.dict(by_alias=True))
