import customtkinter as ctk
import tkinter
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

Width = 1024
Height = 768


class BenefitPlanGui(ctk.CTk):
    def __init__(self, master=None):
        super().__init__()

        self.title("Benefit Plan Management")
        self.geometry(f"{Width}x{Height}")
        self.resizable(True, True)

        def entry_size(entry):
            entry.configure(
                width=400, height=30, font=("Century Gothic", 14), corner_radius=10
            )

        def add_benefit_plan(self):
            self.button1_frame = ctk.CTkFrame(master=self.right_frame)

            self.label = ctk.CTkLabel(
                master=self.button1_frame,
                text="Information",
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
                text="Description: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label2.place(relx=0.135, rely=0.275, anchor=tkinter.CENTER)

            self.entry2 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter Description"
            )
            entry_size(self.entry2)
            self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

            self.label3 = ctk.CTkLabel(
                master=self.right_frame,
                text="Cost: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label3.place(relx=0.085, rely=0.4, anchor=tkinter.CENTER)

            self.entry3 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter Cost"
            )
            entry_size(self.entry3)
            self.entry3.place(relx=0.325, rely=0.445, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(
                master=self.right_frame,
                text="Confirm",
                command=(lambda: add_successfully(self)),
            )
            self.button.configure(
                width=100,
                height=40,
                font=("Century Gothic", 15, "bold"),
                corner_radius=10,
                fg_color="purple",
            )
            self.button.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

            self.button1_frame.pack(pady=20)

            def add_successfully(self):
                name = self.entry1.get()
                description = self.entry2.get()
                cost = self.entry3.get()
                if name == "" or description == "" or cost == "":
                    messagebox.showerror("Error", "Please fill in all the fields")
                elif not name.isalpha():
                    messagebox.showerror("Error", "Name must be a string")
                elif not description.isalpha():
                    messagebox.showerror("Error", "Description must be a string")
                elif not cost.isdigit():
                    messagebox.showerror("Error", "Cost must be a number")
                else:
                    messagebox.showinfo("Success", "Benefit Plan added successfully")

        def remove_benefit_plan(self):
            self.button2_frame = ctk.CTkFrame(master=self.right_frame)

            self.label = ctk.CTkLabel(
                master=self.button2_frame,
                text="Remove Benefit Plan",
                font=("Century Gothic", 30, "bold"),
            )
            self.label.pack()

            self.label1 = ctk.CTkLabel(
                master=self.right_frame,
                text="Benefit name: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label1.place(relx=0.145, rely=0.15, anchor=tkinter.CENTER)

            self.entry1 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter Name"
            )
            entry_size(self.entry1)
            self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(
                master=self.right_frame,
                text="Remove",
                fg_color="red",
                command=(lambda: remove_successfully(self)),
            )
            self.button.configure(
                width=100,
                height=40,
                font=("Century Gothic", 15, "bold"),
                corner_radius=10,
            )
            self.button.place(relx=0.5, rely=0.295, anchor=tkinter.CENTER)

            self.button2_frame.pack(pady=20)

            def remove_successfully(self):
                name = self.entry1.get()
                if name == "" or id == "" or department == "":
                    messagebox.showerror("Error", "Please fill in all the fields")
                elif not name.isalpha():
                    messagebox.showerror("Error", "Please enter a valid name")
                else:
                    messagebox.showinfo("Success", "Benefit Plan removed successfully")

        def update_benefit_plan(self):
            self.button3_frame = ctk.CTkFrame(master=self.right_frame)

            self.label = ctk.CTkLabel(
                master=self.button3_frame,
                text="Update Information",
                font=("Century Gothic", 30, "bold"),
            )
            self.label.pack()

            self.label0 = ctk.CTkLabel(
                master=self.right_frame,
                text="(You are currently update the information of: ) ",
                font=("Century Gothic", 14, "italic"),
            )
            self.label0.place(relx=0.5, rely=0.095, anchor=tkinter.CENTER)

            self.label1 = ctk.CTkLabel(
                master=self.right_frame,
                text="Old Name: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label1.place(relx=0.135, rely=0.15, anchor=tkinter.CENTER)

            self.entry1 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter old name"
            )
            entry_size(self.entry1)
            self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

            self.label2 = ctk.CTkLabel(
                master=self.right_frame,
                text="New name: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label2.place(relx=0.135, rely=0.275, anchor=tkinter.CENTER)

            self.entry2 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter new name"
            )
            entry_size(self.entry2)
            self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

            self.label3 = ctk.CTkLabel(
                master=self.right_frame,
                text="New Description: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label3.place(relx=0.175, rely=0.4, anchor=tkinter.CENTER)

            self.entry3 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter new description"
            )
            entry_size(self.entry3)
            self.entry3.place(relx=0.325, rely=0.445, anchor=tkinter.CENTER)

            self.label4 = ctk.CTkLabel(
                master=self.right_frame,
                text="New cost: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label4.place(relx=0.135, rely=0.525, anchor=tkinter.CENTER)

            self.entry4 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter new cost"
            )
            entry_size(self.entry4)
            self.entry4.place(relx=0.325, rely=0.57, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(
                master=self.right_frame,
                text="Update",
                command=(lambda: update_successfully(self)),
            )
            self.button.configure(
                width=100,
                height=40,
                font=("Century Gothic", 15, "bold"),
                corner_radius=10,
                fg_color="purple",
            )
            self.button.place(relx=0.5, rely=0.675, anchor=tkinter.CENTER)

            self.button3_frame.pack(pady=20)

            def update_successfully(self):
                name = self.entry1.get()
                new_name = self.entry2.get()
                new_description = self.entry3.get()
                new_cost = self.entry4.get()
                if (
                    name == ""
                    or new_name == ""
                    or new_description == ""
                    or new_cost == ""
                ):
                    messagebox.showerror("Error", "Please fill in all the fields")
                elif not name.isalpha() or not new_name.isalpha():
                    messagebox.showerror("Error", "Please enter a valid value")
                elif not new_cost.isdigit():
                    messagebox.showerror("Error", "Please enter a valid cost")
                else:
                    messagebox.showinfo("Success", "Benefit Plan updated successfully")

        def apply_benefit_plan(self):
            self.button5_frame = ctk.CTkFrame(master=self.right_frame)

            self.label = ctk.CTkLabel(
                master=self.button5_frame,
                text="Apply Benefit Plan",
                font=("Century Gothic", 30, "bold"),
            )
            self.label.pack()

            self.label1 = ctk.CTkLabel(
                master=self.right_frame,
                text="Benefit Plan Name: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label1.place(relx=0.175, rely=0.15, anchor=tkinter.CENTER)

            self.entry1 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter name"
            )
            entry_size(self.entry1)
            self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

            self.label2 = ctk.CTkLabel(
                master=self.right_frame,
                text="Employee ID: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label2.place(relx=0.135, rely=0.275, anchor=tkinter.CENTER)

            self.entry2 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter ID"
            )
            entry_size(self.entry2)
            self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(
                master=self.right_frame,
                text="Apply",
                command=(lambda: apply_successfully(self)),
            )
            self.button.configure(
                width=100,
                height=40,
                font=("Century Gothic", 15, "bold"),
                corner_radius=10,
                fg_color="purple",
            )
            self.button.place(relx=0.5, rely=0.425, anchor=tkinter.CENTER)

            self.button5_frame.pack(pady=20)

            def apply_successfully(self):
                name = self.entry1.get()
                id = self.entry2.get()
                if name == "" or id == "":
                    messagebox.showerror("Error", "Please fill in all the fields")
                elif not name.isalpha():
                    messagebox.showerror("Error", "Please enter a valid name")
                else:
                    messagebox.showinfo("Success", "Benefit Plan applied successfully")

        def view_benefit_plan(self):
            self.button2_frame = ctk.CTkFrame(master=self.right_frame)

            self.label = ctk.CTkLabel(
                master=self.button2_frame,
                text="View Benefit Plan",
                font=("Century Gothic", 30, "bold"),
            )
            self.label.pack()

            self.label1 = ctk.CTkLabel(
                master=self.right_frame,
                text="Benefit name: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label1.place(relx=0.145, rely=0.15, anchor=tkinter.CENTER)

            self.entry1 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter Name"
            )
            entry_size(self.entry1)
            self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(
                master=self.right_frame, text="View", fg_color="purple"
            )
            self.button.configure(
                width=100,
                height=40,
                font=("Century Gothic", 15, "bold"),
                corner_radius=10,
            )
            self.button.place(relx=0.5, rely=0.295, anchor=tkinter.CENTER)

            self.button2_frame.pack(pady=20)

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
            text="Add Benefit Plan",
            command=(lambda: [destroy_all_frames(self), add_benefit_plan(self)]),
        )
        button_size(self.button1)
        self.button1.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(
            master=self.left_frame,
            text="Remove Benefit Plan",
            command=(lambda: [destroy_all_frames(self), remove_benefit_plan(self)]),
        )
        button_size(self.button2)
        self.button2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.button3 = ctk.CTkButton(
            master=self.left_frame,
            text="Update Benefit Plan",
            command=(lambda: [destroy_all_frames(self), update_benefit_plan(self)]),
        )
        button_size(self.button3)
        self.button3.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

        self.button4 = ctk.CTkButton(
            master=self.left_frame,
            text="View Benefit Plan",
            command=(lambda: [destroy_all_frames(self), view_benefit_plan(self)]),
        )
        button_size(self.button4)
        self.button4.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        self.button5 = ctk.CTkButton(
            master=self.left_frame,
            text="Apply to the employee",
            command=(lambda: [destroy_all_frames(self), apply_benefit_plan(self)]),
        )
        button_size(self.button5)
        self.button5.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

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
    app = BenefitPlanGui()
    app.mainloop()
