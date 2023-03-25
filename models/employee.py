import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

# NOTE: possible abstraction: split name and id into its own Entity class or
# something, though i don't like that approach very much tbh - Rylie
class Employee:
    def __init__(
        self, name: str, dob: str,
        id: str, phone: str, department: str
    ) -> None:
        self.__name = name
        self.__dob = dob
        self.__id = id
        self.__phone = phone
        # TODO: think of some way to decouple department members list and
        # members being a part of departments, it's kinda a circle dependency
        # rn. - Rylie
        self.__department = department

    @property
    def name(self) -> str:
        return self.__name

    @property
    def dob(self) -> str:
        return self.__dob

    @property
    def id(self) -> str:
        return self.__id

    @property
    def phone(self) -> str:
        return self.__phone

    @property
    def department(self) -> str:
        return self.__department

    @name.setter
    def name(self, name: str) -> Self:
        self.__name = name
        return self

    @dob.setter
    def dob(self, dob: str) -> Self:
        self.__dob = dob
        return self

    @id.setter
    def id(self, id: str) -> Self:
        self.__id = id
        return self

    @phone.setter
    def phone(self, phone: str) -> Self:
        self.__phone = phone
        return self

    @department.setter
    def department(self, department: str) -> Self:
        self.__department = department
        return self
