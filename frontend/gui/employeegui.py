import os
import tkinter
import customtkinter as ctk
from tkinter import messagebox as msgbox

from models import Company, Employee, hash
from database.mongo import employee_repo
from frontend.helpers_gui import *
from frontend.helpers_gui.global_styling import *

the_company = Company()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

Width = 1024
Height = 768


class EmployeeGui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Employee Management")
        self.geometry(f"{Width}x{Height}")
        self.resizable(True, True)

        self.left_frame = ctk.CTkFrame(master=self, corner_radius=10)
        self.left_frame.pack(side=ctk.LEFT)
        self.left_frame.pack_propagate(False)
        self.left_frame.configure(width=320, height=760)

        self.right_frame = ctk.CTkFrame(master=self)
        self.right_frame.pack(side=ctk.RIGHT, expand=True)
        self.right_frame.pack_propagate(False)

        self.admin() if the_company.logged_in_employee.is_admin else self.employee()

    def admin(self):
        menu_buttons = MenuButtons(
            self.left_frame,
            self.right_frame,
            {
                "Add Employee": self.__admin_add_employee,
                "Remove Employee": self.__admin_remove_employee,
                "Update Employee": self.__admin_update_employee,
                "View Employee": self.__admin_view_employee,
                "Change Password": self.__change_password,
                "Back": self.__back_to_homepage,
            },
        )
        menu_buttons.create()

    def employee(self):
        menu_buttons = MenuButtons(
            self.left_frame,
            self.right_frame,
            {
                "View Employee": self.__employee_view_employee,
                "Change Password": self.__change_password,
                "Back": self.__back_to_homepage,
            },
        )
        menu_buttons.create()

    def __back_to_homepage(self):
        from .homepage import Homepage

        self.destroy()
        Homepage().mainloop()

    # region: admin functions

    def __admin_add_employee(self):
        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        ctk.CTkLabel(master=main_frame, text="Add Employee", **label_title_style).grid(
            row=0, column=0, columnspan=2, pady=(20, 0)
        )

        ctk.CTkLabel(master=main_frame, text="Name: ", **label_desc_style).grid(row=1, column=0, pady=(20, 0))
        name_entry = ctk.CTkEntry(master=main_frame, placeholder_text="Enter name", **input_box_style)
        name_entry.grid(row=1, column=1, pady=(20, 0))

        ctk.CTkLabel(master=main_frame, text="Date of birth: ", **label_desc_style).grid(row=2, column=0, pady=(20, 0))
        dob_entry = ctk.CTkEntry(master=main_frame, placeholder_text="Enter date of birth", **input_box_style)
        dob_entry.grid(row=2, column=1, pady=(20, 0))

        ctk.CTkLabel(master=main_frame, text="ID: ", **label_desc_style).grid(row=3, column=0, pady=(20, 0))
        id_entry = ctk.CTkEntry(master=main_frame, placeholder_text="Enter ID", **input_box_style)
        id_entry.grid(row=3, column=1, pady=(20, 0))

        ctk.CTkLabel(master=main_frame, text="Phone Number: ", **label_desc_style).grid(row=4, column=0, pady=(20, 0))
        phone_entry = ctk.CTkEntry(master=main_frame, placeholder_text="Enter phone number", **input_box_style)
        phone_entry.grid(row=4, column=1, pady=(20, 0))

        ctk.CTkLabel(master=main_frame, text="Email: ", **label_desc_style).grid(row=5, column=0, pady=(20, 0))
        email_entry = ctk.CTkEntry(master=main_frame, placeholder_text="Enter email", **input_box_style)
        email_entry.grid(row=5, column=1, pady=(20, 0))

        ctk.CTkLabel(master=main_frame, text="Password: ", **label_desc_style).grid(row=6, column=0, pady=(20, 0))
        password_entry = ctk.CTkEntry(master=main_frame, placeholder_text="Enter password", **input_box_style)
        password_entry.grid(row=6, column=1, pady=(20, 0))

            name = name_entry.get()
            dob = dob_entry.get()
            empl_id = id_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            employee = Employee()
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
        def _add_handler():

                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.insert_one(employee.dict(by_alias=True))
                msgbox.showinfo("Success", "Employee added successfully")

        ctk.CTkButton(master=main_frame, text="Add", command=_add_handler, **btn_action_style).grid(
            row=7, column=0, columnspan=2, pady=(20, 0)
        )

    def __admin_remove_employee(self):
        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        ctk.CTkLabel(master=main_frame, text="Remove Employee", **label_title_style).grid(
            row=0, column=0, columnspan=2, pady=(20, 0)
        )

        # Select employee from a list
        radio_empl_idx_select: ctk.Variable = ctk.IntVar(value=0)
        empl_items = tuple(f"{empl.employee_id} - {empl.name}" for empl in the_company.employees)
        _display_list = display_list(
            _master=main_frame, options=empl_items, returned_idx=[radio_empl_idx_select], selectable=True
        )
        if _display_list[0] is False:
            ctk.CTkLabel(master=main_frame, text="No employee found", **label_desc_style).grid(
                row=1, column=0, columnspan=2, pady=20, padx=20
            )

        def _remove_handler():
            if msgbox.askyesno("Confirmation", "Are you sure you want to remove this employee?"):
                the_company.employees.pop(radio_empl_idx_select.get())

                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.delete_one({"employee_id": the_company.employees[radio_empl_idx_select.get()].employee_id})
                msgbox.showinfo("Success", "Employee removed successfully")

        ctk.CTkButton(master=main_frame, text="Remove", command=_remove_handler, **btn_action_style).grid(
            row=2, column=0, columnspan=2, pady=(20, 0)
        )

    def __admin_update_employee(self):
        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        ctk.CTkLabel(master=main_frame, text="Update Employee", **label_title_style).grid(
            row=0, column=0, columnspan=2, pady=(20, 0)
        )

        # Select employee from a list
        radio_empl_idx_select: ctk.Variable = ctk.IntVar(value=0)
        empl_items = tuple(f"{empl.employee_id} - {empl.name}" for empl in the_company.employees)
        _display_list = display_list(
            _master=main_frame, options=empl_items, returned_idx=[radio_empl_idx_select], selectable=True
        )
        if _display_list[0] is False:
            ctk.CTkLabel(master=main_frame, text="No employee found", **label_desc_style).grid(
                row=1, column=0, columnspan=2, pady=20, padx=20
            )

        ctk.CTkLabel(master=main_frame, text="Name: ", **label_desc_style).grid(row=2, column=0, pady=(20, 0))
        name_entry = ctk.CTkEntry(master=main_frame, placeholder_text="Enter name", **input_box_style)
        name_entry.grid(row=2, column=1, pady=(20, 0))

        ctk.CTkLabel(master=main_frame, text="Date of Birth: ", **label_desc_style).grid(row=3, column=0, pady=(20, 0))
        dob_entry = ctk.CTkEntry(master=main_frame, placeholder_text="Enter date of birth", **input_box_style)
        dob_entry.grid(row=3, column=1, pady=(20, 0))

        ctk.CTkLabel(master=main_frame, text="ID: ", **label_desc_style).grid(row=4, column=0, pady=(20, 0))
        id_entry = ctk.CTkEntry(master=main_frame, placeholder_text="Enter ID", **input_box_style)
        id_entry.grid(row=4, column=1, pady=(20, 0))

        ctk.CTkLabel(master=main_frame, text="Phone Number: ", **label_desc_style).grid(row=5, column=0, pady=(20, 0))
        phone_entry = ctk.CTkEntry(master=main_frame, placeholder_text="Enter phone number", **input_box_style)
        phone_entry.grid(row=5, column=1, pady=(20, 0))

        ctk.CTkLabel(master=main_frame, text="Email: ", **label_desc_style).grid(row=6, column=0, pady=(20, 0))
        email_entry = ctk.CTkEntry(master=main_frame, placeholder_text="Enter email", **input_box_style)
        email_entry.grid(row=6, column=1, pady=(20, 0))

        ctk.CTkLabel(master=main_frame, text="Password: ", **label_desc_style).grid(row=7, column=0, pady=(20, 0))
        password_entry = ctk.CTkEntry(master=main_frame, placeholder_text="Enter password", **input_box_style)
        password_entry.grid(row=7, column=1, pady=(20, 0))

            if msgbox.askyesno("Confirmation", "Are you sure you want to update this employee?"):
                the_company.employees[radio_empl_idx_select.get()].name = name_entry.get()
                the_company.employees[radio_empl_idx_select.get()].date_of_birth = dob_entry.get()
                the_company.employees[radio_empl_idx_select.get()].employee_id = id_entry.get()
                the_company.employees[radio_empl_idx_select.get()].phone_number = phone_entry.get()
                the_company.employees[radio_empl_idx_select.get()].email = email_entry.get()
                the_company.employees[radio_empl_idx_select.get()].password = password_entry.get()

                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one(
                        {"employee_id": the_company.employees[radio_empl_idx_select.get()].employee_id},
                        {
                            "$set": {
                                "name": the_company.employees[radio_empl_idx_select.get()].name,
                                "date_of_birth": the_company.employees[radio_empl_idx_select.get()].dob,
                                "employee_id": the_company.employees[radio_empl_idx_select.get()].employee_id,
                                "phone_number": the_company.employees[radio_empl_idx_select.get()].phone,
                                "email": the_company.employees[radio_empl_idx_select.get()].email,
                                "password": the_company.employees[radio_empl_idx_select.get()].hashed_password,
                            }
                        },
                    )
                msgbox.showinfo("Success", "Employee updated successfully")
        def _update_handler():

        ctk.CTkButton(master=main_frame, text="Update", command=_update_handler, **btn_action_style).grid(
            row=8, column=0, columnspan=2, pady=(20, 0)
        )

    def __admin_view_employee(self):
        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        ctk.CTkLabel(master=main_frame, text="View Employee", **label_title_style).grid(
            row=0, column=0, columnspan=2, pady=(20, 0)
        )

        # Select employee from a list
        radio_empl_idx_select: ctk.Variable = ctk.IntVar(value=0)
        empl_items = tuple(f"{empl.employee_id} - {empl.name}" for empl in the_company.employees)
        _display_list = display_list(
            _master=main_frame, options=empl_items, returned_idx=[radio_empl_idx_select], selectable=True
        )
        if _display_list[0] is False:
            ctk.CTkLabel(master=main_frame, text="No employee found", **label_desc_style).grid(
                row=1, column=0, columnspan=2, pady=20, padx=20
            )

        def _display_employee_handler():
            _empl = the_company.employees[radio_empl_idx_select.get()]
            _empl_info = (
                f"Name: {_empl.name}\n"
                f"Date of Birth: {_empl.dob}\n"
                f"ID: {_empl.employee_id}\n"
                f"Phone Number: {_empl.phone}\n"
                f"Email: {_empl.email}\n"
                f"Password: {_empl.hashed_password}\n"
            )
            ctk.CTkLabel(master=main_frame, text=_empl_info, **label_desc_style).grid(
                row=2, column=0, columnspan=2, pady=20, padx=20
            )

        ctk.CTkButton(master=main_frame, text="View", command=_display_employee_handler, **btn_action_style).grid(
            row=3, column=0, columnspan=2, pady=(20, 0)
        )

    # endregion

    # region: employee functions

    def __employee_view_employee(self):
        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        ctk.CTkLabel(master=main_frame, text="View Employee", **label_title_style).grid(
            row=0, column=0, columnspan=2, pady=(20, 0)
        )

        def _display_employee_handler():
            _empl = the_company.logged_in_employee
            _empl_info = (
                f"Name: {_empl.name}\n"
                f"Date of Birth: {_empl.dob}\n"
                f"ID: {_empl.employee_id}\n"
                f"Phone Number: {_empl.phone}\n"
                f"Email: {_empl.email}\n"
                f"Password: {_empl.hashed_password}\n"
            )
            ctk.CTkLabel(master=main_frame, text=_empl_info, **label_desc_style).grid(
                row=2, column=0, columnspan=2, pady=20, padx=20
            )

        ctk.CTkButton(master=main_frame, text="View", command=_display_employee_handler, **btn_action_style).grid(
            row=3, column=0, columnspan=2, pady=(20, 0)
        )

    # endregion

    def __change_password(self):
        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        ctk.CTkLabel(master=main_frame, text="Change Password", **label_title_style).grid(
            row=0, column=0, columnspan=2, pady=(20, 0)
        )

        ctk.CTkLabel(master=main_frame, text="Old Password: ", **label_desc_style).grid(row=1, column=0, pady=(20, 0))
        old_password_entry = ctk.CTkEntry(master=main_frame, placeholder_text="Enter old password", **input_box_style)
        old_password_entry.grid(row=1, column=1, pady=(20, 0))

        ctk.CTkLabel(master=main_frame, text="New Password: ", **label_desc_style).grid(row=2, column=0, pady=(20, 0))
        new_password_entry = ctk.CTkEntry(master=main_frame, placeholder_text="Enter new password", **input_box_style)
        new_password_entry.grid(row=2, column=1, pady=(20, 0))

        ctk.CTkLabel(master=main_frame, text="Confirm Password: ", **label_desc_style).grid(row=3, column=0, pady=(20, 0))
        confirm_password_entry = ctk.CTkEntry(
            master=main_frame, placeholder_text="Enter confirm password", **input_box_style
        )
        confirm_password_entry.grid(row=3, column=1, pady=(20, 0))

        def _change_password_handler():
            logged_in_employee = the_company.logged_in_employee
            if old_password_entry.get() != the_company.logged_in_employee.hashed_password:
                msgbox.showerror("Error", "Old password is incorrect")
            elif new_password_entry.get() != confirm_password_entry.get():
                msgbox.showerror("Error", "New password and confirm password do not match")
            else:
                the_company.logged_in_employee.hashed_password = new_password_entry.get()
                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one(
                        {"_id": logged_in_employee.employee_id},
                        {"$set": logged_in_employee.dict(include={"hashed_password"})},
                        upsert=True,
                    )

                msgbox.showinfo("Success", "Password changed successfully")

        ctk.CTkButton(master=main_frame, text="Change", command=_change_password_handler, **btn_action_style).grid(
            row=4, column=0, columnspan=2, pady=(20, 0)
        )
