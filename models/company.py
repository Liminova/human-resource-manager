import sys
from threading import Lock
from option import Result, Ok, Err

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
    def __init__(self) -> None:
        self.__name = ""
        self.__departments = []
        self.__employees = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def departments(self) -> list:
        return self.__departments

    @property
    def employees(self) -> list:
        return self.__employees

    def set_name(self, name: str) -> Result[Self, str]:
        if name == "":
            return Err("Name cannot be empty!")
        self.__name = name
        return Ok(self)
