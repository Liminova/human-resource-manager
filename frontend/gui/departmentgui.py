import os
import customtkinter as ctk
from tkinter import messagebox as msgbox

from models import Company, Department
from database.mongo import department_repo, employee_repo
from frontend.helpers_gui import *
from frontend.helpers_gui.global_styling import *

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

    def __admin_add_employee(self):
        # - 2 columns
        # 0: 2 buttons, switch between 2 modes: 1. add, 2. remove
        # 1: select employee from list | select department from list (depends on mode)
        # 2: submit btn

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)


        # Select employee from list
        radio_emp_idx_select: ctk.Variable = ctk.IntVar(value=0)
        empl_items = tuple(f"{empl.name} - ({empl.id})" for empl in the_company.employees)
        _display_list = display_list(
            _master=main_frame, options=empl_items, returned_idx=[radio_emp_idx_select], selectable=True
        )
        if _display_list[0] is False:
            ctk.CTkLabel(master=main_frame, text="No employee to add", **label_desc_style).grid(
                row=1, column=0, columnspan=2, pady=(20, 0)
            )
        _display_list[1].grid(row=1, column=0, columnspan=2, pady=(20, 0))

        # Select department from list
        radio_dept_idx_select: ctk.Variable = ctk.IntVar(value=0)
        dept_items = tuple(f"{dept.dept_id} - {dept.name}" for dept in the_company.departments)
        _display_list = display_list(
            _master=main_frame, options=dept_items, returned_idx=[radio_dept_idx_select], selectable=True
        )
        if _display_list[0] is False:
            ctk.CTkLabel(master=main_frame, text="No department to add", **label_desc_style).grid(
                row=2, column=0, columnspan=2, pady=(20, 0)
            )
        _display_list[1].grid(row=2, column=0, columnspan=2, pady=(20, 0))

        def _add_employee():
            _empl = the_company.employees[radio_emp_idx_select.get()]
            _dept = the_company.departments[radio_dept_idx_select.get()]

            # add employee to department
            _dept.members.append(_empl)

            # update db
            if os.getenv("HRMGR_DB") == "TRUE":
                department_repo.update_one({"id": _dept.id}, {"$set": {"employees": _dept.members}})

            msgbox.showinfo("Success", "Employee added successfully")
            merge_callable(self.__clear_right_frame, self.__admin_add_employee)()

        ctk.CTkButton(master=main_frame, text="Add", command=_add_employee, **btn_action_style).grid(
            row=3, column=0, columnspan=2, pady=20
        )

    def __admin_remove_employee(self):
        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        ctk.CTkLabel(master=main_frame, text="Remove Employee", **label_title_style).grid(
            row=0, column=0, columnspan=2, pady=(20, 0)
        )

        # Select employee from list
        radio_emp_idx_select: ctk.Variable = ctk.IntVar(value=0)
        empl_items = tuple(f"{empl.name} - {empl.id}" for empl in the_company.employees)
        _display_list = display_list(
            _master=main_frame, options=empl_items, returned_idx=[radio_emp_idx_select], selectable=True
        )
        if _display_list[0] is False:
            ctk.CTkLabel(master=main_frame, text="No employee to remove", **label_desc_style).grid(
                row=1, column=0, columnspan=2, pady=(20, 0)
            )
        _display_list[1].grid(row=1, column=0, columnspan=2, pady=(20, 0))

        # Select department from list
        radio_dept_idx_select: ctk.Variable = ctk.IntVar(value=0)
        dept_items = tuple(f"{dept.dept_id} - {dept.name}" for dept in the_company.departments)
        _display_list = display_list(
            _master=main_frame, options=dept_items, returned_idx=[radio_dept_idx_select], selectable=True
        )
        if _display_list[0] is False:
            ctk.CTkLabel(master=main_frame, text="No department to remove", **label_desc_style).grid(
                row=2, column=0, columnspan=2, pady=(20, 0)
            )
        _display_list[1].grid(row=2, column=0, columnspan=2, pady=(20, 0))

        def _remove_employee():
            _empl = the_company.employees[radio_emp_idx_select.get()]
            _dept = the_company.departments[radio_dept_idx_select.get()]

            # remove employee from department
            _dept.members.remove(_empl)

            # update db
            if os.getenv("HRMGR_DB") == "TRUE":
                department_repo.update_one({"id": _dept.id}, {"$set": {"employees": _dept.members}})

            msgbox.showinfo("Success", "Employee removed successfully")
            merge_callable(self.__clear_right_frame, self.__admin_remove_employee)()

        ctk.CTkButton(master=main_frame, text="Remove", command=_remove_employee, **btn_action_style).grid(
            row=3, column=0, columnspan=2, pady=20
        )

    def __admin_list_employees_wo_department(self):
        # - 1 column
        # 0: list of employees without department

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        # Select employee from list
        radio_emp_idx_select: ctk.Variable = ctk.IntVar(value=0)
        empl_items = tuple(f"{empl.name} - {empl.id}" for empl in the_company.employees if empl.department_id is None)
        _display_list = display_list(
            _master=main_frame, options=empl_items, returned_idx=[radio_emp_idx_select], selectable=True
        )
        if _display_list[0] is False:
            ctk.CTkLabel(master=main_frame, text="No employee without department", **label_desc_style).grid(
                row=1, column=0, columnspan=2, pady=(20, 0)
            )
        _display_list[1].grid(row=1, column=0, columnspan=2, pady=(20, 0))

        def _add_employee():
            _empl = the_company.employees[radio_emp_idx_select.get()]

            # add employee to department
            the_company.departments[0].members.append(_empl)

            # update db
            if os.getenv("HRMGR_DB") == "TRUE":
                department_repo.update_one(
                    {"id": the_company.departments[0].id}, {"$set": {"employees": the_company.departments[0].members}}
                )

            msgbox.showinfo("Success", "Employee added successfully")
            merge_callable(self.__clear_right_frame, self.__admin_list_employees_wo_department)()

        ctk.CTkButton(master=main_frame, text="Add", command=_add_employee, **btn_action_style).grid(
            row=2, column=0, columnspan=2, pady=20
        )

    # endregion

    def __view_department(self):
        # - 1 column
        # 0: select department from list
        # 1: view department btn

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        ctk.CTkLabel(master=main_frame, text="View Department", **label_title_style).grid(
            row=0, column=0, columnspan=2, pady=(20, 0)
        )

        # Select a department from a list
        radio_dept_idx_select: ctk.Variable = ctk.IntVar(value=0)
        dept_items = tuple(f"{dept.name} - {dept.dept_id}" for dept in the_company.departments)
        _display_list = display_list(
            _master=main_frame, options=dept_items, returned_idx=[radio_dept_idx_select], selectable=True
        )
        if _display_list[0] is False:
            ctk.CTkLabel(master=main_frame, text="No department to view", **label_desc_style).grid(
                row=1, column=0, columnspan=2, pady=(20, 0)
            )

        def _view_department():
            _dept = the_company.departments[radio_dept_idx_select.get()]
            msgbox.showinfo("Department", f"Name: {_dept.name}\nID: {_dept.dept_id}")

        ctk.CTkButton(master=main_frame, text="View", command=_view_department, **btn_action_style).grid(
            row=2, column=0, columnspan=2, pady=20
        )
