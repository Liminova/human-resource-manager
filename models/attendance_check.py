import datetime as dt
import sys
from option import Result, Ok, Err

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

DEFAULT_LEAVE_BALANCE = 3

class Attendance:
    def __init__(self):
        self.__start_date = dt.datetime.now()
        self.__leave_balance = DEFAULT_LEAVE_BALANCE
        self.__attendance = {}
        self.__time_off = {}

    @property
    def leave_balance(self) -> int:
        return self.__leave_balance

    @property
    def start_date(self) -> dt.datetime:
        return self.__start_date

    def set_leave_balance(self, leave_balance: int = 0) -> Result[Self, str]:
        self.__leave_balance = leave_balance
        return Ok(self) if leave_balance else Err("Leave balance cannot be empty.")

    def set_start_date(self, start_date: dt.datetime = None) -> Result[Self, str]:
        self.__start_date = start_date
        return Ok(self) if start_date else Err("Start date cannot be empty.")

    # NOTE: do we really need all the abstractions below?

    # NOTE: true = present, false = absent
    def add_attendance(self, date: dt.datetime, status: bool) -> Self:
        if date is None:
            return Err("Date or status cannot be empty.")
        self.__attendance[date] = status
        return Ok(self)

    # TODO: what is type?
    # add a type hint for type here later. - Rylie
    def add_time_off(self, date: dt.datetime, type):
        self.__time_off[type].append(date)

    def get_attendance(self, date: dt.datetime) -> Result[bool, str]:
        return Ok(self.__attendance[date]) if date in self.__attendance else Err("Date not found.")

    def get_time_off(self, date: dt.datetime) -> Result[str, str]:
        for type in self.__time_off:
            if date in self.__time_off[type]:
                return Ok(type)
        return Err("Date not found.")
