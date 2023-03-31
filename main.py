import sys
import os
import re
from datetime import datetime
from models import Employee, Company, Department, BenefitPlan, Payroll, Sale
from option import Ok, Err, Result
from frontend import *


class Manager:
    def __init__(self, the_company: Company) -> None:
        self.__company = the_company

        self.__depts = the_company.departments
        self.__employees = the_company.employees
        self.__benefits = the_company.benefits

    @property
    def company(self) -> Company:
        return self.__company

    def employee(self) -> Result[None, str]:
        depts = self.__depts
        employees = self.__employees
        benefits = self.__benefits
        if not depts:
            return Err("No departments available! Please add a department first.")

        last_msg = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg = ""
            employee_menu = [
                f"[1] Add employee",
                f"[2] Remove employee",
                f"[3] Update employee",
                f"[4] View employee",
                f"[5] View all employees",
                f"[6] Back",
            ]
            choice = get_user_option_from_menu("Employee management", employee_menu)

            if (choice not in [1, 6]) and (not employees):
                last_msg = "No employees available! Please add an employee first."
                continue

            match choice:
                case 1:  # Add
                    employee = Employee()
                    fields_data = [
                        ("Enter employee name: ", employee.set_name),
                        ("Enter employee date of birth: ", employee.set_dob),
                        ("Enter employee ID: ", employee.set_id),
                        ("Enter employee phone number: ", employee.set_phone),
                        ("Enter employee email: ", employee.set_email),
                    ]
                    for (field, setter) in fields_data:
                        loop_til_valid_input(field, setter)
                    employees.append(employee)

                case 2:  # Remove
                    employee_index = get_user_option_from_list("Select an employee to remove", [f"{employee.name} ({employee.id})" for employee in employees])
                    if employee_index == -1:
                        continue

                    # remove from whatever department they're in
                    for dept in depts:
                        if employees[employee_index] in dept.employees:
                            dept.employees.remove(employees[employee_index])

                    # remove from whatever benefit plan they're in
                    for benefit in benefits:
                        if employees[employee_index] in benefit.enrolled_employee:
                            benefit.enrolled_employee.remove(employees[employee_index])

                    # remove from the company
                    employees.pop(employee_index)
                    last_msg = "Employee removed successfully!"

                case 3:  # Update
                    selected_employee_index = get_user_option_from_list("Select an employee to update", [f"{employee.name} ({employee.id})" for employee in employees])
                    if selected_employee_index == -1:
                        continue
                    employee = employees[selected_employee_index]
                    fields_data = [
                        ("Enter employee name: ", employee.set_name),
                        ("Enter employee date of birth (YYYY-MM-DD): ", employee.set_dob),
                        ("Enter employee ID: ", employee.set_id),
                        ("Enter employee phone number: ", employee.set_phone),
                        ("Enter employee email: ", employee.set_email),
                    ]
                    for (field, setter) in fields_data:
                        loop_til_valid_input(field, setter)

                case 4:  # View
                    selected_employee = get_user_option_from_list("Select an employee to view", [f"{employee.name} ({employee.id})" for employee in employees])
                    if selected_employee == -1:
                        return
                    print(employees[selected_employee])
                    input("\nPress enter to continue...")

                case 5:  # View all
                    listing("Employees", [f"{employee.name} ({employee.id})" for employee in employees])
                    input("Press enter to continue...")

                case _:
                    return Ok(None)

    def benefit_plan(self) -> Result[None, str]:
        benefits = self.__benefits
        employees = self.__employees

        last_msg = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg = ""
            benefit_plan_menu = [
                f"[1] Add benefit plan",
                f"[2] Apply benefit plan to employee",
                f"[3] Remove benefit plan",
                f"[4] Update benefit plan",
                f"[5] View benefit plan",
                f"[6] Exit",
            ]
            choice = get_user_option_from_menu("Benefit plan management", benefit_plan_menu)

            if (choice not in [1, 6]) and (not benefits):
                last_msg = "No benefits available! Please add a benefit plan first."
                continue

            match choice:
                case 1:  # Add
                    benefit = BenefitPlan()
                    loop_til_valid_input("Enter benefit plan name: ", benefit.set_name)
                    loop_til_valid_input("Enter benefit plan description: ", benefit.set_description)
                    loop_til_valid_input("Enter benefit plan cost: ", benefit.set_cost)
                    benefits.append(benefit)
                    last_msg = f"Benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} added successfully!"

                case 2:  # Apply
                    employee_index_selected = get_user_option_from_list("Select an employee to apply benefit plan to", [f"{employee.name} ({employee.id})" for employee in employees])
                    if employee_index_selected == -1:
                        return

                    benefit_index_selected = get_user_option_from_list("Select a benefit plan to apply to employee", [f"{benefit.name} ({benefit.cost})" for benefit in benefits])
                    if benefit_index_selected == -1:
                        return

                    benefit = benefits[benefit_index_selected]
                    employee = employees[employee_index_selected]

                    if benefit in employee.benefits:
                        last_msg = f"Employee {FCOLORS.GREEN}{employee.name}{FCOLORS.END} already has benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} applied to them!"
                        continue

                    employee.benefits.append(benefit)
                    benefit.enrolled_employees.append(employee)

                    last_msg = f"Benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} applied to employee {FCOLORS.GREEN}{employee.name}{FCOLORS.END} successfully!"

                case 3:  # Remove
                    benefit_index_selected = get_user_option_from_list("Select a benefit plan to remove", [f"{benefit.name} ({benefit.cost})" for benefit in benefits])
                    if benefit_index_selected == -1:
                        continue
                    benefit = benefits[benefit_index_selected]

                    # remove the benefit from whatever employee it's applied to
                    for employee in employees:
                        if benefit in employee.benefits:
                            employee.benefits.remove(benefit)

                    benefits.pop(benefit_index_selected)

                    last_msg = f"Benefit {FCOLORS.GREEN}{benefit}{FCOLORS.END} removed successfully!"

                case 4:  # Update
                    selected_benefit_index = get_user_option_from_list("Select a benefit plan to update", [f"{benefit.name} ({benefit.cost})" for benefit in benefits])
                    if selected_benefit_index == -1:
                        continue

                    benefit = benefits[selected_benefit_index]
                    fields_data = [
                        ("Enter benefit plan name: ", benefit.set_name),
                        ("Enter benefit plan description: ", benefit.set_description),
                        ("Enter benefit plan cost: ", benefit.set_cost),
                    ]
                    for (field, setter) in fields_data:
                        loop_til_valid_input(field, setter)

                    last_msg = f"Benefit {FCOLORS.GREEN}{benefit.name}{FCOLORS.END} updated successfully!"

                case 5:  # View
                    selected_benefit_index = get_user_option_from_list("Select a benefit plan to view", [f"{benefit.name} ({benefit.cost})" for benefit in benefits])
                    if selected_benefit_index == -1:
                        continue

                    print(benefits[selected_benefit_index])

                case _:
                    return Ok(None)

    def attendance(self) -> Result[None, str]:
        employees = self.__employees
        if not employees:
            return Err("No employees to manage attendance for!")

        selected_employee_index = get_user_option_from_list("Select an employee to manage attendance for", [f"{employee.name} ({employee.id})" for employee in employees])
        if selected_employee_index == -1:
            return Ok(None)
        employee = employees[selected_employee_index]
        attendances = employee.attendance

        last_msg = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg = ""
            print(f"=== Attendance management for {employee.name} ===")
            attendance_menu = [
                f"[1] Check attendance",
                f"[2] Update attendance",
                f"[3] Get attendance report",
                f"[4] Exit",
            ]
            choice = get_user_option_from_menu("Attendance management", attendance_menu)
            match choice:
                case 1:  # Check
                    date = input("Enter date (YYYY-MM-DD, leave blank for today): ")
                    try:
                        date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
                        is_presence = input("Is employee present? (y/n): ")
                        attendances.add_attendance(date, is_presence).unwrap()
                        if not is_presence:
                            reason = input("Enter reason for absence: ")
                            attendances.add_absence_day(date, reason).unwrap()
                    except (ValueError, TypeError) as e:
                        last_msg = str(e)

                case 2:  # Update
                    date = input("Enter date (YYYY-MM-DD, leave blank for today): ")
                    try:
                        date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
                        if date not in attendances:
                            print("No attendance found for that date!")
                            break
                        is_presence = input("Is employee present? (y/n): ")
                        attendances.update_attendance(date, is_presence).unwrap()
                        if not is_presence:
                            reason = input("Enter reason for absence: ")
                            attendances.add_absence_day(date, reason).unwrap()
                        break
                    except:
                        date = input("Invalid date format! Try again: ")
                        continue
                case 3:  # Report
                    report = attendances.get_report()
                    try:
                        items = [f"{k}: {v}" for k, v in report.unwrap().items()]
                        listing("Attendance report", items)
                    except:
                        print("No attendance found for this employee!")
                case _:
                    return Ok(None)

    def payroll(self) -> Result[None, str]:
        employees = self.__employees
        if not employees:
            return Err("No employees to manage payroll for!")

        selected_employee_index = get_user_option_from_list("Select an employee to manage payroll for", [f"{employee.name} ({employee.id})" for employee in employees])
        if selected_employee_index == -1:
            return Ok(None)
        employee = employees[selected_employee_index]

        last_msg = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg = ""
            payroll_menu = [
                f"[1] Create payroll",
                f"[2] Update payroll",
                f"[3] Exit"
            ]
            choice = get_user_option_from_menu("Payroll management", payroll_menu)
            match choice:
                case 1:  # Create
                    clrscr()
                    print(f"== Creating payroll for employee {FCOLORS.GREEN}{employee.name}{FCOLORS.END} ==")
                    payroll = Payroll()
                    fields_data = [
                        ("Enter payroll salary: ", payroll.set_salary),
                        ("Enter payroll bonus: ", payroll.set_bonus),
                        ("Enter payroll tax: ", payroll.set_tax),
                        ("Enter payroll punishment: ", payroll.set_punish)
                    ]
                    for (field, setter) in fields_data:
                        loop_til_valid_input(field, setter)
                    employee.set_payroll(payroll)
                    last_msg = f"Payroll for employee {FCOLORS.GREEN}{employee.name}{FCOLORS.END} created successfully!"

                case 2:  # View
                    payroll = employee.payroll
                    if payroll is None:
                        last_msg = f"Employee {FCOLORS.GREEN}{employee.name}{FCOLORS.END} has no payroll!"
                        continue
                    print(payroll)

                case _:
                    return Ok(None)

    def department(self) -> Result[None, str]:
        employees = self.__employees
        depts = self.__depts

        last_msg = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg = ""
            department_menu = [
                f"[1] Add department",
                f"[2] Remove department",
                f"[3] Update department",
                f"[4] View department",
                f"[5] View all departments",
                f"[6] Back",
            ]

            choice = get_user_option_from_menu("Department management", department_menu)
            if (choice in range(2, 6)) and (not depts):
                last_msg = "No departments to manage, please add a department first!"
                continue

            match choice:
                case 1:  # Add
                    dept = Department()
                    loop_til_valid_input("Enter department name: ", dept.set_name)
                    loop_til_valid_input("Enter department ID: ", dept.set_id)
                    depts.append(dept)
                    last_msg = f"Department {FCOLORS.GREEN}{dept.name}{FCOLORS.END} added successfully!"

                case 2:  # Remove
                    dept_selected_index = get_user_option_from_list("Select a department to remove", [f"{dept.name} ({dept.id})" for dept in depts])
                    if dept_selected_index == -1:
                        continue

                    # remove the department from whatever employee it's applied to
                    for employee in employees:
                        if employee.department == depts[dept_selected_index]:
                            employee.set_department(None)

                    depts.pop(dept_selected_index)
                    last_msg = "Department removed successfully!"

                case 3:  # Update
                    dept_selected_index = get_user_option_from_list("Select a department to update", [f"{dept.name} ({dept.id})" for dept in depts])
                    if dept_selected_index == -1:
                        continue

                    dept = depts[dept_selected_index]
                    loop_til_valid_input("Enter department name: ", dept.set_name)
                    loop_til_valid_input("Enter department ID: ", dept.set_id)

                    last_msg = "Department updated successfully!"

                case 4:  # View
                    dept_selected_index = get_user_option_from_list("Select a department to view info", [f"{dept.name} ({dept.id})" for dept in depts])

                    if dept_selected_index == -1:
                        continue

                    print(depts[dept_selected_index])
                    input("Press enter to continue...")

                case 5:  # View all
                    listing("Departments", [f"{dept.name} ({dept.id})" for dept in depts])

                case 6:  # Back
                    return Ok(None)

                case _:
                    continue

    def performance(self) -> Result[None, str]:
        employees = self.__employees
        if employees is None:
            return Err("No employees to manage performance, please add an employee first!")

        # --- Select an employee to manage performance first ---
        employee_selected_index = get_user_option_from_list("Select an employee to manage performance", [f"{employee.name} ({employee.id})" for employee in employees])
        if employee_selected_index == -1:
            return
        employee = employees[employee_selected_index]
        performance = employee.performance

        last_msg = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg = ""
            performance_menu = [
                f"[1] Add sale"
                f"[2] View sales performance",
                f"[3] Remove sale",
                f"[4] Get sale info",
                f"[5] Find sale(s) by...",
                f"[6] Back",
            ]
            choice = get_user_option_from_menu("Performance management", performance_menu)
            match choice:
                case 1:  # Add
                    # --- Create a new sale ---
                    sale = Sale()
                    fields_data = [
                        ("Enter sale ID: ", sale.set_sale_id),
                        ("Enter revenue: ", sale.set_revenue),
                        ("Enter cost: ", sale.set_cost),
                        ("Enter profit: ", sale.set_profit),
                        ("Enter client ID: ", sale.set_client_id),
                        ("Enter client rating: ", sale.set_client_rating),
                        ("Enter client comment: ", sale.set_client_comment)
                    ]
                    for (field, setter) in fields_data:
                        loop_til_valid_input(field, setter)

                    # Sale date has a default value, can't use the loop_til_valid_input function
                    sale_date = input("Enter sale date (YYYY-MM-DD, leave blank for today): ")
                    try:
                        sale_date = datetime.strptime(sale_date, "%Y-%m-%d") if sale_date else datetime.now()
                        sale.set_sale_date(sale_date).unwrap()
                    except (ValueError, TypeError) as e:
                        last_msg = str(e)

                    # --- Add sale to employee ---
                    performance.sale_list.append(sale)
                    last_msg = f"Sale for employee {FCOLORS.GREEN}{employee.name}{FCOLORS.END} added successfully!"

                case 2:  # View
                    print(performance)
                    input("Press enter to continue...")

                case 3:  # Remove
                    # --- Select sale to remove ---
                    selected_sale_index = get_user_option_from_list("Select a sale to remove", [f"{sale.sale_id} ({sale.client_id})" for sale in performance.sale_list])
                    if selected_sale_index == -1:
                        continue

                    # --- Remove sale ---
                    performance.sale_list.pop(selected_sale_index)
                    last_msg = f"Sale for employee {FCOLORS.GREEN}{employee.name}{FCOLORS.END} removed successfully!"

                case 4:  # Get info
                    print(performance.get_info())

                case 5:  # Find sales by...
                    # --- Select a field to search by ---
                    search_fields = [
                        "Sale ID",
                        "Client ID",
                        "Client rating",
                        "Date"
                    ]
                    search_selection = get_user_option_from_list("Find all sales by...", search_fields)
                    match search_selection:
                        case 0:  # Sale ID
                            sale = performance.get_sale_by_id(input("Enter sale ID: "))
                            if sale:
                                print(sale)
                                input("Press enter to continue...")
                            else:
                                last_msg = "No sales found!"
                        case 1:  # Client ID
                            sales = performance.get_sales_by_client_id(input("Enter client ID: "))
                            if not sales:
                                last_msg = "No sales found!"
                                continue
                            for sale in sales:
                                print(sale)
                        case 2:  # Client rating
                            rating = input("Enter client rating: ")
                            try:
                                rating = int(rating)
                            except:
                                last_msg = "Invalid rating!"
                                continue
                            sales = performance.get_sales_by_rating(rating)
                            if not sales:
                                last_msg = "No sales found!"
                                continue
                            for sale in sales:
                                print(sale, end="\n\n")
                        case 3:  # Date
                            date = input("Enter date (YYYY-MM-DD, leave blank for today): ")
                            try:
                                date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
                            except:
                                last_msg = "Invalid date!"
                                continue
                            sales = performance.get_sales_by_date(date)
                            if not sales:
                                last_msg = "No sales found!"
                                continue

                            for sale in sales:
                                print(sale, end="\n\n")
                        case _:  # Back
                            continue

                case _:  # Back
                    return Ok(None)


def main():

    last_msg = ""

    the_company = Company()
    manager = Manager(the_company)

    while True:
        clrscr()
        if last_msg:
            print(last_msg)
            last_msg = ""
        main_menu = [
            f"[1] Employee management",
            f"[2] Benefit plan management",
            f"[3] Attendance management",
            f"[4] Payroll management",
            f"[5] Department management",
            f"[6] Exit",
        ]
        user_choice = get_user_option_from_menu("Main menu", main_menu)

        respond: Result = Ok(None)

        match user_choice:
            case 1: respond = manager.employee()
            case 2: respond = manager.benefit_plan()
            case 3: respond = manager.attendance()
            case 4: respond = manager.payroll()
            case 5: respond = manager.department()
            case 6:
                break
            case _:
                last_msg = FCOLORS.RED + "Invalid choice!" + FCOLORS.END

        try:
            respond.unwrap()
        except (TypeError, ValueError) as e:
            last_msg = FCOLORS.RED + str(e) + FCOLORS.END


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
