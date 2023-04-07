from __future__ import annotations
import sys
from ..helpers import *
from datetime import datetime

if sys.version_info >= (3, 11):
    from typing import TYPE_CHECKING
else:
    from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from ...models.company import Company

class MenuAttendance:
    def __init__(self, company: Company) -> None:
        self.__company = company

    def start(self) -> tuple[bool, str]:
        employees = self.__company.employees

        # check if there are any employees to manage attendance for
        if not employees:
            return False, "No employees to manage attendance for!"

        # a list containing the string representation of each employee
        employee_items = [f"{employee.name} ({employee.id})" for employee in employees]

        # get the index of the selected employee
        selected_employee_index = get_user_option_from_list("Select an employee to manage attendance for", employee_items)
        if selected_employee_index == -1:
            return False, "No employee selected!"

        # get the employee object from the index
        self.__employee = employees[selected_employee_index]
        self.__attendances = self.__employee.attendance

        last_msg = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg = ""
            print(f"=== Attendance management for {self.__employee.name} ===")
            attendance_menu = [
                "[1] Check attendance",
                "[2] Update attendance",
                "[3] Get attendance report",
                "[4] Exit",
            ]
            choice = get_user_option_from_menu("Attendance management", attendance_menu)
            match choice:
                case 1: last_msg = self.__check()
                case 2: last_msg = self.__update()
                case 3: last_msg = self.__report()
                case _: return True, ""

    def __check(self) -> str:
        date = input("Enter date (YYYY-MM-DD, leave blank for today): ")
        try:
            date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
            is_presence = input("Is employee present? (y/n): ")
            self.__attendances.add_attendance(date, is_presence).unwrap()
            if not is_presence:
                reason = input("Enter reason for absent: ")
                self.__attendances.add_absent_day(date, reason).unwrap()
        except (ValueError, TypeError) as e:
            return str(e)
        return ""

    def __update(self) -> str:
        date = input("Enter date (YYYY-MM-DD, leave blank for today): ")
        try:
            # try to parse the date, if it fails, use today's date
            date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()

            # check if attendance exists for that date
            if date not in self.__attendances:
                return "No attendance found for that date!"

            # get the attendance object
            is_presence = input("Is employee present? (y/n): ")

            # update the attendance
            self.__attendances.add_attendance(date, is_presence).unwrap()

            # if the employee is absent, ask for the reason
            if not is_presence:
                reason = input("Enter reason for absent: ")
                self.__attendances.add_absent_day(date, reason).unwrap()
        except (ValueError, TypeError) as e:
            return str(e)
        return ""

    def __report(self) -> str:
        # check if there are any attendance data available
        if not self.__attendances:
            return "No attendance data available!"

        # get all the available years existing in the attendance data
        available_years = self.__attendances.get_available_years()

        # a list containing the string representation of each year
        year_items = [str(year) for year in available_years]

        # get the index of the selected year
        selected_year_index = get_user_option_from_list("Select a year to view attendance report for", year_items)
        if selected_year_index == -1:
            return "No year selected!"

        # print the attendance report
        print(self.__attendances.get_report(available_years[selected_year_index]))
        input("Press enter to continue...")
        return ""