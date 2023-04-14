from __future__ import annotations
import sys
from option import Result, Ok, Err
from datetime import datetime
from pydantic import BaseModel, Field

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class Attendance(BaseModel):
    start_date: datetime = Field(default_factory=datetime.now)
    allowed_absent_days: dict[int, int] = Field(default_factory=dict)
    attendances: dict[str, bool] = Field(default_factory=dict)
    absents: dict[str, str] = Field(default_factory=dict)

    def get_attendance(self, date: datetime) -> Result[bool, str]:
        date_str = date.strftime("%Y-%m-%d")
        if date_str in self.attendances:
            return Ok(self.attendances[date_str])
        return Err("Date not found.")

    def get_absent_reason(self, date: datetime) -> Result[str, str]:
        date_str = date.strftime("%Y-%m-%d")
        if date_str in self.absents:
            return Ok(self.absents[date_str])
        return Err("Date not found.")

    def get_allowed_absent_days(self, year: int) -> Result[int, str]:
        if year in self.allowed_absent_days:
            return Ok(self.allowed_absent_days[year])
        return Err("Year not found.")

    def set_start_date(self, start_date: datetime) -> Result[Self, str]:
        self.start_date = start_date.strftime("%Y-%m-%d")
        return Ok(self)

    def add_attendance(self, date: datetime, is_present: bool) -> Result[Self, str]:
        date_str = date.strftime("%Y-%m-%d")
        # Check the "allowed_absent_days" first, if it doesn't contain current year, add it and set to 3
        if date.year not in self.allowed_absent_days:
            self.allowed_absent_days[date.year] = 3
        self.attendances[date_str] = is_present
        return Ok(self)

    def add_absent_day(self, date: datetime, reason: str) -> Result[Self, str]:
        date_str = date
        if not reason:
            return Err("Reason cannot be empty.")
        self.absents[date_str] = reason
        self.allowed_absent_days[date.year] -= 1
        return Ok(Self)

    class Config:
        arbitrary_types_allowed = True

    def get_available_years(self) -> list[int]:
        """For user to choose in the attendance report menu."""
        years: list[int] = []
        for date in self.attendances.keys():
            date = datetime.strptime(date, "%Y-%m-%d")
            if date.year not in years:
                years.append(date.year)
        return years

    def get_report(self, year: datetime) -> str:
        """Get the attendance report for a specific year."""
        data = ""  # temporary variable to store the report data
        for date, is_present in self.attendances.items():
            # only get the attendance data for the specified year
            date = datetime.strptime(date, "%Y-%m-%d")
            if date.year == year:
                # different message if the employee is present or absent
                if is_present:
                    data += f"{datetime.strftime(date, '%d %b %Y')} - Present\n"
                else:
                    absent_reason = self.absents.get(date, "No reason")
                    data += f"{datetime.strftime(date, '%d %b %Y')} - Absent ({absent_reason})\n"
        return data
