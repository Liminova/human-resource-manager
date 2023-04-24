from ..helpers_tui import *
from datetime import datetime
from option import Result, Ok, Err
from models import Company
from database.mongo import employee_repo  # type: ignore
import os

the_company: Company = Company()


class MenuAttendance:
    def __init__(self) -> None:
        self.mainloop = self.admin if the_company.logged_in_employee.is_admin else self.employee

    def admin(self) -> Result[None, str]:
        # get the index of the selected employee
        empl_idx_select = get_user_option_from_list(
            "Select an employee to manage attendance for",
            tuple(f"{e.name} ({e.employee_id})" for e in the_company.employees),
        )
        if empl_idx_select in (-1, -2):
            return Err(NO_EMPLOYEE_MSG) if empl_idx_select == -1 else Ok(None)

        self.__empl_idx = empl_idx_select

        if not the_company.can_modify("attendance", the_company.employees[self.__empl_idx]):
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
            choice = get_user_option_from_menu(
                "Attendance management for " + the_company.employees[self.__empl_idx].name, attendance_menu
            )
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
            last_msg = refresh(last_msg)
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
        empl = the_company.logged_in_employee

        try:
            # as an admin checking attendance for other employee
            if the_company.can_modify("attendance", empl):
                if datetime.strftime(datetime.now(), "%Y-%m-%d") in empl.attendance.attendances:
                    return "This employee already has their attendance checked!"
                date = datetime.now()
                is_present = input("Is employee present? (y/n): ")
                if is_present.lower() == "y":
                    empl.attendance.add_attendance(date, True).unwrap()
                else:
                    reason = input("Enter reason for absent: ")
                    empl.attendance.add_attendance(date, False).unwrap()
                    empl.attendance.add_absent_day(date, reason).unwrap()
                    if empl.attendance.get_allowed_absent_days(date.year).unwrap() < 0:
                        empl.payroll.set_punish("10")

                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one({"_id": empl.id}, {"$set": empl.dict(include={"attendance"})}, upsert=True)

            # as an employee or admin updating their own attendance
            else:
                if datetime.strftime(datetime.now(), "%Y-%m-%d") in empl.attendance.attendances:
                    return "You are already present!"
                empl.attendance.add_attendance(datetime.now(), True).unwrap()
                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one({"_id": empl.id}, {"$set": empl.dict(include={"attendance"})}, upsert=True)
                return "You are present now!"

        except (ValueError, TypeError) as e:
            return str(e)
        return ""

    def __update(self) -> str:
        empls = the_company.employees
        date_str = input("Enter date (YYYY-MM-DD, leave blank for today): ")
        try:
            if the_company.can_modify("attendance", empls[self.__empl_idx]):
                # parse the date, if the date is empty, use today's date
                date = datetime.strptime(date_str, "%Y-%m-%d") if date_str != "" else datetime.now()

                # check if attendance exists for that date
                if datetime.strftime(date, "%Y-%m-%d") not in empls[self.__empl_idx].attendance.attendances:
                    return "No attendance found for that date!"

                # get the attendance object
                is_present = input("Is employee present? (y/n): ")
                if is_present.lower() == "y":
                    # update the attendance
                    empls[self.__empl_idx].attendance.add_attendance(date, True).unwrap()
                else:
                    # if the employee is absent, ask for the reason
                    reason = input("Enter reason for absent: ")
                    empls[self.__empl_idx].attendance.add_absent_day(date, reason).unwrap()
                    empls[self.__empl_idx].attendance.add_attendance(date, False).unwrap()

                    if empls[self.__empl_idx].attendance.get_allowed_absent_days(date.year).unwrap() < 0:
                        empls[self.__empl_idx].payroll.set_punish("10")

                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one(
                        {"_id": empls[self.__empl_idx].id},
                        {"$set": empls[self.__empl_idx].dict(include={"attendance"})},
                        upsert=True,
                    )
        except (ValueError, TypeError) as e:
            return str(e)
        return ""

    def __report(self) -> str:
        empls = the_company.employees

        if empls[self.__empl_idx].is_admin:
            # check if there are any attendance data available
            if not empls[self.__empl_idx].attendance.attendances:
                return NO_ATTENDANCE_MSG

            # get all the available years existing in the attendance data
            available_years = empls[self.__empl_idx].attendance.get_available_years()

            # a list containing the string representation of each year
            year_items = [str(year) for year in available_years]

            # get the index of the selected year
            year_idx_select = get_user_option_from_list(
                "Select a year to view attendance report for", tuple(str(y) for y in year_items)
            )
            if year_idx_select in (-1, -2):
                return NO_ATTENDANCE_MSG if year_idx_select == -1 else ""

            # print the attendance report
            print(empls[self.__empl_idx].attendance.get_report(datetime.strptime(year_items[year_idx_select], "%Y")))
        else:
            year_items = [str(year) for year in empls[self.__empl_idx].attendance.get_available_years()]
            year_idx_select = get_user_option_from_list("Select a year to view attendance report for", tuple(year_items))
            if year_idx_select in (-1, -2):
                return NO_ATTENDANCE_MSG if year_idx_select == -1 else ""

            # print the attendance report
            print(empls[self.__empl_idx].attendance.get_report(datetime.strptime(year_items[year_idx_select], "%Y")))

        input(ENTER_TO_CONTINUE_MSG)
        return ""
