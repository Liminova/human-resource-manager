import os
import customtkinter as ctk
from tkinter import messagebox as msgbox
from tkinter import W, E, NORMAL, DISABLED

from models import Company, BenefitPlan, Employee
from database.mongo import benefit_repo, employee_repo
from frontend.helpers_gui import *
from frontend.helpers_gui.global_styling import *

the_company = Company()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

Width = 1024
Height = 768


class BenefitPlanGui(ctk.CTk):
    def __init__(self, master=None):
        super().__init__()
        self.title("Benefit Plan Management")
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
            "Add/remove/modify": self.__admin_add_rm_modify,
            "Apply/remove": self.__admin_apply_rm,
            "Request to enroll": self.__request,
            "Resolve requests": self.__admin_resolve,
            "View details": self.__view_details,
            "List empls w/o benefit": self.__admin_empls_w_o_benefit,
            "Back": self.__back_to_homepage,
        }

    def employee(self):
        return {
            "View benefit plans": self.__view_details,
            "Request to enroll": self.__request,
            "Back": self.__back_to_homepage,
        }

    def __clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def __back_to_homepage(self):
        from .homepage import Homepage

        self.destroy()
        Homepage().mainloop()

    def __admin_add_rm_modify(self, mode: int = 1):
        # - 3 columns
        # 0: 3 buttons, switch between 3 modes: 1. add, 2. remove, 3. modify
        # 1: Table to choose bnf if modify or remove, "Creating..." if add
        # 2: Label | Input name
        # 3: Label | Input desc
        # 4: Label | Input cost
        # 5: Button to submit

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        # region: initialize widgets and variables
        input_name = ctk.CTkEntry(master=main_frame, **input_box_style)
        input_desc = ctk.CTkEntry(master=main_frame, **input_box_style)
        input_cost = ctk.CTkEntry(master=main_frame, **input_box_style)

        bnf_idx_select = ctk.IntVar()

        btn_add = ctk.CTkButton(master=main_frame, text="Add", **btn_action_style)
        btn_remove = ctk.CTkButton(master=main_frame, text="Remove", **btn_action_style)
        btn_modify = ctk.CTkButton(master=main_frame, text="Modify", **btn_action_style)
        # endregion

        # region: switch between modes handler
        first_row: ctk.CTkBaseClass = ctk.CTkFrame(None)

        def _switch_mode(new_mode: int):
            nonlocal input_name, input_desc, input_cost, btn_modify, btn_remove, btn_add
            nonlocal first_row, mode, bnf_idx_select, main_frame
            first_row.destroy()
            first_row = ctk.CTkLabel(master=main_frame, text="Adding new benefit...", **label_desc_style)
            first_row.grid(row=1, column=0, columnspan=3, padx=20, pady=(0, 20))

            mode = new_mode
            match new_mode:
                case 1:  # add
                    # enable input boxes, <remove> and <modify> buttons
                    # disable <add> button (already clicked)
                    for elem in (input_name, input_desc, input_cost, btn_modify, btn_remove):
                        elem.configure(state=NORMAL)
                    btn_add.configure(state=DISABLED)

                case 2:  # remove
                    first_row.destroy()
                    first_row = display_list(
                        _master=main_frame,
                        options=tuple(f"{b.name} - {b.cost}" for b in the_company.benefits),
                        err_msg="No benefit plan to remove",
                        returned_idx=[bnf_idx_select],
                        place=(1, 0),
                        colspan=3,
                        pady=(0, 15),
                    )
                    # disable input boxes, <delete> btn (clicked)
                    # enable <add> and <modify> buttons
                    for elem in (input_name, input_desc, input_cost, btn_remove):
                        elem.configure(state=DISABLED)
                    for elem in (btn_add, btn_modify):
                        elem.configure(state=NORMAL)

                case 3:  # modify
                    first_row.destroy()
                    first_row = display_list(
                        _master=main_frame,
                        options=tuple(f"{b.name} - {b.cost}" for b in the_company.benefits),
                        err_msg="No benefit plan to modify",
                        returned_idx=[bnf_idx_select],
                        place=(1, 0),
                        colspan=3,
                        pady=(0, 15),
                    )
                    # enable input boxes, <add> and <remove> buttons
                    # disable <modify> button (clicked)
                    for elem in (input_name, input_desc, input_cost, btn_add, btn_remove):
                        elem.configure(state=NORMAL)
                    btn_modify.configure(state=DISABLED)

        _switch_mode(mode)

        btn_add.grid(row=0, column=0, padx=(20, 0), pady=20)
        btn_add.configure(command=lambda: _switch_mode(1))
        btn_remove.grid(row=0, column=1, padx=20, pady=20)
        btn_remove.configure(command=lambda: _switch_mode(2))
        btn_modify.grid(row=0, column=2, padx=(0, 20), pady=20)
        btn_modify.configure(command=lambda: _switch_mode(3))
        # endregion

        # region: input boxes
        entries = [input_name, input_desc, input_cost]
        for row, entry, title in zip(range(2, 5), entries, ("Name: ", "Description: ", "Cost: ")):
            ctk.CTkLabel(master=main_frame, text=title, **label_desc_style).grid(
                row=row, column=0, sticky=W, padx=(20, 0), pady=10
            )
            entry.grid(row=row, column=1, columnspan=2, padx=20, sticky=E)
        # endregion

        # region: submit button
        def _submit_handler():
            nonlocal input_name, input_desc, input_cost, bnf_idx_select, mode
            name, desc, cost = input_name.get(), input_desc.get(), input_cost.get()
            bnf_idx_select = bnf_idx_select.get()
            bnfs = the_company.benefits

            # for message box later
            bnf_name = bnfs[bnf_idx_select].name if mode == 3 else ""

            match mode:
                case 1:  # add
                    new_benefit = BenefitPlan()
                    new_benefit.set_name(name)
                    new_benefit.set_description(desc)
                    new_benefit.set_cost(float(cost))
                    if (not name) and (not desc) and (not cost):
                        msgbox.showerror("Error", "Please fill in all fields")

                    the_company.benefits.append(new_benefit)
                    if os.getenv("HRMGR_DB") == "TRUE":
                        benefit_repo.insert_one(new_benefit.dict(by_alias=True))

                case 2:  # remove
                    selected_bnf = bnfs[bnf_idx_select]
                    bnf_name = selected_bnf.name

                    if bnf_idx_select is None:
                        msgbox.showerror("Error", "Please select a benefit plan to remove")
                        return

                    # remove the benefit from the company
                    the_company.benefits.remove(the_company.benefits[bnf_idx_select])
                    if os.getenv("HRMGR_DB") == "TRUE":
                        benefit_repo.delete_one({"_id": selected_bnf.id})

                    # remove the benefit from employees
                    for empl in the_company.employees:
                        if selected_bnf.name not in empl.benefits:
                            continue
                        empl.benefits.remove(selected_bnf.name)
                        if os.getenv("HRMGR_DB") == "TRUE":
                            employee_repo.update_one(
                                {"_id": empl.id}, {"$set": empl.dict(include={"benefits"})}, upsert=True
                            )

                case 3:  # modify
                    if bnf_idx_select is None:
                        msgbox.showerror("Error", "Please select a benefit plan to modify")
                        return
                    if (not name) and (not desc) and (not cost):
                        msgbox.showerror("Error", "Please fill in at least one field")
                        return
                    selected_bnf = the_company.benefits[bnf_idx_select]
                    selected_bnf.set_name(name) if name else None
                    selected_bnf.set_description(desc) if desc else None
                    selected_bnf.set_cost(float(cost)) if cost else None

                    if os.getenv("HRMGR_DB") == "TRUE":
                        benefit_repo.update_one(
                            {"_id": selected_bnf.id}, {"$set": selected_bnf.dict(by_alias=True)}, upsert=True
                        )

            msgbox.showinfo("Success", f"Benefit plan {bnf_name} has been {['added', 'removed', 'modified'][mode - 1]}")

            self.__clear_right_frame()
            self.__admin_add_rm_modify(mode)

        ctk.CTkButton(master=main_frame, text="Submit", command=_submit_handler, **btn_action_style).grid(
            row=5, column=0, columnspan=3, pady=20
        )
        # endregion

    def __admin_apply_rm(self, current_submenu: int = 1):
        # 0: 2 buttons: apply, remove
        # 1: Table to choose employee | Table to choose benefit
        # 2: - if in apply: Apply button
        #    - if in remove: Benefits of this employee | Remove button

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        # because later we will have index of benefits (in empl || not in empl), not the list of benefits in the company
        custom_bnfs: list[BenefitPlan] = []
        custom_bnf_items = tuple()

        # region: when user select an employee, update the benefits list
        bnf_idx_select = ctk.IntVar()
        bnf_list_frame = ctk.CTkBaseClass(None)

        empl_idx_select = ctk.IntVar()

        def _update_bnf_list():
            nonlocal bnf_idx_select, empl_idx_select, current_submenu, custom_bnf_items, bnf_list_frame, custom_bnfs

            # get the employee
            selected_empl = the_company.employees[empl_idx_select.get()]

            bnfs = the_company.benefits
            custom_bnfs = [bnf for bnf in bnfs if (current_submenu == 1) ^ (bnf.name in selected_empl.benefits)]
            # Explanation:
            # the ^ operator is XOR, which means it will return True if only one of the two operands is True
            # so if it's in apply mode, we want to show only the benefits that are not in the employee's benefits list
            # if it's in remove mode, we want to show only the benefits that are in the employee's benefits list

            custom_bnf_items = tuple([f"{bnf.name} - {bnf.cost}" for bnf in custom_bnfs])

            # this list will be refreshed every time user select an employee
            bnf_list_frame.destroy()
            bnf_list_frame = display_list(
                _master=main_frame,
                options=custom_bnf_items,
                returned_idx=[bnf_idx_select],
                err_msg="No benefits",
                place=(1, 1),
                colspan=1,
                pady=0,
            )

        _update_bnf_list()
        display_list(
            _master=main_frame,
            options=tuple([f"{empl.employee_id} - {empl.name}" for empl in the_company.employees]),
            returned_idx=[empl_idx_select],
            err_msg="No employees",
            place=(1, 0),
            colspan=1,
            cmd=_update_bnf_list,
            pady=0,
        )
        # endregion

        # region: 2 buttons to switch between apply and remove submenu
        btn_apply = ctk.CTkButton(master=main_frame, text="Add benefit to employee", **btn_action_style)
        btn_remove = ctk.CTkButton(master=main_frame, text="Remove benefit from employee", **btn_action_style)
        btn_apply.grid(row=0, column=0, padx=(20, 10), pady=20)
        btn_remove.grid(row=0, column=1, padx=(10, 20), pady=20)

        def _switch_mode_handler():
            nonlocal btn_apply, btn_remove, current_submenu, bnf_list_frame, _update_bnf_list
            current_submenu = 3 - current_submenu

            if current_submenu == 1:
                btn_apply.configure(state=DISABLED)
                btn_remove.configure(state=NORMAL)
            else:
                btn_apply.configure(state=NORMAL)
                btn_remove.configure(state=DISABLED)
            bnf_list_frame.destroy()
            _update_bnf_list()

        btn_apply.configure(command=_switch_mode_handler)
        btn_remove.configure(command=_switch_mode_handler)
        # endregion

        # region: submit button
        def _submit_handler():
            nonlocal empl_idx_select, bnf_idx_select, current_submenu
            selected_empl = the_company.employees[empl_idx_select.get()]
            selected_bnf = custom_bnfs[bnf_idx_select.get()]

            if current_submenu == 1:  # apply
                if not the_company.can_modify("benefits", selected_empl):
                    msgbox.showerror("Error", "Cannot modify benefits")
                    self.__clear_right_frame()
                    self.__admin_apply_rm(current_submenu)
                    return

                selected_empl.benefits.append(selected_bnf.name)
                selected_bnf.enrolled_employees.append(selected_empl)

                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one(
                        {"_id": selected_empl.id}, {"$set": selected_empl.dict(include={"benefits"})}, upsert=True
                    )
                    benefit_repo.update_one(
                        {"_id": selected_bnf.id}, {"$set": selected_bnf.dict(include={"enrolled_employees"})}, upsert=True
                    )

            elif current_submenu == 2:  # remove
                selected_empl.benefits.remove(selected_bnf.name)
                selected_bnf.enrolled_employees.remove(selected_empl)

                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one(
                        {"_id": selected_empl.id}, {"$set": selected_empl.dict(include={"benefits"})}, upsert=True
                    )
                    benefit_repo.update_one(
                        {"_id": selected_bnf.id}, {"$set": selected_bnf.dict(include={"enrolled_employees"})}, upsert=True
                    )

            msgbox.showinfo(
                "Success",
                "Benefit plan {} {} employee {} successfully".format(
                    selected_bnf.name, "added to" if current_submenu == 1 else "removed from", selected_empl.name
                ),
            )

            self.__clear_right_frame()
            self.__admin_apply_rm(current_submenu)

        ctk.CTkButton(master=main_frame, text="Submit", command=_submit_handler, **btn_action_style).grid(
            row=2, column=0, columnspan=2, pady=20
        )
        # endregion

    def __request(self):
        # 0: Table to choose benefit
        # 1: Request button

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        # region: variables
        bnf_idx_select = ctk.IntVar()
        bnfs_empl_not_in = tuple(
            bnf for bnf in the_company.benefits if bnf.name not in the_company.logged_in_employee.benefits
        )
        # endregion

        # region: table to choose benefit
        display_list(
            _master=main_frame,
            options=tuple(f"{bnf.name} - {bnf.cost}" for bnf in bnfs_empl_not_in),
            returned_idx=[bnf_idx_select],
            err_msg="No benefits",
            place=(0, 0),
            colspan=1,
            pady=(20, 0),
        )
        # endregion

        # region: request button
        def _request_handler():
            nonlocal bnf_idx_select
            selected_bnf = bnfs_empl_not_in[bnf_idx_select.get()]

            if the_company.logged_in_employee in selected_bnf.pending_requests:
                msgbox.showinfo("Error", "You have already requested this benefit")
                return

            selected_bnf.pending_requests.append(the_company.logged_in_employee)

            if os.getenv("HRMGR_DB") == "TRUE":
                benefit_repo.update_one(
                    {"_id": selected_bnf.id}, {"$set": selected_bnf.dict(include={"pending_requests"})}, upsert=True
                )
            msgbox.showinfo("Success", f"Benefit plan {selected_bnf.name} requested")
            merge_callable(self.__clear_right_frame, self.__request)()

        ctk.CTkButton(master=main_frame, text="Request", command=_request_handler, **btn_action_style).grid(
            row=1, column=0, pady=20
        )
        # endregion

    def __admin_resolve(self):
        # 0: Table to choose benefit | Table to choose employee
        # 1: Approve button | Reject button

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        # region: variables
        # we need them here to disable the buttons when there is no pending request
        btn_approve = ctk.CTkButton(master=main_frame, text="Approve", **btn_action_style)
        btn_reject = ctk.CTkButton(master=main_frame, text="Reject", **btn_action_style)

        bnf_idx_select = ctk.IntVar()
        empl_idx_select = ctk.IntVar()

        bnfs_have_pending: list[BenefitPlan] = []
        bnf_item_have_pending: tuple[str] = tuple()

        # this changes every time the user select a benefit
        pending_empls: list[Employee] = []
        empl_list_frame = ctk.CTkBaseClass(None)
        # endregion

        # region: when user select a benefit, update the employee list
        def _update_empl_list():
            nonlocal empl_idx_select, bnfs_have_pending, bnf_item_have_pending, pending_empls, empl_list_frame
            bnfs_have_pending = [bnf for bnf in the_company.benefits if bnf.pending_requests]

            if len(bnfs_have_pending) == 0:
                btn_approve.configure(state=DISABLED)
                btn_reject.configure(state=DISABLED)
                return

            bnf_item_have_pending = tuple(f"{bnf.name} - {bnf.cost}" for bnf in bnfs_have_pending)
            pending_empls = bnfs_have_pending[bnf_idx_select.get()].pending_requests

            empl_list_frame.destroy()
            empl_list_frame = display_list(
                _master=main_frame,
                options=tuple(f"{empl.name} - {empl.employee_id}" for empl in pending_empls),
                returned_idx=[empl_idx_select],
                err_msg="No pending requests",
                place=(0, 1),
                colspan=1,
                pady=(20, 0),
            )

        _update_empl_list()

        display_list(
            _master=main_frame,
            options=bnf_item_have_pending,
            returned_idx=[bnf_idx_select],
            err_msg="No employees requesting",
            place=(0, 0),
            colspan=1,
            cmd=_update_empl_list,
            pady=(20, 0),
        )
        if len(bnf_item_have_pending) == 0:
            display_list(
                _master=main_frame,
                options=tuple(),
                err_msg="No employees requesting",
                place=(0, 1),
                colspan=1,
                pady=(20, 0),
                padx=(0, 20),
            )

        # endregion

        # region: approve button | reject button
        btn_approve.grid(row=1, column=0, pady=20)
        btn_reject.grid(row=1, column=1, pady=20)

        def _action_handler(mode: int):
            nonlocal bnf_idx_select, empl_idx_select, bnfs_have_pending, pending_empls
            selected_bnf = bnfs_have_pending[bnf_idx_select.get()]
            selected_empl = pending_empls[empl_idx_select.get()]

            if not the_company.can_modify("benefits", selected_empl):
                msgbox.showinfo("Error", "You do not have permission to modify this employee")
                return

            selected_bnf.pending_requests.remove(selected_empl)
            selected_bnf.enrolled_employees.append(selected_empl)
            if os.getenv("HRMGR_DB") == "TRUE":
                benefit_repo.update_one(
                    {"_id": selected_bnf.id},
                    {"$set": selected_bnf.dict(include={"pending_requests", "enrolled_employees"})},
                    upsert=True,
                )
            msgbox.showinfo("Success", f"Benefit plan {selected_bnf.name} approved for {selected_empl.name}")
            merge_callable(self.__clear_right_frame, self.__admin_resolve)()

        def _reject_handler():
            nonlocal bnf_idx_select, empl_idx_select, bnfs_have_pending, pending_empls
            selected_bnf = bnfs_have_pending[bnf_idx_select.get()]
            selected_empl = pending_empls[empl_idx_select.get()]

            selected_bnf.pending_requests.remove(selected_empl)
            if os.getenv("HRMGR_DB") == "TRUE":
                benefit_repo.update_one(
                    {"_id": selected_bnf.id}, {"$set": selected_bnf.dict(include={"pending_requests"})}, upsert=True
                )
            msgbox.showinfo("Success", f"Benefit plan {selected_bnf.name} rejected for {selected_empl.name}")
            merge_callable(self.__clear_right_frame, self.__admin_resolve)()

        btn_approve.configure(command=_approve_handler)
        btn_reject.configure(command=_reject_handler)
        # endregion

        # region: if no pending requests, show message
        if len(bnfs_have_pending) == 0:
            for widget in zero_row.winfo_children():
                widget.destroy()
            ctk.CTkLabel(master=zero_row, text="No pending requests", **label_desc_style).grid(
                row=0, column=0, pady=20, padx=20
            )
            btn_approve.configure(state=DISABLED)
            btn_reject.configure(state=DISABLED)
        # endregion

    def __view_details(self):
        # 0: List of benefits | List of employees enrolled in that benefit
        # 1: Description of benefit

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        # region: variables
        bnf_idx_select = ctk.IntVar()
        empl_list_frame = ctk.CTkBaseClass(None)
        bnf_detail_widget = ctk.CTkLabel(master=main_frame)
        # endregion

        # region: when user select a benefit, update the employee list
        bnfs_items = tuple(f"{bnf.name} - {bnf.cost}" for bnf in the_company.benefits)

        def _update_empl_list():
            nonlocal bnf_idx_select, bnfs_items, bnf_detail_widget, empl_list_frame
            selected_bnf = the_company.benefits[bnf_idx_select.get()]
            empl_list_frame.destroy()
            empl_list_frame = display_list(
                _master=main_frame,
                options=tuple(f"{empl.name} - {empl.employee_id}" for empl in selected_bnf.enrolled_employees),
                err_msg="No employees enrolled",
                place=(0, 1),
                colspan=1,
                padx=(0, 20),
            )

            # update description
            bnf_detail_widget.destroy()
            bnf_detail_widget = ctk.CTkLabel(
                master=main_frame, text=(selected_bnf.description if selected_bnf.description else "No description")
            )
            bnf_detail_widget.grid(row=1, column=0, columnspan=2, pady=(0, 20), padx=20)

        display_list(
            _master=main_frame,
            options=bnfs_items,
            returned_idx=[bnf_idx_select],
            err_msg="No benefits",
            place=(0, 0),
            colspan=1,
            cmd=_update_empl_list,
        ) if len(bnfs_items) > 0 else None
        # endregion

        # if there's no benefit, display err msg instead of `display_list`
        if len(bnfs_items) == 0:
            for widget in zero_row.winfo_children():
                widget.destroy()
            zero_row.destroy()
            zero_row = ctk.CTkLabel(master=main_frame, text="No benefits", **label_desc_style)
            zero_row.grid(row=0, column=0, pady=20, padx=20, columnspan=2)

    def __admin_empls_w_o_benefit(self):
        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        # empls_w_o_bnf = tuple(empl for empl in the_company.employees if len(empl.benefits) == 0)
        empls_w_o_bnf = tuple(
            f"{empl.name} - {empl.employee_id}" for empl in the_company.employees if len(empl.benefits) == 0
        )
        display_list(
            _master=main_frame,
            options=tuple(f"{e.name} - {e.employee_id}" for e in the_company.employees if len(e.benefits) == 0),
            err_msg="No employees",
            place=(1, 0),
            colspan=1,
        )
