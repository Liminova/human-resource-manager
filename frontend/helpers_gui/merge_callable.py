from typing import Callable


def merge_callable(*args: Callable) -> Callable:
    def wrapper():
        for callable in args:
            callable()

    return wrapper
