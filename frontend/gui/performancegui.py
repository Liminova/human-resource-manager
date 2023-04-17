import os
import tkinter
import customtkinter as ctk
from tkinter import messagebox as msgbox
from frontend.helpers import merge_callable
from models import Company, Sale
from datetime import datetime
from database.mongo import employee_repo

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

        def button_size(button):
            button.configure(width=260, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10)

        self.button1 = ctk.CTkButton(master=self.left_frame, text="Add Sale", command=merge_callable(self.__destroy_all_frames, self.__add_sale))
        button_size(self.button1)
        self.button1.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(
            master=self.left_frame, text="View Sales Performance", command=merge_callable(self.__destroy_all_frames, self.__view_sales_performance)
        )
        button_size(self.button2)
        self.button2.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

        self.button3 = ctk.CTkButton(
            master=self.left_frame, text="Remove Sale", command=merge_callable(self.__destroy_all_frames, self.__remove_sale)
        )
        button_size(self.button3)
        self.button3.place(relx=0.5, rely=0.35, anchor=tkinter.CENTER)

        self.button4 = ctk.CTkButton(
            master=self.left_frame, text="Get Sale Info", command=merge_callable(self.__destroy_all_frames, self.__get_sale_info)
        )
        button_size(self.button4)
        self.button4.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

        self.button5 = ctk.CTkButton(
            master=self.left_frame, text="Find Sale By", command=merge_callable(self.__destroy_all_frames, self.__find_sale_by)
        )
        button_size(self.button5)
        self.button5.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

        self.button6 = ctk.CTkButton(master=self.left_frame, text="Back", fg_color="red", command=self._back_to_homepage)
        self.button6.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="red")
        self.button6.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        self.left_frame.pack(side=ctk.LEFT)
        self.left_frame.pack_propagate(False)
        self.left_frame.configure(width=320, height=760)

        self.right_frame = ctk.CTkFrame(master=self, border_width=2, corner_radius=10)
        self.right_frame.pack(side=ctk.RIGHT)
        self.right_frame.pack_propagate(False)
        self.right_frame.configure(width=700, height=760)

    def __destroy_all_frames(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def __back_to_homepage(self):
        from .homepage import Homepage

        self.destroy()
        Homepage().mainloop()

    def __input_box_style(self, element):
        element.configure(width=400, height=30, font=("Century Gothic", 14), corner_radius=10)

    def __add_sale(self):
        self.button1_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button1_frame, text="Information", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="ID: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.1, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter employee's ID")
        self.__input_box_style(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.label2 = ctk.CTkLabel(master=self.right_frame, text="Revenue: ", font=("Century Gothic", 20, "italic"))
        self.label2.place(relx=0.1, rely=0.25, anchor=tkinter.CENTER)

        self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter revenue")
        self.__input_box_style(self.entry2)
        self.entry2.place(relx=0.325, rely=0.295, anchor=tkinter.CENTER)

        self.label3 = ctk.CTkLabel(master=self.right_frame, text="Cost: ", font=("Century Gothic", 20, "italic"))
        self.label3.place(relx=0.1, rely=0.35, anchor=tkinter.CENTER)

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
