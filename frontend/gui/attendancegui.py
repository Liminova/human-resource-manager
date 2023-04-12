class AttendanceGUI(ctk.CTk):
    def __init__(self, master = None):
        super().__init__()

        self.title("Attendance Management")
        self.geometry(f"{Width}x{Height}")
        self.resizable(True, True)

        self.frame1 = ctk.CTkFrame(master=self, width=325, height=700, corner_radius=10)
        self.frame1.pack(padx = 10, pady = 10, side = tkinter.LEFT)

        self.label = ctk.CTkLabel(master=self.frame1, text="Index", font=("Century Gothic", 25, "bold"))
        self.label.place(relx=0.5, rely=0.085, anchor=tkinter.CENTER)

        def button_size(button):
            button.configure(width=260, height=40, font=("Century Gothic", 16), corner_radius=10)

        # Bind the button1 to frame3
        self.button1 = ctk.CTkButton(master=self.frame1, text="Check Attendance", command=self.add_attendance)
        button_size(self.button1)
        self.button1.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(master=self.frame1, text="Update Attendance")
        button_size(self.button2)
        self.button2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.button3 = ctk.CTkButton(master=self.frame1, text="Get Attendance Report")
        button_size(self.button3)
        self.button3.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        self.button4 = ctk.CTkButton(master=self.frame1, text="Exit")
        button_size(self.button4)
        self.button4.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # create second frame
        self.frame2 = ctk.CTkFrame(master=self, width=900, height=700, corner_radius=10)
        self.frame2.pack(padx = 10, pady = 10, side = tkinter.RIGHT)

        # display on the second frame
        self.label = ctk.CTkLabel(master=self.frame2, text="Attendance Management", font=("Century Gothic", 25, "bold"))
        self.label.place(relx=0.5, rely=0.085, anchor=tkinter.CENTER)

        def check_attendance(self):
            self.frame3 = ctk.CTkFrame(master=self.frame2, width=900, height=700, corner_radius=10)
            self.frame3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Check Attendance", font=("Century Gothic", 25, "bold"))
            self.label.place(relx=0.5, rely=0.085, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Enter Index", font=("Century Gothic", 16))
            self.label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

            self.entry = ctk.CTkEntry(master=self.frame3, width=30)
            self.entry.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Check", command=self.check_attendance)
            self.button.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Back", command=self.back)
            self.button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        def update_attendance(self):
            self.frame3 = ctk.CTkFrame(master=self.frame2, width=900, height=700, corner_radius=10)
            self.frame3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Update Attendance", font=("Century Gothic", 25, "bold"))
            self.label.place(relx=0.5, rely=0.085, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Enter Index", font=("Century Gothic", 16))
            self.label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

            self.entry = ctk.CTkEntry(master=self.frame3, width=30)
            self.entry.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Update", command=self.update_attendance)
            self.button.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Back", command=self.back)
            self.button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        def get_attendance_report(self):
            self.frame3 = ctk.CTkFrame(master=self.frame2, width=900, height=700, corner_radius=10)
            self.frame3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Get Attendance Report", font=("Century Gothic", 25, "bold"))
            self.label.place(relx=0.5, rely=0.085, anchor=tkinter.CENTER)

            self.label = ctk.CTkLabel(master=self.frame3, text="Enter Index", font=("Century Gothic", 16))
            self.label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

            self.entry = ctk.CTkEntry(master=self.frame3, width=30)
            self.entry.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Get Report", command=self.get_attendance_report)
            self.button.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.frame3, text="Back", command=self.back)
            self.button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        def back(self):
            self.frame3.destroy()

    def main():
        root = tkinter.Tk()
        root.title("Attendance Management")
        root.geometry("1200x700")
        root.resizable(False, False)
        app = Application(master=root)
        app.mainloop()

    if __name__ == "__main__":
        main()


        
