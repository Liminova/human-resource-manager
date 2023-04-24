from ..helpers_tui import *
from models import Payroll, Company
from option import Result, Ok
from database.mongo import employee_repo  # type: ignore
import os

the_company: Company = Company()


class MenuPayroll:
    def __init__(self) -> None:
        self.mainloop = self.admin if the_company.logged_in_employee.is_admin else self.employee

    def admin(self) -> Result[None, str]:
        last_msg = ""
        while True:
            last_msg = refresh(last_msg)
            payroll_menu = ["[1] Create payroll", "[2] Update payroll", "[3] View all payrolls", "[4] Back"]
            choice = get_user_option_from_menu("Payroll management", payroll_menu)
            match choice:
                case 1:
                    last_msg = self.__create()
                case 2:
                    last_msg = self.__update()
                case 3:
                    last_msg = self.__view_all()
                case 4:
                    return Ok(None)
                case _:
                    last_msg = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def employee(self) -> Result[None, str]:
        last_msg = ""
        while True:
            last_msg = refresh(last_msg)
            payroll_menu = ["[1] View details", "[2] Back"]
            choice = get_user_option_from_menu("Payroll management", payroll_menu)
            match choice:
                case 1:
                    last_msg = self.__view()
                case 2:
                    return Ok(None)
                case _:
                    last_msg = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def __create(self) -> str:
        empls = the_company.employees

        empl_idx_select = get_user_option_from_list(
            "Select an employee to create payroll for", tuple(f"{e.name} ({e.employee_id})" for e in the_company.employees)
        )
        if empl_idx_select in (-1, -2):
            return NO_EMPLOYEE_MSG if empl_idx_select == -1 else ""

        if not the_company.can_modify("payroll", empls[empl_idx_select]):
            return "Only the owner can create payroll for admins!"

        if empls[empl_idx_select].payroll.salary != 0:
            return f"Employee {FCOLORS.GREEN}{empls[empl_idx_select].name}{FCOLORS.END} already has a payroll!"

        clrscr()
        print(f"== Creating payroll for employee {FCOLORS.GREEN}{empls[empl_idx_select].name}{FCOLORS.END} ==")

        # create an empty payroll object
        payroll = Payroll()

        # assigning values to the payroll object
        fields_data = [
            ("Enter payroll salary", payroll.set_salary),
            ("Enter payroll bonus", payroll.set_bonus),
            ("Enter payroll tax", payroll.set_tax),
            ("Enter payroll punishment", payroll.set_punish),
        ]
        for field, setter in fields_data:
            if (msg := loop_til_valid_input(field, setter)) != "":
                return msg

        # add the payroll object to the employee
        the_company.employees[empl_idx_select].payroll = payroll
        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one(
                {"_id": empls[empl_idx_select].id}, {"$set": empls[empl_idx_select].dict(include={"payroll"})}, upsert=True
            )

        return f"Payroll for employee {FCOLORS.GREEN}{empls[empl_idx_select].name}{FCOLORS.END} created successfully!"

    def __update(self) -> str:
        empls = the_company.employees

        empl_idx_select = get_user_option_from_list(
            "Select an employee to update payroll for", tuple(f"{e.name} ({e.employee_id})" for e in empls)
        )
        if empl_idx_select in (-1, -2):
            return NO_EMPLOYEE_MSG if empl_idx_select == -1 else ""

        if not the_company.can_modify("payroll", empls[empl_idx_select]):
            return "Only the owner can update payroll for admins!"

        if empls[empl_idx_select].payroll.salary == 0:
            return f"Employee {FCOLORS.GREEN}{empls[empl_idx_select].name}{FCOLORS.END} has no payroll!"

        clrscr()
        print(f"== Updating payroll for employee {FCOLORS.GREEN}{empls[empl_idx_select].name}{FCOLORS.END} ==")

        # assigning values to the payroll object
        fields_data = [
            ("Enter payroll salary", empls[empl_idx_select].payroll.set_salary),
            ("Enter payroll bonus", empls[empl_idx_select].payroll.set_bonus),
            ("Enter payroll tax", empls[empl_idx_select].payroll.set_tax),
            ("Enter payroll punishment", empls[empl_idx_select].payroll.set_punish),
        ]
        for field, setter in fields_data:
            if (msg := loop_til_valid_input(field, setter)) != "":
                return msg
        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one(
                {"_id": empls[empl_idx_select].id}, {"$set": empls[empl_idx_select].dict(include={"payroll"})}, upsert=True
            )

        return f"Payroll for employee {FCOLORS.GREEN}{empls[empl_idx_select].name}{FCOLORS.END} updated successfully!"

    def __view_all(self) -> str:
        empl_payroll_items = tuple(
            f"{e.name} ({e.employee_id}) | Salary: {e.payroll.salary} | Bonus: {e.payroll.bonus} | Tax: {e.payroll.tax} | Punishment: {e.payroll.punish}"
            for e in the_company.employees
        )
        listing("All employees payroll", empl_payroll_items)
        return ""

    def __view(self) -> str:
        empls = the_company.employees

        clrscr()
        print(f"== Payroll for employee {FCOLORS.GREEN}{the_company.logged_in_employee.name}{FCOLORS.END} ==")
        if not the_company.logged_in_employee.is_admin:
            print(the_company.logged_in_employee.payroll)
        else:
            empl_idx_select = get_user_option_from_list(
                "Select an employee to view payroll for", tuple(f"{e.name} ({e.employee_id})" for e in empls)
            )
            if empl_idx_select in (-1, -2):
                return NO_EMPLOYEE_MSG if empl_idx_select == -1 else ""
            print(empls[empl_idx_select].payroll)

        input(ENTER_TO_CONTINUE_MSG)
        return ""
