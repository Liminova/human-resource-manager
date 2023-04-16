from ..helpers import *
from datetime import datetime
from option import Result, Ok, Err
from models import Company

the_company: Company = Company()


class MenuAttendance:
    def __init__(self) -> None:
        if the_company.logged_in_employee.is_admin:
            self.mainloop = self.admin
        else:
            self.mainloop = self.employee

    def admin(self) -> Result[None, str]:
        # a list containing the string representation of each employee
        employee_items = [f"{e.name} ({e.employee_id})" for e in the_company.employees]

        # get the index of the selected employee
        selected_employee_index = get_user_option_from_list(
            "Select an employee to manage attendance for", employee_items
        )
        if selected_employee_index == -1:
            return Err(NO_EMPLOYEE_MSG)
        elif selected_employee_index == -2:
            return Ok(None)

        # get the employee object from the index
        self.__employee = the_company.employees[selected_employee_index]

        if not the_company.can_modify("attendance", self.__employee):
            return Err(
                "You do not have permission to modify this employee's attendance!"
            )

        last_msg: str = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg: str = ""
            attendance_menu = [
                "[1] Check attendance",
                "[2] Update attendance",
                "[3] Get attendance report",
                "[4] Back",
            ]
            choice = get_user_option_from_menu(
                "Attendance management for " + self.__employee.name, attendance_menu
            )
            match choice:
                case 1:
                    last_msg: str = self.__check()
                case 2:
                    last_msg: str = self.__update()
                case 3:
                    last_msg: str = self.__report()
                case 4:
                    return Ok(None)
                case _:
                    last_msg: str = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def employee(self) -> Result[None, str]:
        last_msg: str = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg: str = ""
            attendance_menu = [
                "[1] Check attendance",
                "[2] Get attendance report",
                "[3] Back",
            ]
            choice = get_user_option_from_menu(
                "Attendance management for " + the_company.logged_in_employee.name,
                attendance_menu,
            )
            match choice:
                case 1:
                    last_msg: str = self.__check()
                case 2:
                    last_msg: str = self.__report()
                case 3:
                    return Ok(None)
                case _:
                    last_msg: str = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def __check(self) -> str:
        attendances = the_company.logged_in_employee.attendance
        payroll = the_company.logged_in_employee.payroll

        try:
            # as an admin checking attendance for other employee
            if not the_company.can_modify("attendance", the_company.logged_in_employee):
                date = input("Enter date (YYYY-MM-DD, leave blank for today): ")
                date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
                is_presence = input("Is employee present? (y/n): ")
                presence: bool = False
                if is_presence.lower() == "y":
                    is_presence = True
                attendances.add_attendance(date, presence).unwrap()
                if not is_presence:
                    reason = input("Enter reason for absent: ")
                    attendances.add_absent_day(date, reason).unwrap()
                    payroll.set_punish("10")

            # as an employee or admin updating their own attendance
            else:
                if (
                    datetime.strftime(datetime.now(), "%Y-%m-%d")
                    in attendances.attendances
                ):
                    return "You are already present!"
                attendances.add_attendance(datetime.now(), True).unwrap()
                return "You are present now!"

        except (ValueError, TypeError) as e:
            return str(e)
        return ""

    def __update(self) -> str:
        attendances = the_company.logged_in_employee.attendance
        payroll = the_company.logged_in_employee.payroll

        date = input("Enter date (YYYY-MM-DD, leave blank for today): ")
        try:
            if not the_company.can_modify("attendance", self.__employee):
                # parse the date, if the date is empty, use today's date
                date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()

                # check if attendance exists for that date
                if date not in attendances.attendances:
                    return "No attendance found for that date!"

                # get the attendance object
                is_presence = input("Is employee present? (y/n): ")
                presence: bool = False
                if is_presence.lower() == "y":
                    presence = True

                # update the attendance
                attendances.add_attendance(date, presence).unwrap()

                # if the employee is absent, ask for the reason
                if not presence:
                    reason = input("Enter reason for absent: ")
                    attendances.add_absent_day(date, reason).unwrap()
                    payroll.set_punish("10")
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
                "Select a year to view attendance report for", year_items
            )
            if selected_year_index == -1:
                return NO_ATTENDANCE_MSG
            elif selected_year_index == -2:
                return ""

            # print the attendance report
            print(
                attendances.get_report(
                    datetime.strptime(year_items[selected_year_index], "%Y")
                )
            )
        else:
            year_items = [str(year) for year in attendances.get_available_years()]
            selected_year_index = get_user_option_from_list(
                "Select a year to view attendance report for", year_items
            )
            if selected_year_index == -1:
                return NO_ATTENDANCE_MSG
            elif selected_year_index == -2:
                return ""

            # print the attendance report
            print(
                attendances.get_report(
                    datetime.strptime(year_items[selected_year_index], "%Y")
                )
            )

        input(ENTER_TO_CONTINUE_MSG)
        return ""
