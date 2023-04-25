from __future__ import annotations
from .COLORS import FCOLORS
import sys

if sys.version_info >= (3, 11):
    from typing import Callable
else:
    from typing_extensions import Callable


def loop_til_valid_input(prompt: str, validator: Callable) -> str:  # type: ignore
    """Takes a prompt and a validator function and keeps asking for input until the validator returns True"""
    user_input = input(f"{prompt}, leave blank to cancel: ")
    if user_input == "":
        confirm = input("Are you sure you want to cancel? (Y/n): ")
        if confirm.lower() != "n":
            return "Input cancelled!"
        user_input = input(f"{prompt}, leave blank to cancel: ")
    while True:
        try:
            validator(user_input).unwrap()  # type: ignore
            break
        except (ValueError, TypeError) as e:
            user_input = input(f"{FCOLORS.RED}{str(e)} Try again: {FCOLORS.END}")
    return ""
