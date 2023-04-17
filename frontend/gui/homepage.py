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

        self.frame1 = ctk.CTkFrame(master=self, width=720, height=520, corner_radius=10)
        self.frame1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.label = ctk.CTkLabel(master=self.frame1, text="Welcome to the Human Resources Information System", font=("Century Gothic", 25, "bold"))
        self.label.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        self.label1 = ctk.CTkLabel(master=self.frame1, text="Sign Out", text_color="cyan", font=("Century Gothic", 14, "underline"))
        self.label1.place(relx=0.95, rely=0.975, anchor=tkinter.CENTER)
        self.label1.bind("<Button-1>", lambda event: self.sign_out())

        self.label2 = ctk.CTkLabel(
            master=self.frame1, text=f"You are currently sign in as: {the_company.logged_in_employee.name}", font=("Century Gothic", 14)
        )
        self.label2.place(relx=0.825, rely=0.935, anchor=tkinter.CENTER)

        def button_size(button):
            button.configure(width=260, height=40, font=("Century Gothic", 16, "bold"), corner_radius=10)

        self.button1 = ctk.CTkButton(master=self.frame1, text="Employee Management", command=self.click_employeegui)
        button_size(self.button1)
        self.button1.place(relx=0.25, rely=0.35, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(master=self.frame1, text="Benefit Plan Management", command=self.click_benefitgui)
        button_size(self.button2)
        self.button2.place(relx=0.75, rely=0.35, anchor=tkinter.CENTER)

        self.button3 = ctk.CTkButton(master=self.frame1, text="Attendance Management", command=self.click_attendancegui)
        button_size(self.button3)
        self.button3.place(relx=0.25, rely=0.55, anchor=tkinter.CENTER)

        self.button4 = ctk.CTkButton(master=self.frame1, text="Payroll Management", command=self.click_payrollgui)
        button_size(self.button4)
        self.button4.place(relx=0.75, rely=0.55, anchor=tkinter.CENTER)

        self.button5 = ctk.CTkButton(master=self.frame1, text="Department Management", command=self.click_departmentgui)
        button_size(self.button5)
        self.button5.place(relx=0.25, rely=0.75, anchor=tkinter.CENTER)

        self.button6 = ctk.CTkButton(master=self.frame1, text="Performance Management", command=self.click_performancegui)
        button_size(self.button6)
        self.button6.place(relx=0.75, rely=0.75, anchor=tkinter.CENTER)

    def sign_out(self):
        from .login import Login

        messagebox.showwarning("Sign Out", "Are you sure you want to sign out?", icon="warning", parent=self, type="okcancel")
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
