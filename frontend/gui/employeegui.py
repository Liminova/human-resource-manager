import os
from tkinter import E, W
from tkinter import messagebox as msgbox

import customtkinter as ctk

from database.mongo import benefit_repo, department_repo, employee_repo
from frontend.helpers_gui import *
from frontend.helpers_gui.global_styling import *
from models import Company, Employee, hash

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
        # - 2 columns
        # 0: label + input name
        # 1:               dob
        # 2:               id
        # 3:               phone
        # 4:               email
        # 5:               password
        # 6: add button

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

            for value in values:
                if not value:
                    msgbox.showerror("Error", "Please fill in all the fields")
                    return

            new_empl = Employee()
            for setter, value in zip(
                (
                    new_empl.set_name,
                    new_empl.set_dob,
                    new_empl.set_id,
                    new_empl.set_phone,
                    new_empl.set_email,
                    new_empl.set_password,
                ),
                values,
            ):
                setter(value).unwrap()

            the_company.employees.append(new_empl)

            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.insert_one(new_empl.dict(by_alias=True))
            msgbox.showinfo("Success", "Employee added successfully")

        ctk.CTkButton(master=main_frame, text="Add", command=_add_handler, **btn_action_style).grid(
            row=7, column=0, columnspan=2, pady=20
        )

    def __admin_remove_employee(self):
        # - 1 column
        # 0: select employee from a list
        # 1: remove button

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        # Select employee from a list
        empl_idx_select: ctk.Variable = ctk.IntVar(value=0)
        display_list(
            _master=main_frame,
            options=tuple(f"{empl.employee_id} - {empl.name}" for empl in the_company.employees),
            returned_idx=[empl_idx_select],
            err_msg="No employee to remove",
            place=(0, 0),
        )

        def _remove_handler():
            nonlocal empl_idx_select
            if not msgbox.askyesno("Confirmation", "Are you sure you want to remove this employee?"):
                return
            empls = the_company.employees
            selected_empl = empls[empl_idx_select.get()]

            updated_bnfs, updated_depts = [], []
            # remove employee from benefits
            for bnf in the_company.benefits:
                if selected_empl in bnf.enrolled_employees:
                    bnf.enrolled_employees.remove(selected_empl)
                    updated_bnfs.append(bnf)
                if selected_empl in bnf.pending_requests:
                    bnf.pending_requests.remove(selected_empl)
                    updated_bnfs.append(bnf)

            # remove employee from departments
            for dept in the_company.departments:
                if selected_empl in dept.members:
                    dept.members.remove(selected_empl)
                    updated_depts.append(dept)

            # remove employee from company
            empls.remove(selected_empl)

            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.delete_one({"_id": selected_empl.id})
                for bnf in updated_bnfs:
                    benefit_repo.update_one(
                        {"_id": bnf.id}, {"$set": bnf.dict(include={"enrolled_employees", "pending_requests"})}, upsert=True
                    )
                for dept in updated_depts:
                    department_repo.update_one({"_id": dept.id}, {"$set": dept.dict(include={"members"})}, upsert=True)

            msgbox.showinfo("Success", "Employee removed successfully")
            merge_callable(self.__clear_right_frame, self.__admin_remove_employee)()

        ctk.CTkButton(master=main_frame, text="Remove", command=_remove_handler, **btn_action_style).grid(
            row=1, column=0, columnspan=2, pady=(0, 20)
        )

    def __admin_update_employee(self):
        # - 2 columns
        # 0: select employee from a list
        # 1: label + input name
        # 2:               dob
        # 3:               id
        # 4:               phone
        # 5:               email
        # 6:               password
        # 7: update button

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        # Select employee from a list
        empl_idx_select: ctk.Variable = ctk.IntVar(value=0)
        display_list(
            _master=main_frame,
            options=tuple(f"{empl.employee_id} - {empl.name}" for empl in the_company.employees),
            err_msg="No employee found",
            returned_idx=[empl_idx_select],
            place=(0, 0),
            colspan=2,
            pady=(20, 0),
        )

        entries = [ctk.CTkEntry(master=main_frame) for _ in range(6)]
        labels = ("Name: ", "Date of birth: ", "ID: ", "Phone Number: ", "Email: ", "Password: ")
        placeholder = ("Alex", "2000-12-31", "1234ABC", "0123456789", "hello@wo.rld", "secure")
        for row, label, entry, placeholder in zip(range(1, 7), labels, entries, placeholder):
            ctk.CTkLabel(master=main_frame, text=label, **label_desc_style).grid(
                row=row, column=0, padx=(20, 0), pady=(20, 0), sticky="w"
            )
            entry.configure(placeholder_text=placeholder, **input_box_style)
            entry.grid(row=row, column=1, padx=20, pady=(20, 0))

        def _update_handler():
            nonlocal entries
            values = [entry.get().strip() for entry in entries]
            if not msgbox.askyesno("Confirmation", "Are you sure you want to update this employee?"):
                return
            selected_empl = the_company.employees[empl_idx_select.get()]
            for setter, value in zip(
                (
                    selected_empl.set_name,
                    selected_empl.set_dob,
                    selected_empl.set_id,
                    selected_empl.set_phone,
                    selected_empl.set_email,
                    selected_empl.set_password,
                ),
                values,
            ):
                setter(value).unwrap() if value else None

            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.update_one(
                    {"_id": selected_empl.id},
                    {"$set": selected_empl.dict(include={"name", "dob", "employee_id", "phone", "email", "password"})},
                    upsert=True,
                )
            msgbox.showinfo("Success", "Employee updated successfully")
            merge_callable(self.__clear_right_frame, self.__admin_update_employee)()

        ctk.CTkButton(master=main_frame, text="Update", command=_update_handler, **btn_action_style).grid(
            row=7, column=0, columnspan=2, pady=20
        )

    def __admin_view_employee(self):
        # - 2 columns
        # 0: select employee from a list
        # 1: info frame

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        empl_info_frame = ctk.CTkBaseClass(None)
        empl_idx_select: ctk.Variable = ctk.IntVar(value=0)

        def update_empl_info_frame():
            nonlocal empl_info_frame, empl_idx_select
            selected_empl = the_company.employees[empl_idx_select.get()]
            labels = ("Name: ", "Date of birth: ", "ID: ", "Phone Number: ", "Email: ")
            values = (
                selected_empl.name,
                selected_empl.dob,
                selected_empl.employee_id,
                selected_empl.phone,
                selected_empl.email,
            )
            empl_info_frame.destroy()
            empl_info_frame = ctk.CTkFrame(master=main_frame)
            empl_info_frame.grid(row=1, column=0, pady=(0, 20), padx=20)
            for row, label, value in zip(range(1, 6), labels, values):
                pady = (20, 0) if row == 1 else (0, 20) if row == len(labels) - 1 else 0
                ctk.CTkLabel(master=empl_info_frame, text=label).grid(row=row, column=0, padx=(20, 0), pady=pady, sticky=W)
                ctk.CTkLabel(master=empl_info_frame, text=value).grid(row=row, column=1, padx=20, pady=pady, sticky=E)

        update_empl_info_frame()

        display_list(
            _master=main_frame,
            options=tuple(f"{empl.employee_id} - {empl.name}" for empl in the_company.employees),
            returned_idx=[empl_idx_select],
            cmd=update_empl_info_frame,
            place=(0, 0),
            colspan=2,
            err_msg="No employee found",
        )

    # endregion

    # region: employee functions

    def __employee_view_employee(self):
        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)
        empl = the_company.logged_in_employee

        labels = ("Name: ", "Date of birth: ", "ID: ", "Phone Number: ", "Email: ")
        values = (empl.name, empl.dob, empl.employee_id, empl.phone, empl.email)
        for row, label, value in zip(range(0, 5), labels, values):
            pady = (20, 0) if row == 0 else (0, 20) if row == len(labels) - 1 else 0
            ctk.CTkLabel(master=main_frame, text=label).grid(row=row, column=0, padx=(20, 0), pady=pady, sticky=W)
            ctk.CTkLabel(master=main_frame, text=value).grid(row=row, column=1, padx=20, pady=pady, sticky=E)

    # endregion

    def __change_password(self):
        # - 2 columns
        # 0: label + input old password
        # 1:               new password
        # 2:               confirm password
        # 3: change button

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        entries = [ctk.CTkEntry(master=main_frame) for _ in range(3)]
        for row, entry, label, placeholder in zip(
            range(0, 3), entries, ("Old: ", "New: ", "Confirm: "), ("secure", "newpass", "newpass")
        ):
            ctk.CTkLabel(master=main_frame, text=label, **label_desc_style).grid(
                row=row, column=0, pady=(20, 0), sticky="w", padx=20
            )
            entry.configure(placeholder_text=placeholder, **input_box_style)
            entry.grid(row=row, column=1, pady=(20, 0), padx=(0, 20))

        def _change_password_handler():
            nonlocal entries
            old_pwd, new_pwd, confirm_pwd = (entry.get() for entry in entries)
            logged_in_employee = the_company.logged_in_employee

            if hash(logged_in_employee.employee_id, old_pwd) != logged_in_employee.hashed_password:
                msgbox.showerror("Error", "Old password is incorrect")
                print(old_pwd)
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
            row=3, column=0, columnspan=2, pady=20
        )
