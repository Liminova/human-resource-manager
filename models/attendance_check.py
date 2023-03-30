import sys
from option import Result, Ok, Err
from datetime import datetime

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class Attendance:
    def __init__(self):
        # date of first attendance
        self.__start_date = datetime.now()
        # number of days the employee absent, they're allowed to be absent 3 days per year before taking a pay cut
        self.__allowed_absence_days = []
        # list of tuples (date, isPresent)
        self.__attendance = []
        # list of tuples (date, reason)
        self.__absences = []

    @property
    def allowed_absence_days(self) -> int:
        return self.__max_allowed_absence_days

    @property
    def start_date(self) -> datetime:
        return self.__start_date

    @property
    def attendance(self) -> list:
        return self.__attendance

    @property
    def absences(self) -> list:
        return self.__absences

    def get_attendance(self, date: str) -> Result[bool, str]:
        if date == None:
            return Err("Date cannot be empty.")
        for d, isPresent in self.__attendance:
            if d == date:
                return Ok(isPresent)
        return Err("Date not found.")

    def get_absence_reason(self, date: str) -> Result[str, str]:
        if date == None:
            return Err("Date cannot be empty.")
        for d, reason in self.__absences:
            if d == date:
                return Ok(reason)
        return Err("Date not found.")

    def get_allowed_absence_days(self, year: int) -> Result[int, str]:
        for y, days in self.__allowed_absence_days:
            if y == year:
                return Ok(days)
        return Err("Year not found.")

    def set_start_date(self, start_date: datetime = None) -> Result[None, str]:
        self.__start_date = start_date
        return Ok(None) if start_date else Err("Start date cannot be empty.")

    def add_attendance(self, date: str, is_presence: bool) -> Result[None, str]:
        # Check the allowed absence days first, if it doesn't contain current year, add it and set to 3
        for year, _ in self.__allowed_absence_days:
            if year == date.year:
                break
        else:
            self.__allowed_absence_days.append((date.year, 3))

        try:
            date = datetime.strptime(date, "%Y-%m-%d")
        except:
            return Err("Date format is incorrect.")
        if is_presence == None:
            return Err("Presence status cannot be empty.")
        self.__attendance[date] = is_presence
        return Ok(None)

    def add_absence_day(self, date: datetime, reason: str) -> Result[None, str]:
        if date == None or reason == None:
            return Err("Date or reason cannot be empty.")
        self.__absences[date] = reason
        self.__allowed_absence_days[date.year] -= 1
        return Ok(None)
