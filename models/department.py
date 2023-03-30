from __future__ import annotations
import sys
import textwrap
from option import Result, Ok, Err

if sys.version_info >= (3, 11):
    from typing import Self, TYPE_CHECKING
else:
    from typing_extensions import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from .employee import Employee

class Department:
    def __init__(self) -> None:
        self.__name = ""
        self.__id = ""
        self.__members = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def id(self) -> str:
        return self.__id

    @property
    def members(self) -> list[Employee]:
        return self.__members

    def set_name(self, name: str) -> Result[Self, str]:
        self.__name = name
        return Ok(self) if name else Err("Name cannot be empty.")

    def set_id(self, id: str) -> Result[Self, str]:
        self.__id = id
        return Ok(self) if id else Err("ID cannot be empty.")

    def __str__(self) -> str:
        data = textwrap.dedent(f"""\
                - Name: {self.__name}
                - ID: {self.__id}
                - Members:
            """)
        for (i, member) in enumerate(self.__members, 1):
            data += f"{i}. {member.name}\n"
        return data
