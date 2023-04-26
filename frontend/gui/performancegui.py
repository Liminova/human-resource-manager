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
            # "Remove sale": self.__admin_remove_sale,
            # "View details of sale": self.__admin_view_sale,
            # "Find sale(s) by...	": self.__admin_find_sale,
            # "View sales performance	of all employees": self.__admin_view_sales_perf,
            "Back": self.__back_to_homepage,
        }

    def employee(self):
        return {
            # "View sales performance": self.__employee_view_sales_perf,
            # "View info about a sale": self.__employee_view_sale,
            # "Find sale(s) by...": self.__employee_find_sale,
            "Back": self.__back_to_homepage
        }

    def __clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def __back_to_homepage(self):
        from .homepage import Homepage

        self.destroy()
        Homepage().mainloop()

    def __admin_add_sale(self):
        # 0: table to choose empl
        # input: 1: empl id
        #        2. revenue
        #        3. cost
        #        4. client id
        #        5. client rating
        #        6. client comment
        # 7: confirm button

        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        # region: variables
        _empl_idx_select = tkinter.IntVar()
        # endregion

        entries = [ctk.CTkEntry(master=main_frame) for _ in range(7)]
        labels = ("Employee ID", "Revenue", "Cost", "Client ID", "Client rating (1-5)", "Client comment")
        placeholders = ("abcxyz", "1000000", "500000", "123", "5", "Good")
        for row, entry, lable, placeholder in zip(range(7), entries, labels, placeholders):
            ctk.CTkLabel(master=main_frame, text=lable, **label_desc_style).grid(row=row, column=0, pady=10)
            entry.configure(placeholder_text=placeholder, **input_box_style)
            entry.grid(row=row, column=1, pady=10)

        # region: select an employee
        display_list(
            _master=main_frame,
            options=tuple(f"{e.name} - {e.employee_id}" for e in the_company.employees),
            returned_idx=[_empl_idx_select],
            selectable=True,
            err_msg="No employee yet",
            colspan=1,
        )
        # endregion

        # region: confirm button
        btn_submit = ctk.CTkButton(master=main_frame, text="Add", **btn_action_style)

        def _add_sale_handler():
            nonlocal _empl_idx_select, entries
            values = [e.get().strip() for e in entries]
            if not all(values):
                msgbox.showerror("Error", "Please fill in all fields")
                return
            _empl = the_company.employees[_empl_idx_select.get()]

            new_sale = Sale()
            for setter, value in zip(
                (
                    new_sale.set_revenue,
                    new_sale.set_cost,
                    new_sale.set_client_id,
                    new_sale.set_client_rating,
                    new_sale.set_client_comment,
                ),
                values[1:],
            ):
                setter(value).unwrap()

            new_sale.employee_id = _empl.employee_id
            new_sale.employee_name = _empl.name
            new_sale.profit = float(new_sale.revenue) - float(new_sale.cost)
            _empl.performance.add_sale(new_sale)

            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.update_one({"_id": _empl.id}, {"$set": _empl.dict(include={"performance"})}, upsert=True)

            msgbox.showinfo("Success", "Sale added successfully")

        btn_submit.configure(command=_add_sale_handler)
        # endregion

        button2_frame = ctk.CTkFrame(master=self.right_frame)
        ctk.CTkLabel(master=button2_frame, text="Sales performance", **label_title_style).pack()

        ctk.CTkLabel(
            master=self.right_frame, text="Enter numerical order of employee you want to choose: ", **label_desc_style
        ).place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
        self.entry = ctk.CTkEntry(master=self.right_frame, **input_box_style)
        self.entry.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        self.entry3 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter cost")
        self.__input_box_style(self.entry3)
        self.entry3.place(relx=0.325, rely=0.395, anchor=tkinter.CENTER)

        self.label4 = ctk.CTkLabel(master=self.right_frame, text="Profit: ", font=("Century Gothic", 20, "italic"))
        self.label4.place(relx=0.1, rely=0.45, anchor=tkinter.CENTER)

        self.entry4 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter profit")
        self.__input_box_style(self.entry4)
        self.entry4.place(relx=0.325, rely=0.495, anchor=tkinter.CENTER)

        self.label5 = ctk.CTkLabel(master=self.right_frame, text="Client ID: ", font=("Century Gothic", 20, "italic"))
        self.label5.place(relx=0.1, rely=0.55, anchor=tkinter.CENTER)

        self.entry5 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter client ID")
        self.__input_box_style(self.entry5)
        self.entry5.place(relx=0.325, rely=0.595, anchor=tkinter.CENTER)

        self.label6 = ctk.CTkLabel(master=self.right_frame, text="Client rating: ", font=("Century Gothic", 20, "italic"))
        self.label6.place(relx=0.1, rely=0.65, anchor=tkinter.CENTER)

        self.entry6 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter client rating")
        self.__input_box_style(self.entry6)
        self.entry6.place(relx=0.325, rely=0.695, anchor=tkinter.CENTER)

        self.label7 = ctk.CTkLabel(master=self.right_frame, text="Client comment: ", font=("Century Gothic", 20, "italic"))
        self.label7.place(relx=0.1, rely=0.75, anchor=tkinter.CENTER)

        self.entry7 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter client comment")
        self.__input_box_style(self.entry7)
        self.entry7.place(relx=0.325, rely=0.795, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="Confirm", command=lambda self=self: add_successfully(self))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        self.button1_frame.pack(pady=20)

        def add_successfully(self):
            employee_id = self.entry1.get()
            employee_name = [e for e in the_company.employees if e.employee_id == employee_id][0].name
            date = datetime.now()
            revenue = self.entry2.get()
            cost = self.entry3.get()
            profit = self.entry4.get()
            client_id = self.entry5.get()
            client_rating = self.entry6.get()
            client_comment = self.entry7.get()
            sale_id = str(client_id) + str(employee_id) + str(datetime.now().strftime("%Y%m%d%H%M%S"))

            # check if employee_id is valid
            if len([e for e in the_company.employees if e.employee_id == employee_id]) == 0:
                msgbox.showerror("Error", "Invalid employee ID")
                return

            sale = Sale()
            sale.sale_id = sale_id
            sale.employee_id = employee_id
            sale.employee_name = employee_name
            sale.date = date
            sale.revenue = revenue
            sale.cost = cost
            sale.profit = profit
            sale.client_id = client_id
            sale.client_rating = client_rating
            sale.client_comment = client_comment

            the_company.logged_in_employee.performance.sale_list.append(sale)
            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.update_one(
                    {"_id": [e for e in the_company.employees if e.employee_id == employee_id][0].id},
                    {"$set": [e for e in the_company.employees if e.employee_id == employee_id][0].dict(include={"performance"})},
                    upsert=True,
                )

    def __view_sales_performance(self):
        self.button2_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button2_frame, text="Sales performance", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.button = ctk.CTkButton(
            master=self.right_frame, text="View", font=("Century Gothic", 20, "bold"), command=lambda self=self: view_sales_performance(self)
        )
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        self.button2_frame.pack(pady=20)

        def view_sales_performance(self):
            pass

    def __remove_sale(self):
        self.button3_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button3_frame, text="Remove sale", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.button = ctk.CTkButton(master=self.right_frame, text="Remove sale", font=("Century Gothic", 20, "bold"))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        self.button3_frame.pack(pady=20)

    def __get_sale_info(self):
        self.button4_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button4_frame, text="Get sale info", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.button = ctk.CTkButton(master=self.right_frame, text="Get sale info", font=("Century Gothic", 20, "bold"))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        self.button4_frame.pack(pady=20)

    def __find_sale_by(self):
        self.button5_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button5_frame, text="Find sale by", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.button = ctk.CTkButton(master=self.right_frame, text="Find", font=("Century Gothic", 20, "bold"))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        self.button5_frame.pack(pady=20)


if __name__ == "__main__":
    app = PerformanceGui()
    app.mainloop()
