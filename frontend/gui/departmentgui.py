class DepartmentGUI(ctk.CTk):
    def __init__(self, master = None):
        super().__init__()
        self.title("Department Management")
        self.geometry(f"{Width}x{Height}")
        self.resizable(True, True)

        self.frame1 = ctk.CTkFrame(master=self, width=325, height=700, corner_radius=10)
        self.frame1.pack(padx = 10, pady = 10, side = tkinter.LEFT)

        self.label = ctk.CTkLabel(master=self.frame1, text="Index", font=("Century Gothic", 25, "bold"))
        self.label.place(relx=0.5, rely=0.085, anchor=tkinter.CENTER)

        def button_size(button):
            button.configure(width=260, height=40, font=("Century Gothic", 16), corner_radius=10)

        # Bind the button1 to frame3
        self.button1 = ctk.CTkButton(master=self.frame1, text="Add Department", command=self.add_department)
        button_size(self.button1)
        self.button1.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(master=self.frame1, text="Update Department")
        button_size(self.button2)
        self.button2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.button3 = ctk.CTkButton(master=self.frame1, text="Remove Department")
        button_size(self.button3)
        self.button3.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        self.button4 = ctk.CTkButton(master=self.frame1, text="View Department")
        button_size(self.button4)
        self.button4.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.button5 = ctk.CTkButton(master=self.frame1, text="View All Departments")
        button_size(self.button5)
        self.button5.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        self.button6 = ctk.CTkButton(master=self.frame1, text="Back", command=self.back)
        button_size(self.button6)
        self.button6.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        # create second frame
        self.frame2 = ctk.CTkFrame(master=self, width=900, height=700, corner_radius=10)
        self.frame2.pack(padx = 10, pady = 10, side = tkinter.RIGHT)

        # display on second frame
        self.label = ctk.CTkLabel(master=self.frame2, text="Department Management", font=("Century Gothic", 25, "bold"))
        self.label.place(relx=0.5, rely=0.085, anchor=tkinter.CENTER)

        def add_department(self):
            self.frame3 = ctk.CTkFrame(master=self, width=900, height=700, corner_radius=10)
            self.frame3.pack(padx = 10, pady = 10, side = tkinter.RIGHT)

            self.label = ctk.CTkLabel(master=self.frame3, text="Add Department", font=("Century Gothic", 25, "bold"))
            self.label.place(relx=0.5, rely=0.085, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Department Name", font=("Century Gothic", 16))
            self.label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

            self.entry = ctk.CTkEntry(master=self.frame3, width=20, font=("Century Gothic", 16))
            self.entry.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Add", command=self.add)
            self.button.configure(width=260, height=40, font=("Century Gothic", 16), corner_radius=10)
            self.button.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Back", command=self.back)
            self.button.configure(width=260, height=40, font=("Century Gothic", 16), corner_radius=10)
            self.button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        def update_department(self):
            self.frame3 = ctk.CTkFrame(master=self.frame2, width=900, height=700, corner_radius=10)
            self.frame3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Update Department", font=("Century Gothic", 25, "bold"))
            self.label.place(relx=0.5, rely=0.085, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Department Name", font=("Century Gothic", 16))
            self.label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

            self.entry = ctk.CTkEntry(master=self.frame3, width=20, font=("Century Gothic", 16))
            self.entry.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Update", command=self.update)
            self.button.configure(width=260, height=40, font=("Century Gothic", 16), corner_radius=10)
            self.button.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Back", command=self.back)
            self.button.configure(width=260, height=40, font=("Century Gothic", 16), corner_radius=10)
            self.button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        def remove_department(self):
            self.frame3 = ctk.CTkFrame(master=self.frame2, width=900, height=700, corner_radius=10)
            self.frame3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Remove Department", font=("Century Gothic", 25, "bold"))
            self.label.place(relx=0.5, rely=0.085, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Department Name", font=("Century Gothic", 16))
            self.label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

            self.entry = ctk.CTkEntry(master=self.frame3, width=20, font=("Century Gothic", 16))
            self.entry.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Remove", command=self.remove)
            self.button.configure(width=260, height=40, font=("Century Gothic", 16), corner_radius=10)
            self.button.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Back", command=self.back)
            self.button.configure(width=260, height=40, font=("Century Gothic", 16), corner_radius=10)
            self.button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        def view_department(self):
            self.frame3 = ctk.CTkFrame(master=self.frame2, width=900, height=700, corner_radius=10)
            self.frame3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="View Department", font=("Century Gothic", 25, "bold"))
            self.label.place(relx=0.5, rely=0.085, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Department Name", font=("Century Gothic", 16))
            self.label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

            self.entry = ctk.CTkEntry(master=self.frame3, width=20, font=("Century Gothic", 16))
            self.entry.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="View", command=self.view)
            self.button.configure(width=260, height=40, font=("Century Gothic", 16), corner_radius=10)
            self.button.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Back", command=self.back)
            self.button.configure(width=260, height=40, font=("Century Gothic", 16), corner_radius=10)
            self.button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        def view_all_departments(self):
            self.frame3 = ctk.CTkFrame(master=self.frame2, width=900, height=700, corner_radius=10)
            self.frame3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="View All Departments", font=("Century Gothic", 25, "bold"))
            self.label.place(relx=0.5, rely=0.085, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="View", command=self.view_all)
            self.button.configure(width=260, height=40, font=("Century Gothic", 16), corner_radius=10)
            self.button.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Back", command=self.back)
            self.button.configure(width=260, height=40, font=("Century Gothic", 16), corner_radius=10)
            self.button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        def back(self):
            self.frame3.destroy()

    def main():
        root = tkinter.Tk()
        root.title("Department")
        root.geometry("900x700")
        root.resizable(False, False)
        root.configure(bg="#ffffff")
        app = Department(root)
        root.mainloop()

    if __name__ == "__main__":
        main()



            
