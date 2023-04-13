import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
import homepage

from models.performance import Performance, Sale
from models.company import Company

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class PerformanceUI:
    def __init__(self, company: Company) -> None:
        self.__company = company
        self.employees = self.__company.employees
        self.selection: Employee = None

    def start(self):
        self.root = ctk.CTk()
        self.root.title("Performance")
        self.root.geometry("925x600")
        self.root.resizable(True, True)

        self.frame = ctk.CTkFrame(master=self.root, width=320, height=360, corner_radius=20, border_width=2)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        # self.frame.pack(expand=True, padx=20, pady=20)

        self.title_label = ctk.CTkLabel(master=self.frame, text="Performance menu", font=('Century Gothic', 30))
        self.title_label.place(x=25, y=10)
        

        self.main_menu = [("Add sale", self.add_sale),
                          ("View sales performance", self.view_sales),
                          ("Remove sale", self.remove_sale),
                        #   ("Get sale info", self.get_sale_info),
                          ("Exit", self.exit)]
                          



        self.buttons = []
        for text, command in self.main_menu:
            button = ctk.CTkButton(master=self.frame, width=220, text=text, command=command, corner_radius=6, font=('Century Gothic',16))
            button.place(x=50, y=80 + len(self.buttons) * 55)
            self.buttons.append(button)
        

        self.root.mainloop()

    def select_employee(self): # select an employee to manage performance 
        
        # if len(self.employees) == 0:
        #     messagebox.showerror("Error", "No employees to manage performance, please add an employee first!")
            

        # employee_items = [f"{employee.name} ({employee.id})" for employee in self.employees]
        employee_items = ["H (001)", "R (002)", "A (003)"]

        window = ctk.CTk()
        window.title("Select employee")
        window.geometry("500x500")
        window.resizable(True, True)

        frame = ctk.CTkFrame(master=window, width=320, height=200, corner_radius=20, border_width=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = ctk.CTkLabel(master=frame, text="Select employee", font=('Century Gothic', 30))
        title_label.place(x=40, y=10)

        entry1 = ctk.CTkEntry(master=frame, width=220, corner_radius=6, font=('Century Gothic',16), placeholder_text="Name")
        entry1.place(x=50, y=60)

        entry2 = ctk.CTkEntry(master=frame, width=220, corner_radius=6, font=('Century Gothic',16), placeholder_text="ID")
        entry2.place(x=50, y=110)
        

        def click_ok():
            employee_selected_name = entry1.get()
            employee_selected_id = entry2.get()
            for employee in employee_items:
                if employee_selected_name == employee.name and employee_selected_id == employee.id:
                    self.selection = employee 
                    messagebox.showinfo("Success", f"Employee {self.selection.name, self.selection.id} selected!")
                    window.destroy()
                    self.start()
                    break
                    
            else:
                messagebox.showerror("Error", "Employee not found! Enter again!")


        button1 = ctk.CTkButton(master=frame, width=220, text="OK", command=click_ok, corner_radius=6, font=('Century Gothic',16))
        button1.place(x=50, y=160)
            
        window.mainloop()


        

    def add_sale(self):
        # create a new empty sale object
        sale = Sale()

        add_sale_window = ctk.CTk()
        add_sale_window.title("Add sale")
        add_sale_window.geometry("700x600")
        add_sale_window.resizable(True, True)

        frame = ctk.CTkFrame(master=add_sale_window, width=320, height=450, corner_radius=20, border_width=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = ctk.CTkLabel(master=frame, text="Add sale", font=('Century Gothic', 30))
        title_label.place(x=100, y=10)

        entry1 = ctk.CTkEntry(master=frame, width=220, corner_radius=6, font=('Century Gothic',16), placeholder_text="Sale ID")
        entry1.place(x=50, y=60)

        entry2 = ctk.CTkEntry(master=frame, width=220, corner_radius=6, font=('Century Gothic',16), placeholder_text="Revenue")
        entry2.place(x=50, y=110)

        entry3 = ctk.CTkEntry(master=frame, width=220, corner_radius=6, font=('Century Gothic',16), placeholder_text="Cost")
        entry3.place(x=50, y=160)

        entry4 = ctk.CTkEntry(master=frame, width=220, corner_radius=6, font=('Century Gothic',16), placeholder_text="Profit")
        entry4.place(x=50, y=210)

        entry5 = ctk.CTkEntry(master=frame, width=220, corner_radius=6, font=('Century Gothic',16), placeholder_text="Client ID")
        entry5.place(x=50, y=260)

        entry6 = ctk.CTkEntry(master=frame, width=220, corner_radius=6, font=('Century Gothic',16), placeholder_text="Client rating")
        entry6.place(x=50, y=310)

        entry7 = ctk.CTkEntry(master=frame, width=220, corner_radius=6, font=('Century Gothic',16), placeholder_text="Client comment")
        entry7.place(x=50, y=360)

        def click():
            sale.id = entry1.get()
            sale.revenue = entry2.get()
            sale.cost = entry3.get()
            sale.profit = entry4.get()
            sale.client_id = entry5.get()
            sale.client_rating = entry6.get()
            sale.client_comment = entry7.get()
            # add the sale to the employee's performance
            self.selection.performance.sale_list.append(sale)
            self.selection.performance.add_sale(sale)
            messagebox.showinfo("Success", f"Sale {sale.id} added!")
            add_sale_window.destroy()
            self.start()        

        button1 = ctk.CTkButton(master=frame, width=220, text="OK", command=click, corner_radius=6, font=('Century Gothic',16))
        button1.place(x=50, y=410)



        add_sale_window.mainloop()

        
    def view_sales(self):
        # display all sales for the selected employee
        view_sales_window = ctk.CTk()
        view_sales_window.title("View sales")
        view_sales_window.geometry("700x600")
        view_sales_window.resizable(True, True)

        frame = ctk.CTkFrame(master=view_sales_window, width=320, height=450, corner_radius=20, border_width=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = ctk.CTkLabel(master=frame, text="View sales", font=('Century Gothic', 30))
        title_label.place(x=100, y=10)

        sale_list = self.selection.performance.sale_list
        sale_items = [f"{sale.id} ({sale.revenue}, {sale.cost}, {sale.profit}, {sale.client_id}, {sale.client_rating}, {sale.client_comment})" for sale in sale_list]

        
        

        def click():
            print(sale_items)
            view_sales_window.destroy()        

        button1 = ctk.CTkButton(master=frame, width=220, text="OK", command=click, corner_radius=6, font=('Century Gothic',16))
        button1.place(x=50, y=410)

        view_sales_window.mainloop()

    def remove_sale(self):
        sale_list = self.selection.performance.sale_list
        sale_items = [f"{sale.id} ({sale.revenue}, {sale.cost}, {sale.profit}, {sale.client_id}, {sale.client_rating}, {sale.client_comment})" for sale in sale_list]

        remove_sale_window = ctk.CTk()
        remove_sale_window.title("Remove sale")
        remove_sale_window.geometry("500x500")
        remove_sale_window.resizable(True, True)

        frame = ctk.CTkFrame(master=remove_sale_window, width=320, height=200, corner_radius=20, border_width=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = ctk.CTkLabel(master=frame, text="Remove sale", font=('Century Gothic', 30))
        title_label.place(x=100, y=10)

        entry1 = ctk.CTkEntry(master=frame, width=220, corner_radius=6, font=('Century Gothic',16), placeholder_text="Index of sale to remove")
        entry1.place(x=50, y=60)
        idx = entry1.get()

        button1 = ctk.CTkButton(master=frame, width=220, text="OK", command=click, corner_radius=6, font=('Century Gothic',16))
        button1.place(x=50, y=110)

        def click():
            del self.selection.performance.sale_list[idx]
            messagebox.showinfo("Success", f"Sale {idx} removed successfully!")
            remove_sale_window.destroy()
    
    def get_sale_info(self):
        pass
    
    
    def exit(self):
        self.root.destroy()
        homepage.homepage().run()