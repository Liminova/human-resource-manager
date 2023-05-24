import os
import sys


def clrscr():
    return os.system("cls") if sys.platform == "win32" else os.system("clear")
