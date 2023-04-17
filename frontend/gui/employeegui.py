import customtkinter as ctk
import tkinter
import os

from models import Company, Employee, hash
from database.mongo import employee_repo
from tkinter import messagebox as msgbox
from frontend.helpers import merge_callable

the_company = Company()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

Width = 1024
Height = 768


class EmployeeGui(ctk.CTk):
    def __init__(self, master=None):
        super().__init__()
        self.title("Employee Management")
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
            master=self.left_frame, text="Add Employee", command=merge_callable(self.__destroy_all_frames, self.__admin_add_employee)
        )
        self.__button_style(self.button1)
        self.button1.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(
            master=self.left_frame, text="Remove Employee", command=merge_callable(self.__destroy_all_frames, self.__admin_remove_employee)
        )
        self.__button_style(self.button2)
        self.button2.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        self.button3 = ctk.CTkButton(
            master=self.left_frame, text="Update Employee", command=merge_callable(self.__destroy_all_frames, self.__admin_update_employee)
        )
        self.__button_style(self.button3)
        self.button3.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.button4 = ctk.CTkButton(
            master=self.left_frame, text="View Employee", command=merge_callable(self.__destroy_all_frames, self.__admin_view_employee)
        )
        self.__button_style(self.button4)
        self.button4.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        self.button5 = ctk.CTkButton(
            master=self.left_frame, text="View All Employees", command=merge_callable(self.__destroy_all_frames, self.__admin_list_all_employees)
        )
        self.__button_style(self.button5)
        self.button5.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.button6 = ctk.CTkButton(
            master=self.left_frame, text="Change Password", command=merge_callable(self.__destroy_all_frames, self.__admin_change_password)
        )
        self.__button_style(self.button6)
        self.button6.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        self.button7 = ctk.CTkButton(master=self.left_frame, text="Back", command=lambda self=self: self.__back_to_homepage())
        self.button7.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="red")
        self.button7.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

    def employee(self):
        self.button4 = ctk.CTkButton(
            master=self.left_frame, text="View Employee", command=merge_callable(self.__destroy_all_frames, self.__employee_view_employee)
        )
        self.__button_style(self.button4)
        self.button4.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        self.button6 = ctk.CTkButton(
            master=self.left_frame, text="Change Password", command=merge_callable(self.__destroy_all_frames, self.__employee_change_password)
        )
        self.__button_style(self.button6)
        self.button6.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

        self.button7 = ctk.CTkButton(master=self.left_frame, text="Back", fg_color="red", command=lambda self=self: self.__back_to_homepage())
        self.button7.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="red")
        self.button7.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

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

    def __admin_add_employee(self):
        self.button1_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button1_frame, text="Information", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Name: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.1, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Name")
        self.__style_input_box(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.label2 = ctk.CTkLabel(master=self.right_frame, text="Date of birth: ", font=("Century Gothic", 20, "italic"))
        self.label2.place(relx=0.145, rely=0.275, anchor=tkinter.CENTER)

        self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="YYYY-MM-DD")
        self.__style_input_box(self.entry2)
        self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

        self.label3 = ctk.CTkLabel(master=self.right_frame, text="ID: ", font=("Century Gothic", 20, "italic"))
        self.label3.place(relx=0.0715, rely=0.4, anchor=tkinter.CENTER)

        self.entry3 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
        self.__style_input_box(self.entry3)
        self.entry3.place(relx=0.325, rely=0.445, anchor=tkinter.CENTER)

        self.label4 = ctk.CTkLabel(master=self.right_frame, text="Phone Number: ", font=("Century Gothic", 20, "italic"))
        self.label4.place(relx=0.155, rely=0.525, anchor=tkinter.CENTER)

        self.entry4 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Phone Number")
        self.__style_input_box(self.entry4)
        self.entry4.place(relx=0.325, rely=0.57, anchor=tkinter.CENTER)

        self.label5 = ctk.CTkLabel(master=self.right_frame, text="Email: ", font=("Century Gothic", 20, "italic"))
        self.label5.place(relx=0.09, rely=0.65, anchor=tkinter.CENTER)

        self.entry5 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Email")
        self.__style_input_box(self.entry5)
        self.entry5.place(relx=0.325, rely=0.695, anchor=tkinter.CENTER)

        self.label6 = ctk.CTkLabel(master=self.right_frame, text="Password: ", font=("Century Gothic", 20, "italic"))
        self.label6.place(relx=0.125, rely=0.775, anchor=tkinter.CENTER)

        self.entry6 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Password", show="*")
        self.__style_input_box(self.entry6)
        self.entry6.place(relx=0.325, rely=0.82, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="Confirm", command=(lambda: add_successfully(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        self.button1_frame.pack(pady=20)

        def add_successfully(self):
            name = self.entry1.get()
            dob = self.entry2.get()
            empl_id = self.entry3.get()
            phone = self.entry4.get()
            email = self.entry5.get()
            employee = Employee()
            password = self.entry6.get()
            if name == "" or dob == "" or id == "" or phone == "" or email == "":
                msgbox.showerror("Error", "Please fill in all the fields")
            elif not name.isalpha():
                msgbox.showerror("Error", "Please enter a valid name")
            elif not phone.isdigit() and len(phone) != 10:
                msgbox.showerror("Error", "Please enter a valid phone number")
            elif "@" not in email:
                msgbox.showerror("Error", "Please enter a valid email")
            elif "-" not in dob:
                msgbox.showerror("Error", "Please enter a valid date of birth")
            else:
                employee.name = name
                employee.dob = dob
                employee.employee_id = empl_id
                employee.phone = phone
                employee.email = email
                employee.hashed_password = hash(employee.employee_id, password)
                the_company.employees.append(employee)

                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.insert_one(employee.dict(by_alias=True))
                msgbox.showinfo("Success", "Employee added successfully")

    def __admin_remove_employee(self):
        self.button2_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button2_frame, text="Remove Employee", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Employee's name: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.175, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter employee's name")
        self.__style_input_box(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.label2 = ctk.CTkLabel(master=self.right_frame, text="Employee's ID: ", font=("Century Gothic", 20, "italic"))
        self.label2.place(relx=0.145, rely=0.275, anchor=tkinter.CENTER)

        self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter employee's ID")
        self.__style_input_box(self.entry2)
        self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="Remove", fg_color="red", command=(lambda: remove_successfully(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10)
        self.button.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

        self.button2_frame.pack(pady=20)

        def remove_successfully(self):
            employee_name = self.entry1.get()
            employee_id = self.entry2.get()
            if employee_name == "" and employee_id == "":
                msgbox.showerror("Error", "Please fill in at least one field")

            for e in the_company.employees:
                # finding the employee by name or id
                found_employee_by_name = e.name == employee_name
                found_employee_by_id = e.employee_id == employee_id if employee_id else False
                if not (found_employee_by_name or found_employee_by_id):
                    continue

                # removing the employee
                the_company.employees.remove(e)
                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.delete_one({"_id": e.id})
                break
            else:
                msgbox.showerror("Error", "Employee not found")
                return

            msgbox.showinfo("Success", "Employee removed successfully")

    def __admin_update_employee(self):
        self.label0 = ctk.CTkLabel(master=self.right_frame, text="Enter ID: ", font=("Century Gothic", 20, "italic"))
        self.label0.place(relx=0.1, rely=0.1, anchor=tkinter.CENTER)

        self.entry0 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
        self.entry0.configure(width=110, height=30, font=("Century Gothic", 15), corner_radius=10)
        self.entry0.place(relx=0.24, rely=0.1, anchor=tkinter.CENTER)

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Name: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.1, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Name")
        self.__style_input_box(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.label2 = ctk.CTkLabel(master=self.right_frame, text="Date of birth: ", font=("Century Gothic", 20, "italic"))
        self.label2.place(relx=0.145, rely=0.275, anchor=tkinter.CENTER)

        self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="YYYY-MM-DD")
        self.__style_input_box(self.entry2)
        self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

        self.label3 = ctk.CTkLabel(master=self.right_frame, text="ID: ", font=("Century Gothic", 20, "italic"))
        self.label3.place(relx=0.0715, rely=0.4, anchor=tkinter.CENTER)

        self.entry3 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
        self.__style_input_box(self.entry3)
        self.entry3.place(relx=0.325, rely=0.445, anchor=tkinter.CENTER)

        self.label4 = ctk.CTkLabel(master=self.right_frame, text="Phone Number: ", font=("Century Gothic", 20, "italic"))
        self.label4.place(relx=0.155, rely=0.525, anchor=tkinter.CENTER)

        self.entry4 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Phone Number")
        self.__style_input_box(self.entry4)
        self.entry4.place(relx=0.325, rely=0.57, anchor=tkinter.CENTER)

        self.label5 = ctk.CTkLabel(master=self.right_frame, text="Email: ", font=("Century Gothic", 20, "italic"))
        self.label5.place(relx=0.09, rely=0.65, anchor=tkinter.CENTER)

        self.entry5 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Email")
        self.__style_input_box(self.entry5)
        self.entry5.place(relx=0.325, rely=0.695, anchor=tkinter.CENTER)

        self.label6 = ctk.CTkLabel(master=self.right_frame, text="Password: ", font=("Century Gothic", 20, "italic"))
        self.label6.place(relx=0.125, rely=0.775, anchor=tkinter.CENTER)

        self.entry6 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Password", show="*")
        self.__style_input_box(self.entry6)
        self.entry6.place(relx=0.325, rely=0.82, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="Confirm", command=(lambda: update_successfully(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        def update_successfully(self):
            name = self.entry1.get()
            dob = self.entry2.get()
            id = self.entry3.get()
            phone = self.entry4.get()
            email = self.entry5.get()
            password = self.entry6.get()
            if name == "" or dob == "" or id == "" or phone == "" or email == "":
                msgbox.showerror("Error", "Please fill in all the fields")
            if not name.isalpha():
                msgbox.showerror("Error", "Please enter a valid name")
            if not phone.isdigit() and len(phone) != 10:
                msgbox.showerror("Error", "Please enter a valid phone number")
                return
            if "@" not in email:
                msgbox.showerror("Error", "Please enter a valid email")
                return
            if "-" not in dob:
                msgbox.showerror("Error", "Please enter a valid date of birth")
                return
            try:
                # fmt:off
                (the_company
                    .get_empl_by_id(id)
                    .unwrap()
                    .set_name(name)
                    .unwrap()
                    .set_dob(dob)
                    .unwrap()
                    .set_phone(phone)
                    .unwrap()
                    .set_email(email)
                    .unwrap()
                    .set_password(password)
                    .unwrap()
                ) 
                # fmt:on
                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one({"_id": the_company.get_empl_by_id(id).unwrap().id}, {"$set": the_company.get_empl_by_id(id).unwrap().dict(exclude={"id"}, by_alias=True)}, upsert=True)

                msgbox.showinfo("Success", "Employee updated successfully")
            except ValueError as e:
                msgbox.showerror("Error", str(e))

    def __admin_view_employee(self):
        self.button2_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button2_frame, text="View Employee", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Employee ID: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.145, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
        self.__style_input_box(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="View", fg_color="purple", command=(lambda: view_employee(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10)
        self.button.place(relx=0.5, rely=0.295, anchor=tkinter.CENTER)

        self.button2_frame.pack(pady=20)

        def view_employee(self):
            id = self.entry1.get()
            if id == "":
                msgbox.showerror("Error", "Please enter a valid ID")
            else:
                msgbox.showinfo("Success", "Employee found")

    def __admin_list_all_employees(self):
        self.button3_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.right_frame, text="Select options to list employees", font=("Century Gothic", 20, "bold"))
        self.label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkComboBox(
            master=self.right_frame, values=["All", "Name", "ID", "Phone Number", "Email"], command=lambda self=self: choice_selected(self)
        )
        self.__style_input_box(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="View", fg_color="purple", command=lambda self=self: choice_selected(self))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10)
        self.button.place(relx=0.5, rely=0.295, anchor=tkinter.CENTER)

        def choice_selected(self):
            choice = self.entry1.get()
            if choice not in ["All", "Name", "ID", "Phone Number", "Email"]:
                msgbox.showerror("Error", "Please select a valid option")

        self.button3_frame.pack(pady=20)

    def __admin_change_password(self):
        self.button4_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button4_frame, text="Change Password", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Old Password: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.15, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Old Password", show="*")
        self.__style_input_box(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.label2 = ctk.CTkLabel(master=self.right_frame, text="New Password: ", font=("Century Gothic", 20, "italic"))
        self.label2.place(relx=0.15, rely=0.275, anchor=tkinter.CENTER)

        self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter New Password", show="*")
        self.__style_input_box(self.entry2)
        self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

        self.label3 = ctk.CTkLabel(master=self.right_frame, text="Confirm Password: ", font=("Century Gothic", 20, "italic"))
        self.label3.place(relx=0.175, rely=0.4, anchor=tkinter.CENTER)

        self.entry3 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Confirm New Password", show="*")
        self.__style_input_box(self.entry3)
        self.entry3.place(relx=0.325, rely=0.445, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="Change", fg_color="purple", command=lambda: change_password_successfully(self))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10)
        self.button.place(relx=0.5, rely=0.545, anchor=tkinter.CENTER)

        def change_password_successfully(self):
            employee = the_company.logged_in_employee

            old_password = self.entry1.get()
            new_password = self.entry2.get()
            confirm_password = self.entry3.get()

            if old_password == "" or new_password == "" or confirm_password == "":
                msgbox.showerror("Error", "Please enter a valid password")
                return
            if new_password != confirm_password:
                msgbox.showerror("Error", "New password and confirm password do not match")
                return

            if hash(employee.name, old_password) != employee.hashed_password:
                msgbox.showerror("Error", "Incorrect current password")
                return

            employee.hashed_password = hash(employee.name, new_password)
            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.update_one({"_id": employee.id}, {"$set": employee.dict(include={"hashed_password"})}, upsert=True)

            msgbox.showinfo("Success", "Password changed successfully")

    # endregion

    # region: employee functions

    def __employee_view_employee(self):
        self.button2_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button2_frame, text="View Employee", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Employee ID: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.145, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
        self.__style_input_box(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="View", fg_color="purple", command=(lambda: view_employee(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10)
        self.button.place(relx=0.5, rely=0.295, anchor=tkinter.CENTER)

        self.button2_frame.pack(pady=20)

        def view_employee(self):
            id = self.entry1.get()
            if id == "":
                msgbox.showerror("Error", "Please enter a valid ID")
            else:
                msgbox.showinfo("Success", "Employee found")

    def __employee_change_password(self):
        self.button4_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button4_frame, text="Change Password", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Old Password: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.15, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Old Password", show="*")
        self.__style_input_box(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.label2 = ctk.CTkLabel(master=self.right_frame, text="New Password: ", font=("Century Gothic", 20, "italic"))
        self.label2.place(relx=0.15, rely=0.275, anchor=tkinter.CENTER)

        self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter New Password", show="*")
        self.__style_input_box(self.entry2)
        self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

        self.label3 = ctk.CTkLabel(master=self.right_frame, text="Confirm Password: ", font=("Century Gothic", 20, "italic"))
        self.label3.place(relx=0.175, rely=0.4, anchor=tkinter.CENTER)

        self.entry3 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Confirm New Password", show="*")
        self.__style_input_box(self.entry3)
        self.entry3.place(relx=0.325, rely=0.445, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(
            master=self.right_frame,
            text="Change",
            fg_color="purple",
            # command=(lambda: change_password_successfully(self)),
            command=lambda self=self: change_password_successfully(self),
        )
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10)
        self.button.place(relx=0.5, rely=0.545, anchor=tkinter.CENTER)

        def change_password_successfully(self):
            employee = the_company.logged_in_employee

            old_password = self.entry1.get()
            new_password = self.entry2.get()
            confirm_password = self.entry3.get()

            if old_password == "" or new_password == "" or confirm_password == "":
                msgbox.showerror("Error", "Please enter a valid password")
                return
            if new_password != confirm_password:
                msgbox.showerror("Error", "New password and confirm password do not match")
                return

            if hash(employee.employee_id, old_password) != employee.hashed_password:
                msgbox.showerror("Error", "Incorrect current password")
                return

            employee.hashed_password = hash(employee.employee_id, new_password)
            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.update_one({"_id": employee.id}, {"$set": employee.dict(include={"hashed_password"})}, upsert=True)

            msgbox.showinfo("Success", "Password changed successfully")

    # endregion
