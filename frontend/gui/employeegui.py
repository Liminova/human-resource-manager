import customtkinter as ctk
import tkinter
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

Width = 1280
Height = 750

class employeegui(ctk.CTk):
    def __init__(self, master = None):
        super().__init__()

        self.title("Employee Management")
        self.geometry(f"{Width}x{Height}")
        self.resizable(True, True)

        self.frame1 = ctk.CTkFrame(master=self, width=325, height=700, corner_radius=10)
        self.frame1.pack(padx = 10, pady = 10, side = tkinter.LEFT)

        self.label = ctk.CTkLabel(master=self.frame1, text="Index", font=("Century Gothic", 25, "bold"))
        self.label.place(relx=0.5, rely=0.085, anchor=tkinter.CENTER)

        def button_size(button):
            button.configure(width=260, height=40, font=("Century Gothic", 16), corner_radius=10)

        # Bind the button1 to frame3
        self.button1 = ctk.CTkButton(master=self.frame1, text="Add Employee", command=self.add_employee)
        button_size(self.button1)
        self.button1.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(master=self.frame1, text="Remove Employee")
        button_size(self.button2)
        self.button2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.button3 = ctk.CTkButton(master=self.frame1, text="Update Employee")
        button_size(self.button3)
        self.button3.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        self.button4 = ctk.CTkButton(master=self.frame1, text="View Employee")
        button_size(self.button4)
        self.button4.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.button5 = ctk.CTkButton(master=self.frame1, text="View All Employees")
        button_size(self.button5)
        self.button5.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        self.button6 = ctk.CTkButton(master=self.frame1, text="Back", fg_color="blue", command=self.back_to_homepage)
        button_size(self.button6)
        self.button6.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

    # Create second frame
        self.frame2 = ctk.CTkFrame(master=self, width=900, height=700, corner_radius=10)
        self.frame2.pack(padx = 10, pady = 10, side = tkinter.RIGHT)

    # Display on the second frame
        self.label = ctk.CTkLabel(master=self.frame2, text="Employee Management", font=("Century Gothic", 25, "bold"))
        self.label.place(relx=0.5, rely=0.045, anchor=tkinter.CENTER)

    def add_employee(self):
        import addemployee
        addemployee.addemployee().run()   

    def remove_employee(self):
        pass

    def update_employee(self):
        pass

    def view_employee(self):
        pass

    def view_all_employees(self):
        pass
    
    def back_to_homepage(self):
        import homepage
        self.destroy()
        homepage.homepage().run()

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = employeegui()
    app.mainloop()



