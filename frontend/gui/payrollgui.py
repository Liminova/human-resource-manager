class PayrollGUI(ctk.CTk):
    def __init__(self, master = None):
        super().__init__()
        self.title("Payroll Management")
        self.geometry(f"{Width}x{Height}")
        self.resizable(True, True)

        self.frame1 = ctk.CTkFrame(master=self, width=325, height=700, corner_radius=10)
        self.frame1.pack(padx = 10, pady = 10, side = tkinter.LEFT)

        self.label = ctk.CTkLabel(master=self.frame1, text="Index", font=("Century Gothic", 25, "bold"))
        self.label.place(relx=0.5, rely=0.085, anchor=tkinter.CENTER)

        def button_size(button):
            button.configure(width=260, height=40, font=("Century Gothic", 16), corner_radius=10)

        # Bind the button1 to frame3
        self.button1 = ctk.CTkButton(master=self.frame1, text="Create Payroll", command=self.add_payroll)
        button_size(self.button1)
        self.button1.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(master=self.frame1, text="Update Payroll")
        button_size(self.button2)
        self.button2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.button3 = ctk.CTkButton(master=self.frame1, text="Back")
        button_size(self.button2)
        self.button2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        # create second frame
        self.frame2 = ctk.CTkFrame(master=self, width=900, height=700, corner_radius=10)
        self.frame2.pack(padx = 10, pady = 10, side = tkinter.RIGHT)

        # display on second frame
        self.label = ctk.CTkLabel(master=self.frame2, text="Payroll Management", font=("Century Gothic", 25, "bold"))
        self.label.place(relx=0.5, rely=0.085, anchor=tkinter.CENTER)

        def create_payroll(self):
            self.frame3 = ctk.CTkFrame(master=self.frame2, width=900, height=700, corner_radius=10)
            self.frame3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Create Payroll", font=("Century Gothic", 25, "bold"))
            self.label.place(relx=0.5, rely=0.085, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Employee ID", font=("Century Gothic", 16))
            self.label.place(relx=0.2, rely=0.2, anchor=tkinter.CENTER)

            self.entry1 = ctk.CTkEntry(master=self.frame3, width=30)
            self.entry1.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Employee Name", font=("Century Gothic", 16))
            self.label.place(relx=0.2, rely=0.3, anchor=tkinter.CENTER)

            self.entry2 = ctk.CTkEntry(master=self.frame3, width=30)
            self.entry2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Basic Salary", font=("Century Gothic", 16))
            self.label.place(relx=0.2, rely=0.4, anchor=tkinter.CENTER)

            self.entry3 = ctk.CTkEntry(master=self.frame3, width=30)
            self.entry3.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Bonus", font=("Century Gothic", 16))
            self.label.place(relx=0.2, rely=0.5, anchor=tkinter.CENTER)

            self.entry4 = ctk.CTkEntry(master=self.frame3, width=30)
            self.entry4.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Tax", font=("Century Gothic", 16))
            self.label.place(relx=0.2, rely=0.5, anchor=tkinter.CENTER)

            self.entry5 = ctk.CTkEntry(master=self.frame3, width=30)
            self.entry5.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Punishment", font=("Century Gothic", 16))
            self.label.place(relx=0.2, rely=0.6, anchor=tkinter.CENTER)

        def update_payroll(self):
            self.frame3 = ctk.CTkFrame(master=self.frame2, width=900, height=700, corner_radius=10)
            self.frame3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Update Payroll", font=("Century Gothic", 25, "bold"))
            self.label.place(relx=0.5, rely=0.085, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Employee ID", font=("Century Gothic", 16))
            self.label.place(relx=0.2, rely=0.2, anchor=tkinter.CENTER)

            self.entry1 = ctk.CTkEntry(master=self.frame3, width=30)
            self.entry1.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Employee Name", font=("Century Gothic", 16))
            self.label.place(relx=0.2, rely=0.3, anchor=tkinter.CENTER)

            self.entry2 = ctk.CTkEntry(master=self.frame3, width=30)
            self.entry2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Basic Salary", font=("Century Gothic", 16))
            self.label.place(relx=0.2, rely=0.4, anchor=tkinter.CENTER)

            self.entry3 = ctk.CTkEntry(master=self.frame3, width=30)
            self.entry3.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Bonus", font=("Century Gothic", 16))
            self.label.place(relx=0.2, rely=0.5, anchor=tkinter.CENTER)

            self.entry4 = ctk.CTkEntry(master=self.frame3, width=30)
            self.entry4.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Tax", font=("Century Gothic", 16))
            self.entry4.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Punishment", font=("Century Gothic", 16))
            self.label.place(relx=0.2, rely=0.6, anchor=tkinter.CENTER)

            self.entry5 = ctk.CTkEntry(master=self.frame3, width=30)
            self.entry5.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        def back(self):
            self.frame3.destroy()

    if __name__ == "__main__":
        root = tkinter.Tk()
        root.title("Payroll Management System")
        root.geometry("1200x800")
        root.resizable(False, False)
        app = Payroll(root)
        root.mainloop()



