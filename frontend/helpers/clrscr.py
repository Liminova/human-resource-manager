import sys
import os


def clrscr():
    return os.system("cls") if sys.platform == "win32" else os.system("clear")
