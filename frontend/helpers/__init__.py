from .clrscr import clrscr
from .COLORS import BCOLORS, FCOLORS
from .get_user_option_from_list import get_user_option_from_list
from .get_user_option_from_menu import get_user_option_from_menu
from .global_styling import *
from .listing import listing
from .loop_til_valid_input import loop_til_valid_input
from .merge_callable import merge_callable
from .refresh_tui import refresh


def styling(x, y):
    return f"- {FCOLORS.CYAN}{x}{FCOLORS.END} {FCOLORS.GREEN}{y}{FCOLORS.END}"


def __error_msg(x):
    return FCOLORS.RED + x + FCOLORS.END


NO_ATTENDANCE_MSG: str = __error_msg("No attendance records available! Please add an attendance record first.")
NO_BENEFIT_MSG: str = __error_msg("No benefit plan available! Please add a benefit plan first.")
NO_DEPARTMENT_MSG: str = __error_msg("No departments available! Please add a department first.")
NO_EMPLOYEE_MSG: str = __error_msg("No employees available! Please add an employee first.")
NO_PAYROLL_MSG: str = __error_msg("No payroll records available! Please add a payroll record first.")
NO_SALES_MSG: str = __error_msg("No sales records available! Please add a sales record first.")

ENTER_TO_CONTINUE_MSG: str = FCOLORS.PURPLE + "Press Enter to continue..." + FCOLORS.END

# fmt: off
__all__ = [
    "clrscr",
    "BCOLORS",
    "FCOLORS",
    "get_user_option_from_list",
    "get_user_option_from_menu",
    "listing",
    "loop_til_valid_input",
    "styling",
    "refresh",
    "merge_callable",
    "NO_ATTENDANCE_MSG",
    "NO_BENEFIT_MSG",
    "NO_DEPARTMENT_MSG",
    "NO_EMPLOYEE_MSG",
    "NO_PAYROLL_MSG",
    "NO_SALES_MSG",
    "ENTER_TO_CONTINUE_MSG",
]
# fmt: on
