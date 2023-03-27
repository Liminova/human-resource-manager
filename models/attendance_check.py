import datetime as dt
import os
import pickle
import sys

if sys.version_info >= (3, 11):
    from typing import Self, TYPE_CHECKING
else:
    from typing_extensions import Self, TYPE_CHECKING

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

    @leave_balance.setter
    def leave_balance(self, leave_balance: int) -> Self:
        self.__leave_balance = leave_balance
        return self

    @start_date.setter
    def start_date(self, start_date) -> Self:
        self.__start_date = start_date
        return self

    # NOTE: do we really need all the abstractions below?

    # NOTE: true = present, false = absent
    def add_attendance(self, date: dt.datetime, status: bool) -> Self:
        self.__attendance[date] = status
        return self

    # TODO: what is type?
    # add a type hint for type here later. - Rylie
    def add_time_off(self, date: dt.datetime, type):
        self.__time_off[type].append(date)

    def get_attendance(self, date: dt.datetime):
        return self.__attendance[date]

    def get_time_off(self, date: dt.datetime):
        for type in self.__time_off:
            if date in self.__time_off[type]:
                return type
