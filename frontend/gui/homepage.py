import customtkinter as ctk
import tkinter
from tkinter import messagebox
from models import Company

width = 800
height = 640

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

the_company = Company()


class Homepage(ctk.CTk):
    def __init__(self, master=None):
        super().__init__()

        self.title("Human Resources Information System Management")
        self.geometry(f"{width}x{height}")
        self.resizable(True, True)

        self.main_frame = ctk.CTkFrame(master=self, width=720, height=520, corner_radius=10)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        ctk.CTkLabel(
            master=self.main_frame,
            text="Welcome to the Human Resources Information System",
            font=("Century Gothic", 25, "bold"),
        ).place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        signout_hyperlink = ctk.CTkLabel(
            master=self.main_frame, text="Sign Out", text_color="cyan", font=("Century Gothic", 14, "underline")
        )
        signout_hyperlink.place(relx=0.95, rely=0.975, anchor=tkinter.CENTER)
        signout_hyperlink.bind("<Button-1>", lambda event: self.sign_out())

        ctk.CTkLabel(
            master=self.main_frame,
            text=f"You are currently sign in as: {the_company.logged_in_employee.name}",
            font=("Century Gothic", 14),
        ).place(relx=0.825, rely=0.935, anchor=tkinter.CENTER)

        _btn_style = dict(width=260, height=40, font=("Century Gothic", 16, "bold"), corner_radius=10)

        ctk.CTkButton(
            master=self.main_frame, text="Employee Management", command=self.click_employeegui, **_btn_style
        ).place(relx=0.25, rely=0.35, anchor=tkinter.CENTER)

        ctk.CTkButton(
            master=self.main_frame, text="Benefit Plan Management", command=self.click_benefitgui, **_btn_style
        ).place(relx=0.75, rely=0.35, anchor=tkinter.CENTER)

        ctk.CTkButton(
            master=self.main_frame, text="Attendance Management", command=self.click_attendancegui, **_btn_style
        ).place(relx=0.25, rely=0.55, anchor=tkinter.CENTER)

        ctk.CTkButton(master=self.main_frame, text="Payroll Management", command=self.click_payrollgui, **_btn_style).place(
            relx=0.75, rely=0.55, anchor=tkinter.CENTER
        )

        ctk.CTkButton(
            master=self.main_frame, text="Department Management", command=self.click_departmentgui, **_btn_style
        ).place(relx=0.25, rely=0.75, anchor=tkinter.CENTER)

        ctk.CTkButton(
            master=self.main_frame, text="Performance Management", command=self.click_performancegui, **_btn_style
        ).place(relx=0.75, rely=0.75, anchor=tkinter.CENTER)

    def sign_out(self):
        from .login import Login

        messagebox.showwarning(
            "Sign Out", "Are you sure you want to sign out?", icon="warning", parent=self, type="okcancel"
        )
        self.destroy()
        Login().mainloop()

    def click_employeegui(self):
        from .employeegui import EmployeeGui

        self.destroy()
        EmployeeGui().mainloop()

    def click_benefitgui(self):
        from .benefitplangui import BenefitPlanGui

        self.destroy()
        BenefitPlanGui().mainloop()

    def click_attendancegui(self):
        from .attendancegui import AttendanceGui

        self.destroy()
        AttendanceGui().mainloop()

    def click_payrollgui(self):
        from .payrollgui import PayrollGui

        self.destroy()
        PayrollGui().mainloop()

    def click_departmentgui(self):
        from .departmentgui import DepartmentGui

        self.destroy()
        DepartmentGui().mainloop()

    def click_performancegui(self):
        from .performancegui import PerformanceGui

        self.destroy()
        PerformanceGui().mainloop()


if __name__ == "__main__":
    Homepage().mainloop()
