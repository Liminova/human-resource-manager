from __future__ import annotations
import sys
import textwrap
from option import Result, Ok, Err
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from frontend.helpers_tui import styling

from database.pyobjectid import PyObjectId

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from .employee import Employee


class Department(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(default_factory=str)
    dept_id: str = Field(default_factory=str)
    members: list[Employee] = Field(default_factory=list)

    def set_name(self, name: str) -> Result[Self, str]:
        self.name = name
        return Ok(self) if name else Err("Name cannot be empty.")

    def set_id(self, id: str) -> Result[Self, str]:
        self.dept_id = id
        return Ok(self) if id else Err("ID cannot be empty.")

    def __str__(self) -> str:
        data = textwrap.dedent(
            f"""\
                {styling('Name', self.name)}
                {styling('ID', self.dept_id)}
                {styling('Members', len(self.members))}
            """
        )
        for i, member in enumerate(self.members, 1):
            data += f"  {styling(i, member.name)} ({member.employee_id})\n"
        return data

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
