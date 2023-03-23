import sys
from threading import Lock

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

# thread-safe singleton implementation, there should only be one instance of
# Company existing at all times.
class CompanyMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class Company(metaclass=CompanyMeta):
    def __init__(self, name: str, departments: list, employees: list) -> None:
        self.__name = name
        self.__departments = departments
        self.__employees = employees

    @property
    def name(self) -> str:
        return self.__name

    @property
    def departments(self) -> list:
        return self.__departments

    @property
    def employees(self) -> list:
        return self.__employees

    @name.setter
    def name(self, name: str) -> Self:
        self.__name = name
        return self

    @departments.setter
    def departments(self, departments: list) -> Self:
        self.__departments = departments
        return self

    @employees.setter
    def employees(self, employees: list) -> Self:
        self.__employees = employees
        return self
