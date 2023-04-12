import customtkinter
from customtkinter import *
from models import BenefitPlan
from typing import List, Tuple, Callable, Any

class BenefitGUI(ctk.CTk):
    def __init__(self, master = None):
        super().__init__()

        self.title("Benefit Plan Management")
        self.geometry(f"{Width}x{Height}")
        self.resizable(True, True)

        self.frame1 = ctk.CTkFrame(master=self, width=325, height=700, corner_radius=10)
        self.frame1.pack(padx = 10, pady = 10, side = tkinter.LEFT)

        self.label = ctk.CTkLabel(master=self.frame1, text="Index", font=("Century Gothic", 25, "bold"))
        self.label.place(relx=0.5, rely=0.085, anchor=tkinter.CENTER)

        def button_size(button):
            button.configure(width=260, height=40, font=("Century Gothic", 16), corner_radius=10)

        # Bind the button1 to frame3
        self.button1 = ctk.CTkButton(master=self.frame1, text="Add Benefit Plan", command=self.add_benefit_plan)
        button_size(self.button1)
        self.button1.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(master=self.frame1, text="Remove Benefit Plan")
        button_size(self.button2)
        self.button2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.button3 = ctk.CTkButton(master=self.frame1, text="Update Benefit Plan")
        button_size(self.button3)
        self.button3.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        self.button4 = ctk.CTkButton(master=self.frame1, text="View Benefit Plan")
        button_size(self.button4)
        self.button4.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.button5 = ctk.CTkButton(master=self.frame1, text="Apply benefit plan to employee")
        button_size(self.button5)
        self.button5.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        self.button6 = ctk.CTkButton(master=self.frame1, text="Exit")
        button_size(self.button6)
        self.button6.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        # Create second frame
        self.frame2 = ctk.CTkFrame(master=self, width=900, height=700, corner_radius=10)
        self.frame2.pack(padx = 10, pady = 10, side = tkinter.RIGHT)

        # Display on the second frame
        self.label = ctk.CTkLabel(master=self.frame2, text="Benefit Plan Management", font=("Century Gothic", 25, "bold"))
        self.label.place(relx=0.5, rely=0.045, anchor=tkinter.CENTER)

        # add benefit plan
        def add_benefit_plan(self):
            self.frame3 = ctk.CTkFrame(master=self.frame2, width=900, height=700, corner_radius=10)
            self.frame3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Add Benefit Plan", font=("Century Gothic", 25, "bold"))
            self.label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Benefit Plan Name", font=("Century Gothic", 20, "bold"))
            self.label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

            self.entry = ctk.CTkEntry(master=self.frame3, width=30, font=("Century Gothic", 20))
            self.entry.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Benefit Plan Description", font=("Century Gothic", 20, "bold"))
            self.label.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

            self.entry = ctk.CTkEntry(master=self.frame3, width=30, font=("Century Gothic", 20))
            self.entry.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Add", command=self.add)
            self.button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Back", command=self.back)
            self.button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        # remove benefit plan
        def remove_benefit_plan(self):
            self.frame3 = ctk.CTkFrame(master=self.frame2, width=900, height=700, corner_radius=10)
            self.frame3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Remove Benefit Plan", font=("Century Gothic", 25, "bold"))
            self.label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Benefit Plan Name", font=("Century Gothic", 20, "bold"))
            self.label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

            self.entry = ctk.CTkEntry(master=self.frame3, width=30, font=("Century Gothic", 20))
            self.entry.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Remove", command=self.remove)
            self.button.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Back", command=self.back)
            self.button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # update benefit plan
        def update_benefit_plan(self):
            self.frame3 = ctk.CTkFrame(master=self.frame2, width=900, height=700, corner_radius=10)
            self.frame3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Update Benefit Plan", font=("Century Gothic", 25, "bold"))
            self.label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Benefit Plan Name", font=("Century Gothic", 20, "bold"))
            self.label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

            self.entry = ctk.CTkEntry(master=self.frame3, width=30, font=("Century Gothic", 20))
            self.entry.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Update", command=self.update)
            self.button.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Back", command=self.back)
            self.button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # view benefit plan
        def view_benefit_plan(self):
            self.frame3 = ctk.CTkFrame(master=self.frame2, width=900, height=700, corner_radius=10)
            self.frame3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="View Benefit Plan", font=("Century Gothic", 25, "bold"))
            self.label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Benefit Plan Name", font=("Century Gothic", 20, "bold"))
            self.label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

            self.entry = ctk.CTkEntry(master=self.frame3, width=30, font=("Century Gothic", 20))
            self.entry.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="View", command=self.view)
            self.button.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Back", command=self.back)
            self.button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # add benefit plan
        def add(self):
            pass

        # remove benefit plan
        def remove(self):
            pass

        # update benefit plan
        def update(self):
            pass

        # view benefit plan
        def view(self):
            pass

        # back
        def back(self):
            self.frame3.destroy()

if __name__ == "__main__":
    app = BenefitGUI()
    app.mainloop()



