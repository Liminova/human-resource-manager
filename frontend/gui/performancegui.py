import os
from datetime import datetime
from re import match
from tkinter import DISABLED, NORMAL, E, W
from tkinter import messagebox as msgbox

import customtkinter as ctk

from database.mongo import employee_repo
from frontend.helpers_gui import *
from frontend.helpers_gui.global_styling import *
from models import Company, Sale

the_company = Company()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

Width = 1024
Height = 768


class PerformanceGui(ctk.CTk):
    def __init__(self, master=None):
        super().__init__()
        self.title("Performance Management System")
        self.geometry(f"{Width}x{Height}")
        self.resizable(True, True)

        self.left_frame = ctk.CTkFrame(master=self, corner_radius=10)
        self.left_frame.pack(side=ctk.LEFT)
        self.left_frame.pack_propagate(False)
        self.left_frame.configure(width=320, height=760)

        self.right_frame = ctk.CTkFrame(master=self, border_width=2, corner_radius=10)
        self.right_frame.pack(side=ctk.RIGHT, expand=True)
        self.right_frame.pack_propagate(False)

        menu_buttons = MenuButtons(
            self.left_frame, self.right_frame, self.admin() if the_company.logged_in_employee.is_admin else self.employee()
        )
        menu_buttons.create()

    def admin(self):
        return {
            "Add sale": self.__admin_add_sale,
            "Remove sale": self.__admin_remove_sale,
            "View details of sale": self.__view_sale,
            "Find sale(s) by...	": self.__find_sale,
            "View perf of all empls": self.__admin_view_sales_perf,
            "Back": self.__back_to_homepage,
        }

    def employee(self):
        return {
            "View sales performance": self.__employee_view_sales_perf,
            "View info about a sale": self.__view_sale,
            "Find sale(s) by...": self.__find_sale,
            "Back": self.__back_to_homepage,
        }

    def __clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def __back_to_homepage(self):
        from .homepage import Homepage

        self.destroy()
        Homepage().mainloop()

    def __admin_add_sale(self):
        # - 1 column
        # 0: select an employee from list
        # 1: input box for sale id
        # 2:               revenue
        # 2:               cost
        # 3:               client id
        # 4:               client rating
        # 5:               client comment
        # 6: add sale button

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        empl_idx_select: ctk.Variable = ctk.IntVar(value=0)
        display_list(
            _master=main_frame,
            options=tuple(f"{e.employee_id} - {e.name}" for e in the_company.employees),
            returned_idx=[empl_idx_select],
            place=(0, 0),
            colspan=2,
            err_msg="No employee found",
            pady=(20, 0),
        )

        entries = [ctk.CTkEntry(master=main_frame) for _ in range(6)]
        labels = ("Sale ID", "Revenue: ", "Cost: ", "Client ID: ", "Client rating: ", "Client comment: ")
        placeholders = ("someid", "100", "50", "123", "5", "gud gud")
        for row, entry, label, placeholder in zip(range(1, 7), entries, labels, placeholders):
            ctk.CTkLabel(master=main_frame, text=label, **label_desc_style).grid(
                row=row, column=0, pady=(20, 0), padx=20, sticky="w"
            )
            entry.configure(placeholder_text=placeholder, **input_box_style)
            entry.grid(row=row, column=1, pady=(20, 0), padx=(0, 20))

        def add_sale_handler():
            nonlocal empl_idx_select, entries
            selected_empl = the_company.employees[empl_idx_select.get()]
            values = [e.get() for e in entries]

            # fmt: off
            new_sale = (
                Sale()
                .set_sale_id(values[0]).unwrap()
                .set_date(datetime.strftime(datetime.now(), "%Y-%m-%d")).unwrap()
                .set_revenue(values[1]).unwrap()
                .set_cost(values[2]).unwrap()
                .set_client_id(values[3]).unwrap()
                .set_client_rating(values[4]).unwrap()
                .set_client_comment(values[5]).unwrap()
            )
            # fmt: on

            new_sale.set_profit(str(new_sale.revenue - new_sale.cost)).unwrap()
            new_sale.employee_id = selected_empl.employee_id
            new_sale.employee_name = selected_empl.name

            selected_empl.performance.add_sale(new_sale)

            # update employee in db
            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.update_one(
                    {"_id": selected_empl.id}, {"$set": selected_empl.dict(include={"performance"})}, upsert=True
                )
            msgbox.showinfo("Success", "Sale added successfully")
            merge_callable(self.__clear_right_frame, self.__admin_add_sale)()

        ctk.CTkButton(master=main_frame, text="Add sale", command=add_sale_handler, **btn_action_style).grid(
            row=7, column=0, columnspan=2, pady=20
        )

    def __admin_remove_sale(self):
        # - 1 column
        # 0: select a sale from list
        # 1: remove button

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        # Select a sale from list
        all_sales = [s for e in the_company.employees for s in e.performance.sale_list]
        sale_idx_select: ctk.Variable = ctk.IntVar(value=0)
        display_list(
            _master=main_frame,
            options=tuple(f"{s.sale_id} from {s.employee_name}" for s in all_sales),
            returned_idx=[sale_idx_select],
            err_msg="No sale to remove",
            place=(0, 0),
        )

        def _remove_sale():
            nonlocal sale_idx_select, all_sales
            if not msgbox.askyesno("Confirm", "Are you sure you want to remove this sale?"):
                return
            selected_sale = all_sales[sale_idx_select.get()]
            affected_empl = the_company.get_empl_by_id(selected_sale.employee_id).unwrap()

            # remove sale from employee
            affected_empl.performance.sale_list.remove(selected_sale)

            # update employee in db
            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.update_one(
                    {"_id": affected_empl.id}, {"$set": affected_empl.dict(include={"performance"})}, upsert=True
                )
            msgbox.showinfo("Success", "Sale removed successfully")
            merge_callable(self.__clear_right_frame, self.__admin_remove_sale)()

        ctk.CTkButton(master=main_frame, text="Remove", command=_remove_sale, **btn_action_style).grid(
            row=1, column=0, columnspan=2, pady=(0, 20), padx=20
        )

    def __view_sale(self):
        # - 1 columns
        # 0: select a sale from list
        # 1: sale info

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        sale_frame = ctk.CTkFrame(None)

        # Custom sale list depending on admin or employee
        all_sales: list[Sale] = []
        if the_company.logged_in_employee.is_admin:
            all_sales = [s for e in the_company.employees for s in e.performance.sale_list]
        else:
            all_sales = the_company.logged_in_employee.performance.sale_list

        # Select a sale from list
        sale_idx_select: ctk.Variable = ctk.IntVar(value=0)

        def view_sale():
            nonlocal sale_idx_select, sale_frame, main_frame, all_sales
            if len(all_sales) == 0:
                return

            selected_sale = all_sales[sale_idx_select.get()]

            sale_frame.destroy()
            sale_frame = ctk.CTkFrame(master=main_frame)
            sale_frame.grid(row=1, column=0, pady=(0, 20), padx=20)

            titles = ("Employee ID", "Date", "Revenue", "Cost", "Client ID", "Client Rating", "Client Comment")
            values = (
                selected_sale.employee_id,
                datetime.strftime(selected_sale.date, "%Y-%m-%d"),
                selected_sale.revenue,
                selected_sale.cost,
                selected_sale.client_id,
                selected_sale.client_rating,
                selected_sale.client_comment,
            )
            for row, title, value in zip(range(7), titles, values):
                pady = (20, 0) if row == 0 else (0, 20) if row == len(titles) - 1 else 0
                ctk.CTkLabel(master=sale_frame, text=title).grid(row=row, column=0, padx=20, sticky="w", pady=pady)
                ctk.CTkLabel(master=sale_frame, text=str(value)).grid(row=row, column=1, sticky="e", padx=(0, 20), pady=pady)

        view_sale()

        display_list(
            _master=main_frame,
            options=tuple(f"{s.employee_id} - {s.client_id}" for s in all_sales),
            returned_idx=[sale_idx_select],
            place=(0, 0),
            colspan=1,
            err_msg="No sale to view",
            cmd=view_sale,
        )

    def __find_sale(self):
        # - 4 or 5 columns
        # 0: buttons to switch between search by <Sale ID>, <Client ID>, <Rating>, <Date>, <Employee ID> (admin only)
        # 1: the subframe for the selected search type

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        is_admin = the_company.logged_in_employee.is_admin
        types = (
            ("Sale ID", "Client ID", "Rating", "Date", "Employee ID")
            if is_admin
            else ("Sale ID", "Client ID", "Rating", "Date")
        )

        all_sales = (
            [s for e in the_company.employees for s in e.performance.sale_list]
            if is_admin
            else the_company.logged_in_employee.performance.sale_list
        )

        # region: create the buttons to switch between search types
        buttons_change_type = {}
        for idx, type in enumerate(types):
            buttons_change_type[type] = ctk.CTkButton(
                master=main_frame, text=type, command=lambda idx=idx: _change_search_type(idx), **btn_action_style
            )
            buttons_change_type[type].grid(row=0, column=idx, padx=(20, 0), pady=20)

        buttons_change_type[types[-1]].grid(padx=(20, 20))
        # endregion

        search_frame = ctk.CTkFrame(master=main_frame)
        search_frame.grid(row=1, column=0, pady=(0, 20), padx=20, columnspan=(5 if is_admin else 4))

        def _change_search_type(idx: int):
            nonlocal buttons_change_type, main_frame, types

            # enable all buttons except the one that was clicked
            for type in types:
                buttons_change_type[type].configure(state=(NORMAL if type != types[idx] else DISABLED))

            # remove all widgets from search frame
            for widget in search_frame.winfo_children():
                widget.destroy()

            # match types with idx, but types
            if types[idx] == "Sale ID":
                __find_sale_by_sale_id()
            else:
                __find_sale_by_everything_else(idx)

        def __find_sale_by_sale_id():
            # - 2 columns
            # 0: input sale/client id | search button
            # 1: sale info
            nonlocal search_frame, all_sales

            # create widgets
            input_sale_id = ctk.Variable(value="")
            ctk.CTkLabel(master=search_frame, text="Sale ID").grid(row=0, column=0, padx=20, sticky="w", pady=20)
            ctk.CTkEntry(master=search_frame, textvariable=input_sale_id).grid(
                row=0, column=1, sticky="e", padx=(0, 20), pady=20
            )

            def search_handler():
                nonlocal input_sale_id, search_frame, all_sales

                selected_sale = next(
                    (s for s in all_sales if (s.sale_id if type == 0 else s.client_id) == input_sale_id.get()), None
                )

                if selected_sale is None:
                    msgbox.showerror("Error", "Sale not found")
                    return

                msgbox.showinfo(
                    "Sale Info",
                    f"Employee ID: {selected_sale.employee_id}\n"
                    f"Date: {selected_sale.date}\n"
                    f"Revenue: {selected_sale.revenue}\n"
                    f"Cost: {selected_sale.cost}\n"
                    f"Client ID: {selected_sale.client_id}\n"
                    f"Client Rating: {selected_sale.client_rating}\n"
                    f"Client Comment: {selected_sale.client_comment}",
                )

            ctk.CTkButton(master=search_frame, text="Search", command=search_handler, **btn_action_style).grid(
                row=1, column=0, columnspan=2, pady=(0, 20), padx=20
            )

        def __find_sale_by_everything_else(idx: int):
            # - 3 columns
            # 0: input | search button
            # 1: select sale from the list of sales that match the search criteria, updated every time the input changes
            # 2: button to view selected sale
            nonlocal search_frame, all_sales

            # create widgets
            input_value = ctk.Variable(value="")
            labels = ("", "Client ID", "From 1.0 to 5.0 inclusive", "YYYY-MM-DD", "Employee ID")
            ctk.CTkLabel(master=search_frame, text=labels[idx]).grid(row=0, column=0, padx=20, sticky="w", pady=20)
            ctk.CTkEntry(master=search_frame, textvariable=input_value).grid(
                row=0, column=1, sticky="e", padx=(0, 20), pady=20
            )
            select_sale_frame = ctk.CTkBaseClass(None)
            sale_idx_select = ctk.IntVar(value=0)

            def search_handler():
                nonlocal input_value, search_frame, all_sales, sale_idx_select, select_sale_frame

                # filter out sales that don't match the search criteria
                filtered_sales = []
                for sale in all_sales:
                    match idx:
                        case 1:
                            if sale.client_id == input_value.get():
                                filtered_sales.append(sale)
                        case 2:
                            # input must between 1.0 and 5.0 inclusive
                            # if it's an integer, x, find sales with client_rating in range [x, x+1)
                            # if it's a float, x.y, find sales with that exact client_rating

                            # check invalid condition first
                            # not in form x.y
                            # x not in range [1, 5]
                            # x.y not in range [1.0, 5.0]
                            if (
                                not match(r"^\d(\.\d)?$", input_value.get())
                                or (match(r"^\d$", input_value.get()) and int(input_value.get()) not in range(1, 6))
                                or (
                                    match(r"^\d\.\d$", input_value.get())
                                    and (float(input_value.get()) < 1.0 or float(input_value.get()) > 5.0)
                                )
                            ):
                                continue

                            if match(r"^\d\.\d$", input_value.get()):
                                if sale.client_rating == float(input_value.get()):
                                    filtered_sales.append(sale)
                            elif match(r"^\d$", input_value.get()):
                                if int(input_value.get()) <= sale.client_rating < int(input_value.get()) + 1:
                                    filtered_sales.append(sale)
                        case 3:
                            if datetime.strftime(sale.date, "%Y-%m-%d") == input_value.get():
                                filtered_sales.append(sale)
                        case 4:
                            if sale.employee_id == input_value.get():
                                filtered_sales.append(sale)

                select_sale_frame.destroy()
                if len(filtered_sales) == 0:
                    return
                select_sale_frame = display_list(
                    _master=search_frame,
                    options=tuple(f"{s.sale_id} from client {s.client_id}" for s in filtered_sales),
                    returned_idx=[sale_idx_select],
                    place=(1, 0),
                    colspan=2,
                    err_msg="No sale to view",
                    pady=(0, 20),
                )

            # run the search_handler every time the input changes
            input_value.trace_add("write", lambda *args: search_handler())

            def view_sale_details_handler():
                # like from find sale by sale id
                nonlocal sale_idx_select, all_sales

                selected_sale = all_sales[sale_idx_select.get()]

                msgbox.showinfo(
                    "Sale Info",
                    f"Employee ID: {selected_sale.employee_id}\n"
                    f"Date: {datetime.strftime(selected_sale.date, '%Y-%m-%d')}\n"
                    f"Revenue: {selected_sale.revenue}\n"
                    f"Cost: {selected_sale.cost}\n"
                    f"Client ID: {selected_sale.client_id}\n"
                    f"Client Rating: {selected_sale.client_rating}\n"
                    f"Client Comment: {selected_sale.client_comment}",
                )

            ctk.CTkButton(
                master=search_frame, text="View sale details", command=view_sale_details_handler, **btn_action_style
            ).grid(row=2, column=0, columnspan=2, pady=(0, 20), padx=20)

    def __admin_view_sales_perf(self):
        # - 1 column
        # 0: select employee from the list of employees
        # 1: details of the selected employee (2 columns)

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        empl_idx_select = ctk.IntVar(value=0)

        detail_frame = ctk.CTkFrame(master=main_frame)

        def update_details_frame():
            nonlocal detail_frame, empl_idx_select
            selected_empl = the_company.employees[empl_idx_select.get()]
            perf = selected_empl.performance

            detail_frame.destroy()
            detail_frame = ctk.CTkFrame(master=main_frame)
            detail_frame.grid(row=1, column=0, pady=(0, 20), padx=20)

            labels = ("Employee ID", "Name", "Sales count", "Total Revenue", "Total Cost", "Total Profit", "Average Rating")
            values = (
                selected_empl.employee_id,
                selected_empl.name,
                perf.sales_count,
                perf.total_revenue,
                perf.total_cost,
                perf.total_profit,
                perf.average_rating,
            )
            for row, label, value in zip(range(len(labels)), labels, values):
                pady = (20, 0) if row == 0 else ((0, 20) if row == len(labels) - 1 else 0)
                ctk.CTkLabel(master=detail_frame, text=label).grid(row=row, column=0, sticky=W, pady=pady, padx=20)
                ctk.CTkLabel(master=detail_frame, text=str(value)).grid(row=row, column=1, sticky=E, pady=pady, padx=(0, 20))

        update_details_frame()

        display_list(
            _master=main_frame,
            options=tuple(f"{e.name} - {e.employee_id}" for e in the_company.employees),
            returned_idx=[empl_idx_select],
            place=(0, 0),
            colspan=1,
            err_msg="No employee to view",
            cmd=update_details_frame,
        )

    def __employee_view_sales_perf(self):
        # - 1 column
        # 0: details of the logged in employee (2 columns)

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        detail_frame = ctk.CTkFrame(master=main_frame)

        def update_details_frame():
            nonlocal detail_frame
            logged_in_empl = the_company.logged_in_employee
            perf = logged_in_empl.performance

            detail_frame.destroy()
            detail_frame = ctk.CTkFrame(master=main_frame)
            detail_frame.grid(row=1, column=0, pady=(0, 20), padx=20)

            labels = ("Employee ID", "Name", "Sales count", "Total Revenue", "Total Cost", "Total Profit", "Average Rating")
            values = (
                logged_in_empl.employee_id,
                logged_in_empl.name,
                perf.sales_count,
                perf.total_revenue,
                perf.total_cost,
                perf.total_profit,
                perf.average_rating,
            )
            for row, label, value in zip(range(len(labels)), labels, values):
                pady = (20, 0) if row == 0 else ((0, 20) if row == len(labels) - 1 else 0)
                ctk.CTkLabel(master=detail_frame, text=label).grid(row=row, column=0, sticky=W, pady=pady, padx=20)
                ctk.CTkLabel(master=detail_frame, text=str(value)).grid(row=row, column=1, sticky=E, pady=pady, padx=(0, 20))

        update_details_frame()
