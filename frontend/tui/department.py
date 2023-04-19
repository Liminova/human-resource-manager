from __future__ import annotations
import os

from ..helpers import *
from models import Department, Company
from database.mongo import department_repo, employee_repo
from option import Result, Ok

the_company: Company = Company()


class MenuDepartment:
    def __init__(self) -> None:
        self.mainloop = self.admin if the_company.logged_in_employee.is_admin else self.employee

    def admin(self) -> Result[None, str]:
        last_msg = ""
        while True:
            last_msg = refresh(last_msg)
            department_menu = [
                "[1] Add department",
                "[2] Remove department",
                "[3] Update information for department",
                "[4] Add employee to department",
                "[5] Remove employee from department",
                "[6] View details of department",
                "[7] List all departments",
                "[8] List employees without a department",
                "[9] Back",
            ]

            title = "Department management"

            choice = get_user_option_from_menu("Department management", department_menu)
            match choice:
                case 1:
                    last_msg: str = self.__add()
                case 2:
                    last_msg: str = self.__remove()
                case 3:
                    last_msg: str = self.__update()
                case 4:
                    last_msg: str = self.__add_employee()
                case 5:
                    last_msg: str = self.__remove_employee()
                case 6:
                    last_msg: str = self.__view()
                case 7:
                    last_msg: str = self.__view_all()
                case 8:
                    last_msg: str = self.__view_employees_not_belong_to_any_department()
                case 9:
                    return Ok(None)
                case _:
                    last_msg = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def employee(self) -> Result[None, str]:
        logged_in_employee = the_company.logged_in_employee
        last_msg: str = ""
        while True:
            last_msg = refresh(last_msg)
            department_menu = ["[1] View details of one", "[2] List all", "[3] Back"]

            choice = get_user_option_from_menu("Department management", department_menu)
            match choice:
                case 1:
                    last_msg = self.__view()
                case 2:
                    last_msg = self.__view_all()
                case 3:
                    return Ok(None)
                case _:
                    last_msg = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def __add(self) -> str:
        # create a new, empty department
        dept = Department()

        # assign values to the department object
        input_fields = [
            ("Enter department name", dept.set_name),
            ("Enter department ID", dept.set_id),
        ]
        for promt, setter in input_fields:
            if (msg := loop_til_valid_input(promt, setter)) != "":
                return msg

        # add the department to the company
        the_company.departments.append(dept)
        if os.getenv("HRMGR_DB") == "TRUE":
            department_repo.insert_one(dept.dict(by_alias=True))

        return f"Department {FCOLORS.GREEN}{dept.name}{FCOLORS.END} added successfully!"

    def __remove(self) -> str:
        depts = the_company.departments
        empls = the_company.employees

        # get the index of the department selected by the user
        dept_selected_index = get_user_option_from_list("Select a department to remove", [f"{dept.name} ({dept.dept_id})" for dept in depts])
        if dept_selected_index == -1:
            return NO_DEPARTMENT_MSG
        elif dept_selected_index == -2:
            return ""

        # THIS IS A COPY OF THE OBJECT, NOT A REFERENCE
        _dept = depts[dept_selected_index]

        # remove the department id from all employees in the department
        for emp in empls:
            if emp.department_id == _dept.dept_id:
                emp.department_id = ""
                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one({"_id": emp.id}, {"$set": emp.dict(exclude={"id"}, by_alias=True)}, upsert=True)

        # remove the department from the company
        depts.remove(_dept)
        if os.getenv("HRMGR_DB") == "TRUE":
            department_repo.delete_one({"_id": _dept.id})

        return f"Department {FCOLORS.RED}{_dept.name}{FCOLORS.END} removed successfully!"

    def __update(self) -> str:
        depts = the_company.departments

        # a list containing the string representation of each department
        dept_items = [f"{dept.name} ({dept.dept_id})" for dept in depts]

        # get the index of the department to update
        dept_selected_index = get_user_option_from_list("Select a department to update", dept_items)
        if dept_selected_index == -1:
            return NO_DEPARTMENT_MSG
        elif dept_selected_index == -2:
            return ""

        # THIS IS A COPY OF THE OBJECT, NOT A REFERENCE
        _dept = depts[dept_selected_index]

        # get the new values for the department
        input_fields = [
            ("Enter new department name", _dept.set_name),
            ("Enter new department ID", _dept.set_id),
        ]
        for promt, setter in input_fields:
            if (msg := loop_til_valid_input(promt, setter)) != "":
                return msg

        # update the department in the company
        if os.getenv("HRMGR_DB") == "TRUE":
            department_repo.update_one({"_id": _dept.id}, {"$set": _dept.dict(exclude={"id"}, by_alias=True)}, upsert=True)

        return f"Department {FCOLORS.GREEN}{_dept.name}{FCOLORS.END} updated successfully!"

    def __add_employee(self) -> str:
        depts = the_company.departments
        empls = the_company.employees

        # get the index of the employee selected by the user
        empl_idx_select = get_user_option_from_list(
            "Select an employee to add to a department", [f"{employee.name} ({employee.employee_id})" for employee in empls]
        )
        if empl_idx_select in (-1, -2):
            return NO_EMPLOYEE_MSG if empl_idx_select == -1 else ""

        if not the_company.can_modify("department", empls[empl_idx_select]):
            return "Only other admins can manage departments!"

        # get the index of the department selected by the user
        dept_idx_select = get_user_option_from_list("Select a department to add the employee to", [f"{dept.name} ({dept.dept_id})" for dept in depts])
        if dept_idx_select in (-1, -2):
            return NO_DEPARTMENT_MSG if dept_idx_select == -1 else ""

        # THIS IS A COPY OF THE OBJECT, NOT A REFERENCE
        _dept = depts[dept_idx_select]
        _empl = empls[empl_idx_select]

        # check if the employee is already in the department
        if _empl.department_id == _dept.dept_id:
            return "Employee {}{}{} is already in department {}{}{}!".format(
                FCOLORS.GREEN, _empl.name, FCOLORS.END, FCOLORS.GREEN, _dept.name, FCOLORS.END
            )

        # add the employee to the department and vice versa
        empls[empl_idx_select].department_id = depts[dept_idx_select].dept_id
        depts[dept_idx_select].members.append(empls[empl_idx_select])

        # update DB
        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one({"_id": _empl.id}, {"$set": _empl.dict(exclude={"id"}, by_alias=True)}, upsert=True)
            department_repo.update_one({"_id": _dept.id}, {"$set": _dept.dict(exclude={"id"}, by_alias=True)}, upsert=True)

        return f"Employee {FCOLORS.GREEN}{_empl.name}{FCOLORS.END} added to department {FCOLORS.GREEN}{_dept.name}{FCOLORS.END} successfully!"

    def __remove_employee(self) -> str:
        depts = the_company.departments
        empls = the_company.employees

        # get the index of the employee selected by the user
        empl_idx_select = get_user_option_from_list(
            "Select an employee to remove from a department", [f"{employee.name} ({employee.employee_id})" for employee in empls]
        )
        if empl_idx_select in (-1, -2):
            return NO_EMPLOYEE_MSG if empl_idx_select == -1 else ""

        # get the index of the department selected by the user
        dept_idx_select = get_user_option_from_list(
            "Select a department to remove the employee from", [f"{dept.name} ({dept.dept_id})" for dept in depts]
        )
        if dept_idx_select in (-1, -2):
            return NO_DEPARTMENT_MSG if dept_idx_select == -1 else ""

        # THIS IS A COPY OF THE OBJECT, NOT A REFERENCE
        _empl = empls[empl_idx_select]
        _dept = depts[dept_idx_select]

        # remove the employee from the department and vice versa
        if _empl.department_id == "":
            return "Employee {}{}{} is not in a department!".format(FCOLORS.GREEN, _empl.name, FCOLORS.END)
        else:
            empls[empl_idx_select].department_id = ""
            depts[dept_idx_select].members = [empl for empl in depts[dept_idx_select].members if empl.employee_id != _empl.employee_id]

        # update DB
        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one({"_id": _empl.id}, {"$set": _empl.dict(exclude={"id"}, by_alias=True)}, upsert=True)
            department_repo.update_one({"_id": _dept.id}, {"$set": _dept.dict(exclude={"id"}, by_alias=True)}, upsert=True)

        return f"Employee {FCOLORS.GREEN}{_empl.name}{FCOLORS.END} removed from department {FCOLORS.GREEN}{_dept.name}{FCOLORS.END} successfully!"

    def __view(self) -> str:
        depts = the_company.departments

        # get the index of the department from the user
        dept_idx_select = get_user_option_from_list("Select a department to view info", [f"{dept.name} ({dept.dept_id})" for dept in depts])
        if dept_idx_select in (-1, -2):
            return NO_DEPARTMENT_MSG if dept_idx_select == -1 else ""
        _dept = the_company.departments[dept_idx_select]

        # print the department info
        clrscr()
        print(_dept)
        input(ENTER_TO_CONTINUE_MSG)

        return ""

    def __view_all(self) -> str:
        depts = the_company.departments
        if len(depts) == 0:
            return NO_DEPARTMENT_MSG

        clrscr()
        for dept in depts:
            print(dept)
            print("")
        input(ENTER_TO_CONTINUE_MSG)

        return ""

    def __view_employees_not_belong_to_any_department(self) -> str:
        empls = the_company.employees
        if len(empls) == 0:
            return NO_EMPLOYEE_MSG

        clrscr()
        for empl in empls:
            if empl.department_id == "":
                print(empl)
                print("")
        input(ENTER_TO_CONTINUE_MSG)

        return ""
