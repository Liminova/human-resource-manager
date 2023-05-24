import os
from tkinter import DISABLED, NORMAL
from tkinter import messagebox as msgbox

import customtkinter as ctk

from database.mongo import department_repo, employee_repo
from frontend.helpers_gui import *
from frontend.helpers_gui.global_styling import *
from models import Company, Department

the_company = Company()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

Width = 1024
Height = 768


class DepartmentGui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Department Management")
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
            "Add Department": self.__admin_add_department,
            "Remove Department": self.__admin_remove_department,
            "Update Department": self.__admin_update_department,
            "View Department": self.__view_department,
            "Employees w/o department": self.__admin_list_employees_wo_department,
            "Add/remove Employee": self.__admin_add_remove_employee,
            "Back": self.__back_to_homepage,
        }

    def employee(self):
        return {"View Department": self.__view_department, "Back": self.__back_to_homepage}

    def __clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def __back_to_homepage(self):
        from .homepage import Homepage

        self.destroy()
        Homepage().mainloop()

    # region: admin functions

    def __admin_add_department(self):
        # - 2 columns
        # 0: label + name entry
        # 1: label + id entry
        # 2: add btn

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        entries = [ctk.CTkEntry(master=main_frame) for _ in range(2)]
        for row, entry, label, placeholder in zip((0, 1), entries, ("Name: ", "ID: "), ("BHYT", "1")):
            ctk.CTkLabel(master=main_frame, text=label, **label_desc_style).grid(
                row=row, column=0, pady=(20, 0), padx=20, sticky="w"
            )
            entry.configure(placeholder_text=placeholder, **input_box_style)
            entry.grid(row=row, column=1, pady=(20, 0), padx=(0, 20))

        def _add_department():
            nonlocal entries
            values = [entry.get() for entry in entries]

            for value in values:
                if not value:
                    msgbox.showerror("Error", "Please fill in all the fields")
                    return

            _dept = Department()
            for setter, value in zip((_dept.set_name, _dept.set_id), values):
                setter(value).unwrap()

            the_company.departments.append(_dept)

            if os.getenv("HRMGR_DB") == "TRUE":
                department_repo.insert_one(_dept.dict(by_alias=True))
            msgbox.showinfo("Success", "Department added successfully")

        ctk.CTkButton(master=main_frame, text="Add", command=_add_department, **btn_action_style).grid(
            row=2, column=0, columnspan=2, pady=20
        )

    def __admin_remove_department(self):
        # - 1 column
        # 0: select department from list
        # 1: remove department btn

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        # Select a department from a list
        dept_idx_select: ctk.Variable = ctk.IntVar(value=0)
        display_list(
            _master=main_frame,
            options=tuple(f"{dept.dept_id} - {dept.name}" for dept in the_company.departments),
            returned_idx=[dept_idx_select],
            err_msg="No department to remove",
            place=(0, 0),
            colspan=1,
        )

        def _remove_department():
            if not msgbox.askyesno("Confirmation", "Are you sure you want to remove this department?"):
                return
            depts = the_company.departments
            selected_dept = depts[dept_idx_select.get()]

            # remove department from company
            depts.remove(selected_dept)

            # remove department from employees
            affected_empls = []
            for emp in the_company.employees:
                if emp.department_id == selected_dept.id:
                    emp.department_id = ""
                    affected_empls.append(emp)

            # update db
            if os.getenv("HRMGR_DB") == "TRUE":
                department_repo.delete_one({"id": selected_dept.id})
                for emp in affected_empls:
                    employee_repo.update_one({"id": emp.id}, emp.dict(include={"department_id"}), upsert=True)

            msgbox.showinfo("Success", "Department removed successfully")
            merge_callable(self.__clear_right_frame, self.__admin_remove_department)()

        ctk.CTkButton(master=main_frame, text="Remove", command=_remove_department, **btn_action_style).grid(
            row=2, column=0, columnspan=2, pady=(0, 20)
        )

    def __admin_update_department(self):
        # - 2 columns
        # 0: select department from list
        # 1: label + input name
        # 2: label + input id
        # 3: update btn

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        # Select a department from a list
        dept_idx_select: ctk.Variable = ctk.IntVar(value=0)
        display_list(
            _master=main_frame,
            options=tuple(f"{dept.dept_id} - {dept.name}" for dept in the_company.departments),
            returned_idx=[dept_idx_select],
            err_msg="No department found",
            place=(0, 0),
            colspan=2,
            pady=(20, 0),
        )

        # Input new department name
        entries = [ctk.CTkEntry(master=main_frame) for _ in range(2)]
        for row, entry, label, placeholder in zip((1, 2), entries, ("New name", "New ID"), ("BHYT", "BHYT")):
            ctk.CTkLabel(master=main_frame, text=label, **label_desc_style).grid(row=row, column=0, pady=(20, 0), padx=20)
            entry.configure(placeholder_text=placeholder, **input_box_style)
            entry.grid(row=row, column=1, pady=(20, 0), padx=(0, 20))

        def _update_department():
            nonlocal dept_idx_select, entries
            values = [entry.get() for entry in entries]
            selected_dept = the_company.departments[dept_idx_select.get()]

            old_dept_id = selected_dept.dept_id
            # update department
            selected_dept.name = values[0]
            selected_dept.dept_id = values[1]

            # update employees
            affected_emps = []
            for emp in the_company.employees:
                if emp.department_id == old_dept_id:
                    emp.department_id = selected_dept.dept_id
                    affected_emps.append(emp)

            # update db
            if os.getenv("HRMGR_DB") == "TRUE":
                department_repo.update_one({"id": selected_dept.id}, selected_dept.dict(by_alias=True), upsert=True)
                for emp in affected_emps:
                    employee_repo.update_one({"id": emp.id}, emp.dict(include={"department_id"}), upsert=True)

            msgbox.showinfo("Success", "Department updated successfully")
            merge_callable(self.__clear_right_frame, self.__admin_update_department)()

        ctk.CTkButton(master=main_frame, text="Update", command=_update_department, **btn_action_style).grid(
            row=3, column=0, columnspan=2, pady=20
        )

    def __admin_add_remove_employee(self, mode: int = 1):
        # - 2 columns
        # 0: 2 buttons, switch between 2 modes: 1. add, 2. remove
        # 1: select employee from list | select department from list (depends on mode)
        # 2: submit btn

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        # based on add/remove mode, this contains dept without/with the selected employee
        filtered_depts: list[Department] = []
        emp_idx_select: ctk.Variable = ctk.IntVar(value=0)
        dept_idx_select: ctk.Variable = ctk.IntVar(value=0)

        select_dept_frame = ctk.CTkBaseClass(None)

        def _switch_mode():
            nonlocal mode
            mode = 2 if mode == 1 else 1
            self.__clear_right_frame()
            self.__admin_add_remove_employee(mode=mode)

        ctk.CTkButton(
            master=main_frame,
            **btn_action_style,
            text="Add",
            command=_switch_mode,
            state=(NORMAL if mode == 2 else DISABLED),
        ).grid(row=0, column=0, pady=(20, 0), padx=20)
        ctk.CTkButton(
            master=main_frame,
            **btn_action_style,
            text="Remove",
            command=_switch_mode,
            state=(NORMAL if mode == 1 else DISABLED),
        ).grid(row=0, column=1, pady=(20, 0), padx=20)

        # Select employee from list
        def _update_dept_list():
            nonlocal emp_idx_select, select_dept_frame, dept_idx_select, filtered_depts

            depts = the_company.departments
            empls = the_company.employees

            if mode == 1:
                filtered_depts = [dept for dept in depts if dept.dept_id != empls[emp_idx_select.get()].department_id]
            elif mode == 2:
                filtered_depts = [dept for dept in depts if dept.dept_id == empls[emp_idx_select.get()].department_id]

            select_dept_frame.destroy()
            select_dept_frame = display_list(
                _master=main_frame,
                options=tuple(f"{dept.name} - {dept.dept_id}" for dept in filtered_depts),
                returned_idx=[dept_idx_select],
                err_msg=f"No department to {'add' if mode == 1 else 'remove'}",
                place=(1, 1),
                colspan=1,
                padx=(0, 20),
            )

        _update_dept_list()

        display_list(
            _master=main_frame,
            options=tuple(f"{empl.name} - {empl.employee_id}" for empl in the_company.employees),
            returned_idx=[emp_idx_select],
            err_msg="No employee to remove",
            place=(1, 0),
            colspan=1,
            cmd=_update_dept_list,
        )

        def _add_rm_empl_handler():
            nonlocal filtered_depts, emp_idx_select, dept_idx_select

            selected_dept = filtered_depts[dept_idx_select.get()]
            selected_empl = the_company.employees[emp_idx_select.get()]

            if mode == 1:
                selected_dept.members.append(selected_empl)
                selected_empl.department_id = selected_dept.dept_id
            elif mode == 2:
                selected_dept.members.remove(selected_empl)
                selected_empl.department_id = ""

            # update db
            if os.getenv("HRMGR_DB") == "TRUE":
                department_repo.update_one(
                    {"_id": selected_dept.id}, {"$set": selected_dept.dict(include={"members"})}, upsert=True
                )
                employee_repo.update_one(
                    {"_id": selected_empl.id}, {"$set": selected_empl.dict(include={"department_id"})}, upsert=True
                )

            msgbox.showinfo(
                "Success",
                f"Employee {selected_empl.name} {'added to' if mode == 1 else 'removed from'} {selected_dept.name} successfully",
            )
            self.__clear_right_frame()
            self.__admin_add_remove_employee(mode)

        ctk.CTkButton(master=main_frame, text="Submit", command=_add_rm_empl_handler, **btn_action_style).grid(
            row=3, column=0, columnspan=2, pady=(0, 20)
        )

    def __admin_list_employees_wo_department(self):
        # - 1 column
        # 0: list of employees without department

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        # Select employee from list
        radio_emp_idx_select: ctk.Variable = ctk.IntVar(value=0)
        empl_items = tuple(f"{empl.name} - {empl.employee_id}" for empl in the_company.employees if empl.department_id == "")
        display_list(
            _master=main_frame,
            options=empl_items,
            returned_idx=[radio_emp_idx_select],
            err_msg="No employee without department",
            place=(0, 0),
            colspan=1,
        )

    # endregion

    def __view_department(self):
        # - 1 column
        # 0: select department from list
        # 1: display a list of enrolled employees

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        ctk.CTkLabel(master=main_frame, text="View Department", **label_title_style).grid(
            row=0, column=0, columnspan=2, pady=(20, 0)
        )

        # Select a department from a list
        dept_idx_select: ctk.Variable = ctk.IntVar(value=0)
        empl_list_frame = ctk.CTkBaseClass(None)

        def update_empl_list_frame():
            nonlocal empl_list_frame, dept_idx_select

            empl_list_frame.destroy()
            empl_list_frame = ctk.CTkFrame(master=main_frame)
            empl_list_frame.grid(row=1, column=0, columnspan=1)

            dept = the_company.departments[dept_idx_select.get()]
            empl_list_frame = display_list(
                _master=main_frame,
                options=tuple(f"{empl.name} - {empl.employee_id}" for empl in dept.members),
                err_msg="No employee in this department",
                place=(1, 0),
                colspan=1,
                pady=(0, 20),
            )

        update_empl_list_frame()

        display_list(
            _master=main_frame,
            options=tuple(f"{dept.name} - {dept.dept_id}" for dept in the_company.departments),
            returned_idx=[dept_idx_select],
            err_msg="No department to view",
            place=(0, 0),
            colspan=1,
            cmd=update_empl_list_frame,
        )
