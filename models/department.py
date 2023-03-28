from __future__ import annotations
import sys

if sys.version_info >= (3, 11):
    from typing import Self, TYPE_CHECKING
else:
    from typing_extensions import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from .employee import Employee

class Department:
    def __init__(self) -> None:
        self.__name = ""
        # NOTE: maybe we don't need id for departments? food for thoughts.
        # - Rylie
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

    @name.setter
    def name(self, name: str) -> Self:
        self.__name = name
        return self

    @id.setter
    def id(self, id: str) -> Self:
        self.__id = id
        return self


    # NOTE: maybe we should only display the member's name instead of their
    # full info? - Rylie
    def display(self) -> None:
        print(f"- Name: {self.__name}")
        print(f"- ID: {self.__id}")
        print("- Members:")
        for (i, employee) in enumerate(self.__members, 1):
            print(f"Member {i}:")
            print(employee)
            print()
