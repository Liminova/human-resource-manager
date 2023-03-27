from __future__ import annotations
import sys

if sys.version_info >= (3, 11):
    from typing import Self, TYPE_CHECKING
else:
    from typing_extensions import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from .employee import Employee

class Department:
    def __init__(self, name: str, id: str, members: list[Employee]) -> None:
        self.__name = name
        # NOTE: maybe we don't need id for departments? food for thoughts.
        # - Rylie
        self.__id = id
        self.__members = members

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

    @members.setter
    def members(self, members: list[Employee]) -> Self:
        self.__members = members
        return self
