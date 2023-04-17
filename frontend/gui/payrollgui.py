import customtkinter as ctk
import tkinter
from tkinter import messagebox
import os

from models import Company, Payroll
from database.mongo import employee_repo
from frontend.helpers import merge_callable

the_company = Company()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

Width = 1024
Height = 768


class PayrollGui(ctk.CTk):
    def __init__(self, master=None):
        super().__init__()
        self.title("Payroll Management")
        self.geometry(f"{Width}x{Height}")
        self.resizable(True, True)
        self.left_frame = ctk.CTkFrame(master=self, corner_radius=10)

        if the_company.logged_in_employee.is_admin:
            self.admin()
        else:
            self.employee()

        self.left_frame.pack(side=ctk.LEFT)
        self.left_frame.pack_propagate(False)
        self.left_frame.configure(width=320, height=760)

        self.right_frame = ctk.CTkFrame(master=self, border_width=2, corner_radius=10)
        self.right_frame.pack(side=ctk.RIGHT)
        self.right_frame.pack_propagate(False)
        self.right_frame.configure(width=700, height=760)

    def admin(self):
        self.button1 = ctk.CTkButton(
            master=self.left_frame, text="Create Payroll", command=merge_callable(self.__destroy_all_frames, self.__admin_create_payroll)
        )
        self.__button_style(self.button1)
        self.button1.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(
            master=self.left_frame, text="Update Payroll", command=merge_callable(self.__destroy_all_frames, self.__admin_update_payroll)
        )
        self.__button_style(self.button2)
        self.button2.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        self.button3 = ctk.CTkButton(
            master=self.left_frame, text="View Payroll", command=merge_callable(self.__destroy_all_frames, self.__admin_view_payroll)
        )
        self.__button_style(self.button3)
        self.button3.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.button4 = ctk.CTkButton(master=self.left_frame, text="Back", command=lambda self=self: self.__back_to_homepage())
        self.button4.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="red")
        self.button4.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

    def employee(self):
        self.button1 = ctk.CTkButton(
            master=self.left_frame, text="View Payroll", command=merge_callable(self.__destroy_all_frames, self.__employee_view_payroll)
        )
        self.__button_style(self.button1)
        self.button1.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(master=self.left_frame, text="Back", command=lambda self=self: self.__back_to_homepage())
        self.button2.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="red")
        self.button2.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

    def __style_input_box(self, element):
        element.configure(width=400, height=30, font=("Century Gothic", 14), corner_radius=10)

    def __button_style(self, button):
        button.configure(width=260, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10)

    def __destroy_all_frames(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def __back_to_homepage(self):
        from .homepage import Homepage

        self.destroy()
        Homepage().mainloop()

    # region: admin functions

    def __admin_create_payroll(self):
        self.button1_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button1_frame, text="Create Payroll", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Employee ID: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.1, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
        self.__style_input_box(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.label2 = ctk.CTkLabel(master=self.right_frame, text="Salary: ", font=("Century Gothic", 20, "italic"))
        self.label2.place(relx=0.1, rely=0.25, anchor=tkinter.CENTER)

        self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Salary")
        self.__style_input_box(self.entry2)
        self.entry2.place(relx=0.325, rely=0.295, anchor=tkinter.CENTER)

        self.label3 = ctk.CTkLabel(master=self.right_frame, text="Bonus: ", font=("Century Gothic", 20, "italic"))
        self.label3.place(relx=0.1, rely=0.35, anchor=tkinter.CENTER)

        self.entry3 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Bonus")
        self.__style_input_box(self.entry3)
        self.entry3.place(relx=0.325, rely=0.395, anchor=tkinter.CENTER)

        self.label4 = ctk.CTkLabel(master=self.right_frame, text="Tax: ", font=("Century Gothic", 20, "italic"))
        self.label4.place(relx=0.1, rely=0.45, anchor=tkinter.CENTER)

        self.entry4 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Tax")
        self.__style_input_box(self.entry4)
        self.entry4.place(relx=0.325, rely=0.495, anchor=tkinter.CENTER)

        self.label5 = ctk.CTkLabel(master=self.right_frame, text="Punishment: ", font=("Century Gothic", 20, "italic"))
        self.label5.place(relx=0.1, rely=0.55, anchor=tkinter.CENTER)

        self.entry5 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Punishment")
        self.__style_input_box(self.entry5)
        self.entry5.place(relx=0.325, rely=0.595, anchor=tkinter.CENTER)

        self.button1 = ctk.CTkButton(master=self.right_frame, text="Create", command=(lambda: create_successfully(self)))
        self.button1.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button1.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        self.button1_frame.pack(pady=20)

        def create_successfully(self):
            salary = self.entry1.get()
            bonus = self.entry2.get()
            tax = self.entry3.get()
            punishment = self.entry4.get()
            input_id = self.entry5.get()
            if salary == "" or bonus == "" or tax == "" or punishment == "":
                messagebox.showerror("Error", "Please fill in all the fields")
            elif not salary.isdigit() or not bonus.isdigit() or not tax.isdigit() or not punishment.isdigit():
                messagebox.showerror("Error", "Please enter a valid number")
            else:
                for e in the_company.employees:
                    if e.employee_id == input_id:
                        e.payroll = (
                            Payroll().set_salary(salary).unwrap().set_bonus(bonus).unwrap().set_tax(tax).unwrap().set_punish(punishment).unwrap()
                        )
                        if os.getenv("HRMGR_DB") == "TRUE":
                            employee_repo.update_one({"_id": e.id}, {"$set": e.dict(include={"payroll"})}, upsert=True)
                        messagebox.showinfo("Success", "Payroll created successfully")
                    else:
                        messagebox.showerror("Error", "Employee ID not found")

    def __admin_update_payroll(self):
        self.button2_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button2_frame, text="Update Payroll", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Employee ID: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.1, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
        self.__style_input_box(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.label2 = ctk.CTkLabel(master=self.right_frame, text="Salary: ", font=("Century Gothic", 20, "italic"))
        self.label2.place(relx=0.1, rely=0.25, anchor=tkinter.CENTER)

        self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Salary")
        self.__style_input_box(self.entry2)
        self.entry2.place(relx=0.325, rely=0.295, anchor=tkinter.CENTER)

        self.label3 = ctk.CTkLabel(master=self.right_frame, text="Bonus: ", font=("Century Gothic", 20, "italic"))
        self.label3.place(relx=0.1, rely=0.35, anchor=tkinter.CENTER)

        self.entry3 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Bonus")
        self.__style_input_box(self.entry3)
        self.entry3.place(relx=0.325, rely=0.395, anchor=tkinter.CENTER)

        self.label4 = ctk.CTkLabel(master=self.right_frame, text="Tax: ", font=("Century Gothic", 20, "italic"))
        self.label4.place(relx=0.1, rely=0.45, anchor=tkinter.CENTER)

        self.entry4 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Tax")
        self.__style_input_box(self.entry4)
        self.entry4.place(relx=0.325, rely=0.495, anchor=tkinter.CENTER)

        self.label5 = ctk.CTkLabel(master=self.right_frame, text="Punishment: ", font=("Century Gothic", 20, "italic"))
        self.label5.place(relx=0.1, rely=0.55, anchor=tkinter.CENTER)

        self.entry5 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Punishment")
        self.__style_input_box(self.entry5)
        self.entry5.place(relx=0.325, rely=0.595, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(master=self.right_frame, text="Update", command=(lambda: update_successfully(self)))
        self.button2.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button2.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        self.button2_frame.pack(pady=20)

        def update_successfully(self):
            salary = self.entry1.get()
            bonus = self.entry2.get()
            tax = self.entry3.get()
            punishment = self.entry4.get()
            input_id = self.entry5.get()
            if salary == "" or bonus == "" or tax == "" or punishment == "":
                messagebox.showerror("Error", "Please fill in all the fields")
            elif not salary.isdigit() or not bonus.isdigit() or not tax.isdigit() or not punishment.isdigit():
                messagebox.showerror("Error", "Please enter a valid number")
            else:
                for e in the_company.employees:
                    if e.employee_id == input_id:
                        e.payroll = (
                            Payroll().set_salary(salary).unwrap().set_bonus(bonus).unwrap().set_tax(tax).unwrap().set_punish(punishment).unwrap()
                        )
                        if os.getenv("HRMGR_DB") == "TRUE":
                            employee_repo.update_one({"_id": e.id}, {"$set": e.dict(include={"payroll"})}, upsert=True)
                        messagebox.showinfo("Success", "Payroll created successfully")
                    else:
                        messagebox.showerror("Error", "Employee ID not found")

    def __admin_view_payroll(self):
        self.button3_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button3_frame, text="View Payroll", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Employee ID: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.1, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
        self.__style_input_box(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.button3 = ctk.CTkButton(master=self.right_frame, text="View", command=(lambda: view_successfully(self)))
        self.button3.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button3.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        self.button3_frame.pack(pady=20)

        def view_successfully(self):
            input_id = self.entry1.get()
            if input_id == "":
                messagebox.showerror("Error", "Please fill in all the fields")
            else:
                for e in the_company.employees:
                    if e.employee_id == input_id:
                        messagebox.showinfo("Success", "Payroll created successfully")
                    else:
                        messagebox.showerror("Error", "Employee ID not found")

    # endregion

    # region: employee functions

    def __employee_view_payroll(self):
        self.button4_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button4_frame, text="View Payroll", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Employee ID: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.1, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
        self.__style_input_box(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.button4 = ctk.CTkButton(master=self.right_frame, text="View", command=(lambda: view_successfully(self)))
        self.button4.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button4.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        self.button4_frame.pack(pady=20)

        def view_successfully(self):
            input_id = self.entry1.get()
            if input_id == "":
                messagebox.showerror("Error", "Please fill in all the fields")
            else:
                for e in the_company.employees:
                    if e.employee_id == input_id:
                        messagebox.showinfo("Success", "Payroll created successfully")
                    else:
                        messagebox.showerror("Error", "Employee ID not found")

    # endregion
