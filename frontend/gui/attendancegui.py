import customtkinter as ctk
import tkinter
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

Width = 1024
Height = 768


class AttendanceGui(ctk.CTk):
    def __init__(self, master=None):
        super().__init__()

        self.title("Attendance Management System")
        self.geometry(f"{Width}x{Height}")
        self.resizable(True, True)

        def entry_size(entry):
            entry.configure(
                width=400, height=30, font=("Century Gothic", 14), corner_radius=10
            )

        def attendance_check(self):
            self.button1_frame = ctk.CTkFrame(master=self.right_frame)

            self.label = ctk.CTkLabel(
                master=self.button1_frame,
                text="Attendance Check",
                font=("Century Gothic", 30, "bold"),
            )
            self.label.pack()

            self.label1 = ctk.CTkLabel(
                master=self.right_frame,
                text="Name: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label1.place(relx=0.1, rely=0.15, anchor=tkinter.CENTER)

            self.entry1 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter Name"
            )
            entry_size(self.entry1)
            self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

            self.label2 = ctk.CTkLabel(
                master=self.right_frame,
                text="ID: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label2.place(relx=0.0715, rely=0.275, anchor=tkinter.CENTER)

            self.entry2 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter ID"
            )
            entry_size(self.entry2)
            self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

            self.label3 = ctk.CTkLabel(
                master=self.right_frame,
                text="Date: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label3.place(relx=0.085, rely=0.4, anchor=tkinter.CENTER)

            self.entry3 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="YYYY-MM-DD"
            )
            entry_size(self.entry3)
            self.entry3.place(relx=0.325, rely=0.445, anchor=tkinter.CENTER)

            self.label4 = ctk.CTkLabel(
                master=self.right_frame,
                text="Time: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label4.place(relx=0.085, rely=0.525, anchor=tkinter.CENTER)

            self.entry4 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="HH:MM:SS"
            )
            entry_size(self.entry4)
            self.entry4.place(relx=0.325, rely=0.57, anchor=tkinter.CENTER)

            self.label5 = ctk.CTkLabel(
                master=self.right_frame,
                text="Present/Absent/Late: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label5.place(relx=0.195, rely=0.65, anchor=tkinter.CENTER)

            self.radio1 = ctk.CTkRadioButton(
                master=self.right_frame,
                text="Absent",
                font=("Century Gothic", 15, "italic"),
            )
            self.radio1.place(relx=0.325, rely=0.695, anchor=tkinter.CENTER)

            self.radio2 = ctk.CTkRadioButton(
                master=self.right_frame,
                text="Late",
                font=("Century Gothic", 15, "italic"),
            )
            self.radio2.place(relx=0.325, rely=0.745, anchor=tkinter.CENTER)

            self.radio3 = ctk.CTkRadioButton(
                master=self.right_frame,
                text="Present",
                font=("Century Gothic", 15, "italic"),
            )
            self.radio3.place(relx=0.325, rely=0.795, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(
                master=self.right_frame,
                text="Confirm",
                command=(lambda: attendance_check(self)),
            )
            self.button.configure(
                width=100,
                height=40,
                font=("Century Gothic", 15, "bold"),
                corner_radius=10,
                fg_color="purple",
            )
            self.button.place(relx=0.5, rely=0.875, anchor=tkinter.CENTER)

            self.button1_frame.pack(pady=20)

            def attendance_check(self):
                name = self.entry1.get()
                id = self.entry2.get()
                date = self.entry3.get()
                time = self.entry4.get()

                if (
                    name == ""
                    or id == ""
                    or date == ""
                    or time == ""
                    or present == "None"
                ):
                    messagebox.showerror("Error", "Please fill in all the fields")
                elif not name.isalpha():
                    messagebox.showerror("Error", "Please enter a valid name")
                elif "-" not in date:
                    messagebox.showerror("Error", "Please enter a valid date")
                elif ":" not in time:
                    messagebox.showerror("Error", "Please enter a valid time")
                else:
                    messagebox.showinfo("Success", "Attendance has been recorded")

        def update_attendance(self):
            self.button1_frame = ctk.CTkFrame(master=self.right_frame)

            self.label = ctk.CTkLabel(
                master=self.button1_frame,
                text="Update Attendance Check",
                font=("Century Gothic", 30, "bold"),
            )
            self.label.pack()

            self.label0 = ctk.CTkLabel(
                master=self.right_frame,
                text="(You are currently update the attendance of: )",
                font=("Century Gothic", 14, "italic"),
            )
            self.label0.place(relx=0.5, rely=0.095, anchor=tkinter.CENTER)

            self.label1 = ctk.CTkLabel(
                master=self.right_frame,
                text="Name: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label1.place(relx=0.1, rely=0.15, anchor=tkinter.CENTER)

            self.entry1 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter Name"
            )
            entry_size(self.entry1)
            self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

            self.label2 = ctk.CTkLabel(
                master=self.right_frame,
                text="ID: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label2.place(relx=0.0715, rely=0.275, anchor=tkinter.CENTER)

            self.entry2 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter ID"
            )
            entry_size(self.entry2)
            self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

            self.label3 = ctk.CTkLabel(
                master=self.right_frame,
                text="Date: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label3.place(relx=0.085, rely=0.4, anchor=tkinter.CENTER)

            self.entry3 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="YYYY-MM-DD"
            )
            entry_size(self.entry3)
            self.entry3.place(relx=0.325, rely=0.445, anchor=tkinter.CENTER)

            self.label4 = ctk.CTkLabel(
                master=self.right_frame,
                text="Time: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label4.place(relx=0.085, rely=0.525, anchor=tkinter.CENTER)

            self.entry4 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="HH:MM:SS"
            )
            entry_size(self.entry4)
            self.entry4.place(relx=0.325, rely=0.57, anchor=tkinter.CENTER)

            self.label5 = ctk.CTkLabel(
                master=self.right_frame,
                text="Present/Absent/Late: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label5.place(relx=0.195, rely=0.65, anchor=tkinter.CENTER)

            self.radio1 = ctk.CTkRadioButton(
                master=self.right_frame,
                text="Absent",
                font=("Century Gothic", 15, "italic"),
            )
            self.radio1.place(relx=0.325, rely=0.695, anchor=tkinter.CENTER)

            self.radio2 = ctk.CTkRadioButton(
                master=self.right_frame,
                text="Late",
                font=("Century Gothic", 15, "italic"),
            )
            self.radio2.place(relx=0.325, rely=0.745, anchor=tkinter.CENTER)

            self.radio3 = ctk.CTkRadioButton(
                master=self.right_frame,
                text="Present",
                font=("Century Gothic", 15, "italic"),
            )
            self.radio3.place(relx=0.325, rely=0.795, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(
                master=self.right_frame,
                text="Update",
                command=(lambda: attendance_check(self)),
            )
            self.button.configure(
                width=100,
                height=40,
                font=("Century Gothic", 15, "bold"),
                corner_radius=10,
                fg_color="purple",
            )
            self.button.place(relx=0.5, rely=0.875, anchor=tkinter.CENTER)

            self.button1_frame.pack(pady=20)

            def attendance_check(self):
                name = self.entry1.get()
                id = self.entry2.get()
                date = self.entry3.get()
                time = self.entry4.get()

                if (
                    name == ""
                    or id == ""
                    or date == ""
                    or time == ""
                    or present == "None"
                ):
                    messagebox.showerror("Error", "Please fill in all the fields")
                elif not name.isalpha():
                    messagebox.showerror("Error", "Please enter a valid name")
                elif "-" not in date:
                    messagebox.showerror("Error", "Please enter a valid date")
                elif ":" not in time:
                    messagebox.showerror("Error", "Please enter a valid time")
                else:
                    messagebox.showinfo("Success", "Attendance has been recorded")

        def get_report(self):
            self.button3_frame = ctk.CTkFrame(master=self.right_frame)

            self.label = ctk.CTkLabel(
                master=self.button3_frame,
                text="Report",
                font=("Century Gothic", 30, "bold"),
            )
            self.label.pack()

            self.label1 = ctk.CTkLabel(
                master=self.right_frame,
                text="Name: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label1.place(relx=0.1, rely=0.15, anchor=tkinter.CENTER)

            self.entry1 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter Name"
            )
            entry_size(self.entry1)
            self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

            self.label2 = ctk.CTkLabel(
                master=self.right_frame,
                text="ID: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label2.place(relx=0.0715, rely=0.275, anchor=tkinter.CENTER)

            self.entry2 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter ID"
            )
            entry_size(self.entry2)
            self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(
                master=self.right_frame,
                text="Confirm",
                command=(lambda: get_report_successfully(self)),
            )
            self.button.configure(
                width=100,
                height=40,
                font=("Century Gothic", 15, "bold"),
                corner_radius=10,
                fg_color="purple",
            )
            self.button.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

            self.button3_frame.pack(pady=20)

            def get_report_successfully(self):
                name = self.entry1.get()
                id = self.entry2.get()

                if name == "" or id == "":
                    messagebox.showerror("Error", "Please fill in all the fields")
                elif not name.isalpha():
                    messagebox.showerror("Error", "Please enter a valid name")
                else:
                    messagebox.showinfo("Success", "Report has been generated")

        # Destroy all frames
        def destroy_all_frames(self):
            for widget in self.right_frame.winfo_children():
                widget.destroy()

        self.left_frame = ctk.CTkFrame(master=self, corner_radius=10)

        def button_size(button):
            button.configure(
                width=260,
                height=40,
                font=("Century Gothic", 15, "bold"),
                corner_radius=10,
            )

        self.button1 = ctk.CTkButton(
            master=self.left_frame,
            text="Attendance Check",
            command=(lambda: [destroy_all_frames(self), attendance_check(self)]),
        )
        button_size(self.button1)
        self.button1.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(
            master=self.left_frame,
            text="Update Attendace Check",
            command=(lambda: [destroy_all_frames(self), update_attendance(self)]),
        )
        button_size(self.button2)
        self.button2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.button3 = ctk.CTkButton(
            master=self.left_frame,
            text="Attendance Report",
            command=(lambda: [destroy_all_frames(self), get_report(self)]),
        )
        button_size(self.button3)
        self.button3.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

        self.button6 = ctk.CTkButton(
            master=self.left_frame,
            text="Back",
            fg_color="red",
            command=(lambda: self.back_to_homepage()),
        )
        self.button6.configure(
            width=100,
            height=40,
            font=("Century Gothic", 15, "bold"),
            corner_radius=10,
            fg_color="red",
        )
        self.button6.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        self.left_frame.pack(side=ctk.LEFT)
        self.left_frame.pack_propagate(False)
        self.left_frame.configure(width=320, height=760)

        self.right_frame = ctk.CTkFrame(master=self, border_width=2, corner_radius=10)
        self.right_frame.pack(side=ctk.RIGHT)
        self.right_frame.pack_propagate(False)
        self.right_frame.configure(width=700, height=760)

    def back_to_homepage(self):
        import homepage

        self.destroy()
        homepage.homepage().mainloop()


if __name__ == "__main__":
    app = AttendanceGui()
    app.mainloop()
