# Payroll GUI: implement set_salary, set_bonus, set_tax, set_punish, calculate_bonus, calculate_total

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from models.payroll import Payroll
from models.employee import Employee
from typing import List, Tuple, Callable, Any

class PayrollGUI: 
    def __init__(self, employees: List[Employee]):
        self.__employees = employees
        self.__payroll = Payroll()

    def start(self) -> Tuple[bool, str]:
        self.__root = tk.Tk()
        self.__root.title("Payroll Menu")
        self.__root.geometry("500x500")
        self.__root.resizable(False, False)

        self.__frame = ttk.Frame(self.__root)
        self.__frame.pack(fill=tk.BOTH, expand=True)

        self.__main_menu = [
            ("Set salary", self.__set_salary),
            ("Set bonus", self.__set_bonus),
            ("Set tax", self.__set_tax),
            ("Set punish", self.__set_punish),
            ("Calculate bonus", self.__calculate_bonus),
            ("Calculate total", self.__calculate_total),
            ("Exit", self.__exit),
        ]

        self.__last_msg = ""
        self.__last_msg_label = ttk.Label(self.__frame, text=self.__last_msg)
        self.__last_msg_label.pack()

        self.__buttons = []
        for text, command in self.__main_menu:
            button = ttk.Button(self.__frame, text=text, command=command)
            button.pack(fill=tk.X, expand=True)
            self.__buttons.append(button)

        self.__root.mainloop()

    def __set_salary(self) -> None:
        self.__root.destroy()
        self.__root = tk.Tk()
        self.__root.title("Set Salary")
        self.__root.geometry("500x500")
        self.__root.resizable(False, False)

        self.__frame = ttk.Frame(self.__root)
        self.__frame.pack(fill=tk.BOTH, expand=True)

        self.__last_msg = ""
        self.__last_msg_label = ttk.Label(self.__frame, text=self.__last_msg)
        self.__last_msg_label.pack()

        self.__salary_label = ttk.Label(self.__frame, text="Salary")
        self.__salary_label.pack()

        self.__salary_entry = ttk.Entry(self.__frame)
        self.__salary_entry.pack()

        self.__submit_button = ttk.Button(self.__frame, text="Submit", command=self.__submit_salary)
        self.__submit_button.pack()

        self.__root.mainloop()

    def __submit_salary(self) -> None:
        salary = self.__salary_entry.get()
        result = self.__payroll.set_salary(salary)
        if result.is_ok():
            self.__last_msg = "Salary set successfully"
        else:
            self.__last_msg = result.get_error()
        self.__last_msg_label.config(text=self.__last_msg)

    def __set_bonus(self) -> None:
        self.__root.destroy()
        self.__root = tk.Tk()
        self.__root.title("Set Bonus")
        self.__root.geometry("500x500")
        self.__root.resizable(False, False)

        self.__frame = ttk.Frame(self.__root)
        self.__frame.pack(fill=tk.BOTH, expand=True)

        self.__last_msg = ""
        self.__last_msg_label = ttk.Label(self.__frame, text=self.__last_msg)
        self.__last_msg_label.pack()

        self.__bonus_label = ttk.Label(self.__frame, text="Bonus")
        self.__bonus_label.pack()

        self.__bonus_entry = ttk.Entry(self.__frame)
        self.__bonus_entry.pack()

        self.__submit_button = ttk.Button(self.__frame, text="Submit", command=self.__submit_bonus)
        self.__submit_button.pack()

        self.__root.mainloop()

    def __submit_bonus(self) -> None:
        bonus = self.__bonus_entry.get()
        result = self.__payroll.set_bonus(bonus)
        if result.is_ok():
            self.__last_msg = "Bonus set successfully"
        else:
            self.__last_msg = result.get_error()
        self.__last_msg_label.config(text=self.__last_msg)

    def __set_tax(self) -> None:
        self.__root.destroy()
        self.__root = tk.Tk()
        self.__root.title("Set Tax")
        self.__root.geometry("500x500")
        self.__root.resizable(False, False)

        self.__frame = ttk.Frame(self.__root)
        self.__frame.pack(fill=tk.BOTH, expand=True)

        self.__last_msg = ""
        self.__last_msg_label = ttk.Label(self.__frame, text=self.__last_msg)
        self.__last_msg_label.pack()

        self.__tax_label = ttk.Label(self.__frame, text="Tax")
        self.__tax_label.pack()

        self.__tax_entry = ttk.Entry(self.__frame)
        self.__tax_entry.pack()

        self.__submit_button = ttk.Button(self.__frame, text="Submit", command=self.__submit_tax)
        self.__submit_button.pack()

        self.__root.mainloop()

    def __submit_tax(self) -> None:
        tax = self.__tax_entry.get()
        result = self.__payroll.set_tax(tax)
        if result.is_ok():
            self.__last_msg = "Tax set successfully"
        else:
            self.__last_msg = result.get_error()
        self.__last_msg_label.config(text=self.__last_msg)

    def __set_punish(self) -> None:
        self.__root.destroy()
        self.__root = tk.Tk()
        self.__root.title("Set Punish")
        self.__root.geometry("500x500")
        self.__root.resizable(False, False)

        self.__frame = ttk.Frame(self.__root)
        self.__frame.pack(fill=tk.BOTH, expand=True)

        self.__last_msg = ""
        self.__last_msg_label = ttk.Label(self.__frame, text=self.__last_msg)
        self.__last_msg_label.pack()

        self.__punish_label = ttk.Label(self.__frame, text="Punish")
        self.__punish_label.pack()

        self.__punish_entry = ttk.Entry(self.__frame)
        self.__punish_entry.pack()

        self.__submit_button = ttk.Button(self.__frame, text="Submit", command=self.__submit_punish)
        self.__submit_button.pack()

        self.__root.mainloop()

    def __submit_punish(self) -> None:
        punish = self.__punish_entry.get()
        result = self.__payroll.set_punish(punish)
        if result.is_ok():
            self.__last_msg = "Punish set successfully"
        else:
            self.__last_msg = result.get_error()
        self.__last_msg_label.config(text=self.__last_msg)

    def __calculate(self) -> None:
        self.__root.destroy()
        self.__root = tk.Tk()
        self.__root.title("Calculate")
        self.__root.geometry("500x500")
        self.__root.resizable(False, False)

        self.__frame = ttk.Frame(self.__root)
        self.__frame.pack(fill=tk.BOTH, expand=True)

        self.__last_msg = ""
        self.__last_msg_label = ttk.Label(self.__frame, text=self.__last_msg)
        self.__last_msg_label.pack()

        self.__result_label = ttk.Label(self.__frame, text="")
        self.__result_label.pack()

        self.__calculate_button = ttk.Button(self.__frame, text="Calculate", command=self.__calculate_result)
        self.__calculate_button.pack()

        self.__root.mainloop()

    def __calculate_result(self) -> None:
        result = self.__payroll.calculate()
        if result.is_ok():
            self.__last_msg = "Calculated successfully"
            self.__result_label.config(text=f"Result: {result.get_value()}")
        else:
            self.__last_msg = result.get_error()
            self.__result_label.config(text="")
        self.__last_msg_label.config(text=self.__last_msg)

if __name__ == "__main__":
    PayrollApp()