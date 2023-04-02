from __future__ import annotations
import sys
import textwrap
from option import Result, Ok, Err
from pydantic import BaseModel

if sys.version_info >= (3, 11):
    from typing import Self, TYPE_CHECKING
else:
    from typing_extensions import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from .employee import Employee

class Department(BaseModel):
    name = ""
    id = ""
    members: list[Employee] = []

    def set_name(self, name: str) -> Result[Self, str]:
        self.name = name
        return Ok(self) if name else Err("Name cannot be empty.")

    def set_id(self, id: str) -> Result[Self, str]:
        self.id = id
        return Ok(self) if id else Err("ID cannot be empty.")

    def __str__(self) -> str:
        data = textwrap.dedent(f"""\
                - Name: {self.name}
                - ID: {self.id}
                - Members:
            """)
        for (i, member) in enumerate(self.members, 1):
            data += f"{i}. {member.name}\n"
        return data

    class Config:
        arbitrary_types_allowed = True
