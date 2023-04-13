import customtkinter as ctk
import tkinter
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

Width = 1024
Height = 768

class employeegui(ctk.CTk):
    def __init__(self, master = None):
        super().__init__()

        self.title("Employee Management")
        self.geometry(f"{Width}x{Height}")
        self.resizable(True, True)

        def entry_size(entry):
                entry.configure(width=400, height=30, font=("Century Gothic", 14), corner_radius=10)

        def add_employee(self):
            self.button1_frame= ctk.CTkFrame(master=self.right_frame)
            
            self.label = ctk.CTkLabel(master=self.button1_frame, text="Information", font=("Century Gothic", 30, "bold"))
            self.label.pack()

            self.label1 = ctk.CTkLabel(master=self.right_frame, text="Name: ", font=("Century Gothic", 20, "italic"))
            self.label1.place(relx=0.1, rely=0.15, anchor=tkinter.CENTER)

            self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Name")
            entry_size(self.entry1)
            self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

            self.label2 = ctk.CTkLabel(master=self.right_frame, text="Date of birth: ", font=("Century Gothic", 20, "italic"))
            self.label2.place(relx=0.145, rely=0.275, anchor=tkinter.CENTER)

            self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="YYYY-MM-DD")
            entry_size(self.entry2)
            self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

            self.label3 = ctk.CTkLabel(master=self.right_frame, text="ID: ", font=("Century Gothic", 20, "italic"))
            self.label3.place(relx=0.0715, rely=0.4, anchor=tkinter.CENTER)

            self.entry3 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
            entry_size(self.entry3)
            self.entry3.place(relx=0.325, rely=0.445, anchor=tkinter.CENTER)

            self.label4 = ctk.CTkLabel(master=self.right_frame, text="Phone Number: ", font=("Century Gothic", 20, "italic"))
            self.label4.place(relx=0.155, rely=0.525, anchor=tkinter.CENTER)

            self.entry4 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Phone Number")
            entry_size(self.entry4)
            self.entry4.place(relx=0.325, rely=0.57, anchor=tkinter.CENTER)

            self.label5 = ctk.CTkLabel(master=self.right_frame, text="Email: ", font=("Century Gothic", 20, "italic"))
            self.label5.place(relx=0.09, rely=0.65, anchor=tkinter.CENTER)

            self.entry5 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Email")
            entry_size(self.entry5)
            self.entry5.place(relx=0.325, rely=0.695, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.right_frame, text="Confirm", command=(lambda: add_successfully(self)))
            self.button.configure(width=100, height = 40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
            self.button.place(relx=0.5, rely=0.795, anchor=tkinter.CENTER)

            self.button1_frame.pack(pady = 20)

            def add_successfully(self):
                name = self.entry1.get()
                dob = self.entry2.get()
                id = self.entry3.get()
                phone = self.entry4.get()
                email = self.entry5.get()
                if name == "" or dob == "" or id == "" or phone == "" or email == "":
                    messagebox.showerror("Error", "Please fill in all the fields")
                elif not name.isalpha():
                    messagebox.showerror("Error", "Please enter a valid name")
                elif not phone.isdigit() and len(phone) != 10:
                    messagebox.showerror("Error", "Please enter a valid phone number")
                elif not "@" in email:
                    messagebox.showerror("Error", "Please enter a valid email")
                elif not "-" in dob:
                    messagebox.showerror("Error", "Please enter a valid date of birth")
                else:
                    messagebox.showinfo("Success", "Employee added successfully")

        def remove_employee(self):
            self.button2_frame = ctk.CTkFrame(master=self.right_frame)

            self.label = ctk.CTkLabel(master=self.button2_frame, text="Remove Employee", font=("Century Gothic", 30, "bold"))
            self.label.pack()

            self.label1 = ctk.CTkLabel(master=self.right_frame, text="Name: ", font=("Century Gothic", 20, "italic"))
            self.label1.place(relx=0.1, rely=0.15, anchor=tkinter.CENTER)

            self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Name")
            entry_size(self.entry1)
            self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

            self.label2 = ctk.CTkLabel(master=self.right_frame, text="ID: ", font=("Century Gothic", 20, "italic"))
            self.label2.place(relx=0.0715, rely=0.275, anchor=tkinter.CENTER)

            self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
            entry_size(self.entry2)
            self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

            self.label3 = ctk.CTkLabel(master=self.right_frame, text="Department: ", font=("Century Gothic", 20, "italic"))
            self.label3.place(relx=0.145, rely=0.4, anchor=tkinter.CENTER)

            self.entry3 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Department")
            entry_size(self.entry3)
            self.entry3.place(relx=0.325, rely=0.445, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.right_frame, text="Remove", fg_color="red", command=(lambda: remove_successfully(self)))
            self.button.configure(width=100, height = 40, font=("Century Gothic", 15, "bold"), corner_radius=10)
            self.button.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

            self.button2_frame.pack(pady = 20)
            
            def remove_successfully(self):
                name = self.entry1.get()
                id = self.entry2.get()
                department = self.entry3.get()
                if name == "" or id == "" or department == "":
                    messagebox.showerror("Error", "Please fill in all the fields")
                elif not name.isalpha():
                    messagebox.showerror("Error", "Please enter a valid name")
                else:
                    messagebox.showinfo("Success", "Employee removed successfully")

        def update_employee(self):
            self.button3_frame= ctk.CTkFrame(master=self.right_frame)
            
            self.label = ctk.CTkLabel(master=self.button3_frame, text="Update Information", font=("Century Gothic", 30, "bold"))
            self.label.pack()

            self.label0 = ctk.CTkLabel(master=self.right_frame, text="(You are currently update the information of: ) ", font=("Century Gothic", 14, "italic"))
            self.label0.place(relx=0.5, rely=0.095, anchor=tkinter.CENTER)

            self.label1 = ctk.CTkLabel(master=self.right_frame, text="Name: ", font=("Century Gothic", 20, "italic"))
            self.label1.place(relx=0.1, rely=0.15, anchor=tkinter.CENTER)

            self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Name")
            entry_size(self.entry1)
            self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

            self.label2 = ctk.CTkLabel(master=self.right_frame, text="Date of birth: ", font=("Century Gothic", 20, "italic"))
            self.label2.place(relx=0.145, rely=0.275, anchor=tkinter.CENTER)

            self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="YYYY-MM-DD")
            entry_size(self.entry2)
            self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

            self.label3 = ctk.CTkLabel(master=self.right_frame, text="ID: ", font=("Century Gothic", 20, "italic"))
            self.label3.place(relx=0.0715, rely=0.4, anchor=tkinter.CENTER)

            self.entry3 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
            entry_size(self.entry3)
            self.entry3.place(relx=0.325, rely=0.445, anchor=tkinter.CENTER)

            self.label4 = ctk.CTkLabel(master=self.right_frame, text="Phone Number: ", font=("Century Gothic", 20, "italic"))
            self.label4.place(relx=0.155, rely=0.525, anchor=tkinter.CENTER)

            self.entry4 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Phone Number")
            entry_size(self.entry4)
            self.entry4.place(relx=0.325, rely=0.57, anchor=tkinter.CENTER)

            self.label5 = ctk.CTkLabel(master=self.right_frame, text="Email: ", font=("Century Gothic", 20, "italic"))
            self.label5.place(relx=0.09, rely=0.65, anchor=tkinter.CENTER)

            self.entry5 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Email")
            entry_size(self.entry5)
            self.entry5.place(relx=0.325, rely=0.695, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.right_frame, text="Update", command=(lambda: update_successfully(self)))
            self.button.configure(width=100, height = 40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
            self.button.place(relx=0.5, rely=0.795, anchor=tkinter.CENTER)

            self.button3_frame.pack(pady = 20)

            def update_successfully(self):
                name = self.entry1.get()
                dob = self.entry2.get()
                id = self.entry3.get()
                phone = self.entry4.get()
                email = self.entry5.get()
                if name == "" or dob == "" or id == "" or phone == "" or email == "":
                    messagebox.showerror("Error", "Please fill in all the fields")
                elif not name.isalpha():
                    messagebox.showerror("Error", "Please enter a valid name")
                elif id == "":
                    messagebox.showerror("Error", "Please enter a valid ID")
                elif not phone.isdigit() and len(phone) != 10:
                    messagebox.showerror("Error", "Please enter a valid phone number")
                elif not "@" in email:
                    messagebox.showerror("Error", "Please enter a valid email")
                elif not "-" in dob:
                    messagebox.showerror("Error", "Please enter a valid date of birth")
                else:
                    messagebox.showinfo("Success", "Employee updated successfully")

        def view_emplopyee(self):
            self.button2_frame = ctk.CTkFrame(master=self.right_frame)

            self.label = ctk.CTkLabel(master=self.button2_frame, text="View Employee", font=("Century Gothic", 30, "bold"))
            self.label.pack()

            self.label1 = ctk.CTkLabel(master=self.right_frame, text="Employee ID: ", font=("Century Gothic", 20, "italic"))
            self.label1.place(relx=0.145, rely=0.15, anchor=tkinter.CENTER)

            self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
            entry_size(self.entry1)
            self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)


            self.button = ctk.CTkButton(master=self.right_frame, text="View", fg_color="purple", command=(lambda: view_employee(self)))
            self.button.configure(width=100, height = 40, font=("Century Gothic", 15, "bold"), corner_radius=10)
            self.button.place(relx=0.5, rely=0.295, anchor=tkinter.CENTER)

            self.button2_frame.pack(pady = 20)

            def view_employee(self):
                id = self.entry1.get()
                if id == "":
                    messagebox.showerror("Error", "Please enter a valid ID")
                else:
                    messagebox.showinfo("Success", "Employee found")

        # Destroy all frames
        def destroy_all_frames(self):
            for widget in self.right_frame.winfo_children():
                widget.destroy()

        self.left_frame = ctk.CTkFrame(master=self, corner_radius=10)

        def button_size(button):
            button.configure(width=260, height = 40, font=("Century Gothic", 15, "bold"), corner_radius=10)
        
        self.button1 = ctk.CTkButton(master=self.left_frame, text="Add Employee", command=(lambda: [destroy_all_frames(self), add_employee(self)]))
        button_size(self.button1)
        self.button1.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(master=self.left_frame, text="Remove Employee", command=(lambda : [destroy_all_frames(self), remove_employee(self)]))
        button_size(self.button2)
        self.button2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.button3 = ctk.CTkButton(master=self.left_frame, text="Update Employee", command=(lambda : [destroy_all_frames(self), update_employee(self)]))
        button_size(self.button3)
        self.button3.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

        self.button4 = ctk.CTkButton(master=self.left_frame, text="View Employee", command=(lambda : [destroy_all_frames(self), view_emplopyee(self)]))
        button_size(self.button4)
        self.button4.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        self.button5 = ctk.CTkButton(master=self.left_frame, text="View All Employees")
        button_size(self.button5)
        self.button5.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

        self.button6 = ctk.CTkButton(master=self.left_frame, text="Back", fg_color="red", command=(lambda: self.back_to_homepage()))
        self.button6.configure(width=100, height = 40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="red")
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
    app = employeegui()
    app.mainloop()