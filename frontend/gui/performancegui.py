import os
import tkinter
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox as msgbox

from models import Company, Sale
from database.mongo import employee_repo
from frontend.helpers_gui import *
from frontend.helpers_gui.global_styling import *

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
            "View details of sale": self.__admin_view_sale,
            # "Find sale(s) by...	": self.__admin_find_sale, # DEO BIET
            # "View sales performance	of all employees": self.__admin_view_sales_perf, # DEO BIET
            "Back": self.__back_to_homepage,
        }

    def employee(self):
        return {
            # "View sales performance": self.__employee_view_sales_perf, # DEO BIET
            # "View info about a sale": self.__employee_view_sale, # BO DI BAN OI
            # "Find sale(s) by...": self.__employee_find_sale, # BO DI BAN OI
            "Back": self.__back_to_homepage
        }

    def __clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def __back_to_homepage(self):
        from .homepage import Homepage

        self.destroy()
        Homepage().mainloop()

    # region: admin functions

    def __admin_add_sale(self):
        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        entries = [ctk.CTkEntry(master=main_frame) for _ in range(5)]
        labels = ("Revenue: ", "Cost: ", "Client ID: ", "Client rating: ", "Client comment: ")
        placeholders = ("100", "50", "123", "5", "Pas mal")
        for row, entry, label, placeholder in zip(range(1, 6), entries, labels, placeholders):
            ctk.CTkLabel(master=main_frame, text=label, **label_desc_style).grid(
                row=row, column=0, pady=(20, 0), padx=20, sticky="w"
            )
            entry.configure(placeholder_text=placeholder, **input_box_style)
            entry.grid(row=row, column=1, pady=(20, 0), padx=(0, 20))

        def _add_sale():
            _employee = the_company.logged_in_employee
            _sale = Sale(
                employee_id=_employee.employee_id,
                date=datetime.now(),
                revenue=int(entries[0].get()),
                cost=int(entries[1].get()),
                client_id=(entries[2].get()),
                client_rating=int(entries[3].get()),
                client_comment=entries[4].get(),
            )
            _employee.performance.sale_list.append(_sale)

            # update employee in db
            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.update_one(
                    {"_id": _employee.id}, {"$set": _employee.dict(include={"performance"})}, upsert=True
                )
            msgbox.showinfo("Success", "Sale added successfully")
            merge_callable(self.__clear_right_frame, self.__admin_add_sale)()

        ctk.CTkButton(master=main_frame, text="Add sale", command=_add_sale, **btn_action_style).grid(
            row=6, column=0, columnspan=2, pady=(20, 0)
        )

    def __admin_remove_sale(self):
        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        # Select a sale from list
        radio_sale_idx_select: ctk.Variable = ctk.IntVar(value=0)
        sale_items = tuple(
            f"{s.employee_id} - {s.client_id}" for e in the_company.employees for s in e.performance.sale_list
        )
        _display_list = display_list(
            _master=main_frame, options=sale_items, returned_idx=[radio_sale_idx_select], selectable=True
        )
        if _display_list[0] is False:
            ctk.CTkLabel(master=main_frame, text="No sale to remove", **label_desc_style).grid(
                row=1, column=0, columnspan=2, pady=(20, 0)
            )

        def _remove_sale():
            if not msgbox.askyesno("Confirm", "Are you sure you want to remove this sale?"):
                return
            _sales = [s for e in the_company.employees for s in e.performance.sale_list]
            _sale = _sales[radio_sale_idx_select.get()]

            _employee = [e for e in the_company.employees if e.employee_id == _sale.employee_id][0]

            # remove sale from employee
            _employee.performance.sale_list.remove(_sale)

            # update employee in db
            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.update_one(
                    {"_id": _employee.id}, {"$set": _employee.dict(include={"performance"})}, upsert=True
                )
            msgbox.showinfo("Success", "Sale removed successfully")
            merge_callable(self.__clear_right_frame, self.__admin_remove_sale)()

        ctk.CTkButton(master=main_frame, text="Remove", command=_remove_sale, **btn_action_style).grid(
            row=2, column=0, columnspan=2, pady=(20, 0)
        )

    def __admin_view_sale(self):
        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        sale_frame = ctk.CTkFrame(None)

        # Select a sale from list
        radio_sale_idx_select: ctk.Variable = ctk.IntVar(value=0)
        sale_items = tuple(
            f"{s.employee_id} - {s.client_id}" for e in the_company.employees for s in e.performance.sale_list
        )
        _display_list = display_list(
            _master=main_frame, options=sale_items, returned_idx=[radio_sale_idx_select], selectable=True
        )
        if _display_list[0] is False:
            ctk.CTkLabel(master=main_frame, text="No sale to view", **label_desc_style).grid(
                row=1, column=0, columnspan=2, pady=(20, 0)
            )

        def _view_sale():
            nonlocal radio_sale_idx_select, sale_frame, main_frame
            _sales = [s for e in the_company.employees for s in e.performance.sale_list]
            _sale = _sales[radio_sale_idx_select.get()]

            sale_frame.destroy()
            sale_frame = ctk.CTkFrame(master=main_frame)
            sale_frame.grid(row=1, column=0, columnspan=2, pady=(0, 15), padx=20)

            titles = ("Employee ID", "Date", "Revenue", "Cost", "Client ID", "Client Rating", "Client Comment")
            values = (
                _sale.employee_id,
                _sale.date,
                _sale.revenue,
                _sale.cost,
                _sale.client_id,
                _sale.client_rating,
                _sale.client_comment,
            )
            for row, title, value in zip(range(7), titles, values):
                ctk.CTkLabel(master=sale_frame, text=title).grid(row=row, column=0, padx=20, sticky="w")
                ctk.CTkLabel(master=sale_frame, text=str(value)).grid(row=row, column=1, sticky="e", padx=(20, 0))

        _view_sale()

        _sale_select_frame = display_list(
            _master=main_frame,
            options=sale_items,
            returned_idx=[radio_sale_idx_select],
            selectable=True,
            place_col=0,
            place_row=0,
            colspan=1,
            cmd=_view_sale,
        )

        if _sale_select_frame[0] is False:
            ctk.CTkLabel(master=main_frame, text="No sale to view", **label_desc_style).grid(
                row=1, column=0, columnspan=2, pady=(20, 0)
            )

    # endregion

    # region: employee functions

    # endregion

    # BYE
