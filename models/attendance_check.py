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
        self.__allowed_absence_days: dict[int, int] = {}
        self.__attendances: dict[datetime, bool] = {}
        self.__absences: dict[datetime, str] = {}

    @property
    def allowed_absence_days(self) -> int:
        return self.__max_allowed_absence_days

    @property
    def start_date(self) -> datetime:
        return self.__start_date

    @property
    def attendances(self) -> list:
        return self.__attendances

    @property
    def absences(self) -> list:
        return self.__absences

    def strip(self, date: datetime) -> datetime:
        """Strip the time part of the datetime object."""
        return datetime(date.year, date.month, date.day)

    def get_attendance(self, date: datetime) -> Result[bool, str]:
        date = self.strip(date)
        if date in self.__attendances:
            return Ok(self.__attendances[date])
        return Err("Date not found.")

    def get_absence_reason(self, date: datetime) -> Result[str, str]:
        date = self.strip(date)
        if date in self.__absences:
            return Ok(self.__absences[date])
        return Err("Date not found.")

    def get_allowed_absence_days(self, year: int) -> Result[int, str]:
        if year in self.__allowed_absence_days:
            return Ok(self.__allowed_absence_days[year])
        return Err("Year not found.")

    def set_start_date(self, start_date: datetime) -> Result[None, str]:
        self.__start_date = start_date
        return Ok(None)

        return Ok(None)

    def add_absence_day(self, date: datetime, reason: str) -> Result[None, str]:
        date = self.strip(date)
        if not reason:
            return Err("Reason cannot be empty.")
        self.__absences[date] = reason
        self.__allowed_absence_days[date.year] -= 1
        return Ok(None)
