import os
import customtkinter as ctk
from tkinter import messagebox as msgbox

from models import Company, Employee, hash
from database.mongo import employee_repo, department_repo, benefit_repo
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

        menu_buttons = MenuButtons(
            self.left_frame, self.right_frame, self.admin() if the_company.logged_in_employee.is_admin else self.employee()
        )
        menu_buttons.create()

    def admin(self):
        return {
            "Add Employee": self.__admin_add_employee,
            "Remove Employee": self.__admin_remove_employee,
            "Update Employee": self.__admin_update_employee,
            "View Employee": self.__admin_view_employee,
            "Change Password": self.__change_password,
            "Back": self.__back_to_homepage,
        }

    def employee(self):
        return {
            "View Employee": self.__employee_view_employee,
            "Change Password": self.__change_password,
            "Back": self.__back_to_homepage,
        }

    def __clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()
    def __back_to_homepage(self):
        from .homepage import Homepage

        self.destroy()
        Homepage().mainloop()

    # region: admin functions

    def __admin_add_employee(self):
        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        entries = [ctk.CTkEntry(master=main_frame) for _ in range(6)]
        labels = ("Name: ", "Date of birth: ", "ID: ", "Phone Number: ", "Email: ", "Password: ")
        placeholders = ("Alex", "2000-12-31", "1234ABC", "0123456789", "hello@wo.rld", "secure")
        for row, entry, label, placeholder in zip(range(1, 7), entries, labels, placeholders):
            ctk.CTkLabel(master=main_frame, text=label, **label_desc_style).grid(
                row=row, column=0, pady=(20, 0), padx=20, sticky="w"
            )
            entry.configure(placeholder_text=placeholder, **input_box_style)
            entry.grid(row=row, column=1, pady=(20, 0), padx=(0, 20))

        def _add_handler():
            nonlocal entries
            values = [entry.get() for entry in entries]
            print("DEBUG", *values)

            for value in values:
                if not value:
                    msgbox.showerror("Error", "Please fill in all the fields")
                    return

            _empl = Employee()
            for setter, value in zip(
                (_empl.set_name, _empl.set_dob, _empl.set_id, _empl.set_phone, _empl.set_email, _empl.set_password), values
            ):
                setter(value).unwrap()

            the_company.employees.append(_empl)

            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.insert_one(_empl.dict(by_alias=True))
            msgbox.showinfo("Success", "Employee added successfully")

        ctk.CTkButton(master=main_frame, text="Add", command=_add_handler, **btn_action_style).grid(
            row=7, column=0, columnspan=2, pady=20
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
            if not msgbox.askyesno("Confirmation", "Are you sure you want to remove this employee?"):
                return
            _empls = the_company.employees
            _empl = _empls[radio_empl_idx_select.get()]

            _db_update_bnfs, _db_update_dept = [], []
            # remove employee from benefits
            for b in the_company.benefits:
                if _empl in b.enrolled_employees:
                    b.enrolled_employees.remove(_empl)
                    _db_update_bnfs.append(b)
                if _empl in b.pending_requests:
                    b.pending_requests.remove(_empl)
                    _db_update_bnfs.append(b)

            # remove employee from departments
            for d in the_company.departments:
                if _empl in d.members:
                    d.members.remove(_empl)
                    _db_update_dept.append(d)

            # remove employee from company
            _empls.remove(_empl)

            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.delete_one({"_id": _empl.id})
                for b in _db_update_bnfs:
                    benefit_repo.update_one(
                        {"_id": b.id}, {"$set": b.dict(include={"enrolled_employees", "pending_requests"})}, upsert=True
                    )
                for d in _db_update_dept:
                    department_repo.update_one({"_id": d.id}, {"$set": d.dict(include={"members"})}, upsert=True)

            msgbox.showinfo("Success", "Employee removed successfully")

        ctk.CTkButton(master=main_frame, text="Remove", command=_remove_handler, **btn_action_style).grid(
            row=2, column=0, columnspan=2, pady=(10, 20)
        )

    def __admin_update_employee(self):
        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        ctk.CTkLabel(master=main_frame, text="Update Employee", **label_title_style).grid(
            row=0, column=0, columnspan=2, pady=20
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
        _display_list[1].grid(row=1, column=0, columnspan=2, pady=0, padx=20)

        entries = [ctk.CTkEntry(master=main_frame) for _ in range(6)]
        labels = ("Name: ", "Date of birth: ", "ID: ", "Phone Number: ", "Email: ", "Password: ")
        placeholder = ("Alex", "2000-12-31", "1234ABC", "0123456789", "hello@wo.rld", "secure")

        for row, label, entry, placeholder in zip(range(2, 8), labels, entries, placeholder):
            ctk.CTkLabel(master=main_frame, text=label, **label_desc_style).grid(
                row=row, column=0, padx=(20, 0), pady=(20, 0), sticky="w"
            )
            entry.configure(placeholder_text=placeholder, **input_box_style)
            entry.grid(row=row, column=1, padx=20, pady=(20, 0))

        def _update_handler():
            nonlocal entries
            values = [entry.get() for entry in entries]
            if not msgbox.askyesno("Confirmation", "Are you sure you want to update this employee?"):
                return
            _empl = the_company.employees[radio_empl_idx_select.get()]

            for setter, value in zip(
                (_empl.set_name, _empl.set_dob, _empl.set_id, _empl.set_phone, _empl.set_email, _empl.set_password), values
            ):
                setter(value).unwrap() if value else None

            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.update_one({"_id": _empl.id}, {"$set": _empl.dict(exclude={"id"}, by_alias=True)}, upsert=True)
            msgbox.showinfo("Success", "Employee updated successfully")

        ctk.CTkButton(master=main_frame, text="Update", command=_update_handler, **btn_action_style).grid(
            row=8, column=0, columnspan=2, pady=20
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
            )
            ctk.CTkLabel(master=main_frame, text=_empl_info, **label_desc_style).grid(
                row=2, column=0, columnspan=2, pady=20, padx=20
            )

        ctk.CTkButton(master=main_frame, text="View", command=_display_employee_handler, **btn_action_style).grid(
            row=3, column=0, columnspan=2, pady=(10, 20)
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
            row=0, column=0, columnspan=2, pady=(20, 0), padx=20
        )

        old_pwd_entry, new_pwd_entry, confirm_pwd_entry = (ctk.CTkEntry(None),) * 3
        for row, entry, label, placeholder in zip(
            range(1, 4),
            (old_pwd_entry, new_pwd_entry, confirm_pwd_entry),
            ("Old: ", "New: ", "Confirm: "),
            ("secure", "newpass", "newpass"),
        ):
            ctk.CTkLabel(master=main_frame, text=label, **label_desc_style).grid(
                row=row, column=0, pady=(20, 0), sticky="w", padx=20
            )
            entry = ctk.CTkEntry(master=main_frame, placeholder_text=placeholder, **input_box_style)
            entry.grid(row=row, column=1, pady=(20, 0), padx=(0, 20))

        def _change_password_handler():
            nonlocal old_pwd_entry, new_pwd_entry, confirm_pwd_entry
            old_pwd, new_pwd, confirm_pwd = (old_pwd_entry.get(), new_pwd_entry.get(), confirm_pwd_entry.get())
            logged_in_employee = the_company.logged_in_employee
            if hash(the_company.logged_in_employee.name, old_pwd) != the_company.logged_in_employee.hashed_password:
                msgbox.showerror("Error", "Old password is incorrect")
            elif new_pwd != confirm_pwd:
                msgbox.showerror("Error", "New password and confirm password do not match")
            else:
                logged_in_employee.set_password(new_pwd).unwrap()
                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one(
                        {"_id": logged_in_employee.employee_id},
                        {"$set": logged_in_employee.dict(include={"hashed_password"})},
                        upsert=True,
                    )

                msgbox.showinfo("Success", "Password changed successfully")

        ctk.CTkButton(master=main_frame, text="Change", command=_change_password_handler, **btn_action_style).grid(
            row=4, column=0, columnspan=2, pady=20
        )
