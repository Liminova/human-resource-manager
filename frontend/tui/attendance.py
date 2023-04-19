from ..helpers import *
from datetime import datetime
from option import Result, Ok, Err
from models import Company, Employee
from database.mongo import employee_repo
import os

the_company: Company = Company()


class MenuAttendance:
    def __init__(self) -> None:
        if the_company.logged_in_employee.is_admin:
            self.mainloop = self.admin
        else:
            self.mainloop = self.employee
        self.__employee = Employee()

    def admin(self) -> Result[None, str]:
        # get the index of the selected employee
        selected_employee_index = get_user_option_from_list(
            "Select an employee to manage attendance for",
            tuple(f"{e.name} ({e.employee_id})" for e in the_company.employees),
        )
        if selected_employee_index in (-1, -2):
            return Err(NO_EMPLOYEE_MSG) if selected_employee_index == -1 else Ok(None)

        # get the employee object from the index
        self.__employee = the_company.employees[selected_employee_index]

        if not the_company.can_modify("attendance", self.__employee):
            return Err("You do not have permission to modify this employee's attendance!")

        last_msg = ""
        while True:
            last_msg = refresh(last_msg)
            # fmt: off
            attendance_menu = [
                "[1] Check attendance",
                "[2] Update attendance",
                "[3] Get attendance report",
                "[4] Back"
            ]
            # fmt: on
            choice = get_user_option_from_menu("Attendance management for " + self.__employee.name, attendance_menu)
            match choice:
                case 1:
                    last_msg = self.__check()
                case 2:
                    last_msg = self.__update()
                case 3:
                    last_msg = self.__report()
                case 4:
                    return Ok(None)
                case _:
                    last_msg = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def employee(self) -> Result[None, str]:
        last_msg = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg = ""
            # fmt: off
            attendance_menu = [
                "[1] Check attendance",
                "[2] Get attendance report",
                "[3] Back"
            ]
            # fmt: on
            choice = get_user_option_from_menu(
                "Attendance management for " + the_company.logged_in_employee.name, attendance_menu
            )
            match choice:
                case 1:
                    last_msg = self.__check()
                case 2:
                    last_msg = self.__report()
                case 3:
                    return Ok(None)
                case _:
                    last_msg = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def __check(self) -> str:
        employee = the_company.logged_in_employee

        try:
            # as an admin checking attendance for other employee
            if the_company.can_modify("attendance", the_company.logged_in_employee):
                if datetime.strftime(datetime.now(), "%Y-%m-%d") in the_company.logged_in_employee.attendance.attendances:
                    return "This employee already has their attendance checked!"
                date = datetime.now()
                is_present = input("Is employee present? (y/n): ")
                if is_present.lower() == "y":
                    the_company.logged_in_employee.attendance.add_attendance(date, True).unwrap()
                else:
                    reason = input("Enter reason for absent: ")
                    the_company.logged_in_employee.attendance.add_attendance(date, False).unwrap()
                    the_company.logged_in_employee.attendance.add_absent_day(date, reason).unwrap()
                    if the_company.logged_in_employee.attendance.get_allowed_absent_days(date.year).unwrap() < 0:
                        the_company.logged_in_employee.payroll.set_punish("10")

                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one(
                        {"_id": employee.id}, {"$set": employee.dict(include={"attendance"})}, upsert=True
                    )

            # as an employee or admin updating their own attendance
            else:
                if datetime.strftime(datetime.now(), "%Y-%m-%d") in the_company.logged_in_employee.attendance.attendances:
                    return "You are already present!"
                the_company.logged_in_employee.attendance.add_attendance(datetime.now(), True).unwrap()
                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one(
                        {"_id": employee.id}, {"$set": employee.dict(include={"attendance"})}, upsert=True
                    )
                return "You are present now!"

        except (ValueError, TypeError) as e:
            return str(e)
        return ""

    def __update(self) -> str:
        date_str = input("Enter date (YYYY-MM-DD, leave blank for today): ")
        try:
            if the_company.can_modify("attendance", self.__employee):
                # parse the date, if the date is empty, use today's date
                date = datetime.strptime(date_str, "%Y-%m-%d") if date_str != "" else datetime.now()

                # check if attendance exists for that date
                if date not in self.__employee.attendance.attendances:
                    return "No attendance found for that date!"

                # get the attendance object
                is_present = input("Is employee present? (y/n): ")
                if is_present.lower() == "y":
                    # update the attendance
                    self.__employee.attendance.add_attendance(date, True).unwrap()
                else:
                    # if the employee is absent, ask for the reason
                    reason = input("Enter reason for absent: ")
                    self.__employee.attendance.add_attendance(date, False).unwrap()
                    self.__employee.attendance.add_absent_day(date, reason).unwrap()

                    if self.__employee.attendance.get_allowed_absent_days(date.year).unwrap() < 0:
                        self.__employee.payroll.set_punish("10")

                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one(
                        {"_id": self.__employee.id}, {"$set": self.__employee.dict(include={"attendance"})}, upsert=True
                    )
        except (ValueError, TypeError) as e:
            return str(e)
        return ""

    def __report(self) -> str:
        attendances = the_company.logged_in_employee.attendance

        if self.__employee.is_admin:
            # check if there are any attendance data available
            if not attendances:
                return NO_ATTENDANCE_MSG

            # get all the available years existing in the attendance data
            available_years = attendances.get_available_years()

            # a list containing the string representation of each year
            year_items = [str(year) for year in available_years]

            # get the index of the selected year
            selected_year_index = get_user_option_from_list(
                "Select a year to view attendance report for", tuple(str(y) for y in year_items)
            )
            if selected_year_index in (-1, -2):
                return NO_ATTENDANCE_MSG if selected_year_index == -1 else ""

            # print the attendance report
            print(attendances.get_report(datetime.strptime(year_items[selected_year_index], "%Y")))
        else:
            year_items = [str(year) for year in attendances.get_available_years()]
            selected_year_index = get_user_option_from_list(
                "Select a year to view attendance report for", tuple(str(y) for y in year_items)
            )
            if selected_year_index == -1:
                return NO_ATTENDANCE_MSG
            elif selected_year_index == -2:
                return ""

            # print the attendance report
            print(attendances.get_report(datetime.strptime(year_items[selected_year_index], "%Y")))

        input(ENTER_TO_CONTINUE_MSG)
        return ""
