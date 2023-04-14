import customtkinter as ctk
import tkinter
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

Width = 1024
Height = 768

class payrollgui(ctk.CTk):
    def __init__(self, master = None):
        super().__init__()

        self.title("Attendance Management System")
        self.geometry(f"{Width}x{Height}")
        self.resizable(True, True)

        def entry_size(entry):
                entry.configure(width=400, height=30, font=("Century Gothic", 14), corner_radius=10)

        def create_payroll(self):
            self.button1_frame= ctk.CTkFrame(master=self.right_frame)
            
            self.label = ctk.CTkLabel(master=self.button1_frame, text="Create payroll", font=("Century Gothic", 30, "bold"))
            self.label.pack()

            self.label1 = ctk.CTkLabel(master=self.right_frame, text="Salary: ", font=("Century Gothic", 20, "italic"))
            self.label1.place(relx=0.115, rely=0.15, anchor=tkinter.CENTER)

            self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter payroll salary")
            entry_size(self.entry1)
            self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

            self.label2 = ctk.CTkLabel(master=self.right_frame, text="Bonus:", font=("Century Gothic", 20, "italic"))
            self.label2.place(relx=0.105, rely=0.275, anchor=tkinter.CENTER)

            self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter payroll bonus")
            entry_size(self.entry2)
            self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

            self.label3 = ctk.CTkLabel(master=self.right_frame, text="Tax: ", font=("Century Gothic", 20, "italic"))
            self.label3.place(relx=0.0925, rely=0.4, anchor=tkinter.CENTER)

            self.entry3 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter payroll tax")
            entry_size(self.entry3)
            self.entry3.place(relx=0.325, rely=0.445, anchor=tkinter.CENTER)

            self.label4 = ctk.CTkLabel(master=self.right_frame, text="Punishment: ", font=("Century Gothic", 20, "italic"))
            self.label4.place(relx=0.145, rely=0.525, anchor=tkinter.CENTER)

            self.entry4 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter payroll punishment")
            entry_size(self.entry4)
            self.entry4.place(relx=0.325, rely=0.57, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.right_frame, text="Confirm", command=(lambda: add_successfully(self)))
            self.button.configure(width=100, height = 40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
            self.button.place(relx=0.5, rely=0.675, anchor=tkinter.CENTER)

            self.button1_frame.pack(pady = 20)

            def add_successfully(self):
                salary = self.entry1.get()
                bonus = self.entry2.get()
                tax = self.entry3.get()
                punishment = self.entry4.get()
                if salary == "" or bonus == "" or tax == "" or punishment == "":
                    messagebox.showerror("Error", "Please fill in all the fields")
                elif not salary.isdigit() or not bonus.isdigit() or not tax.isdigit() or not punishment.isdigit():
                    messagebox.showerror("Error", "Please enter a valid number")
                else:
                    messagebox.showinfo("Success", "Payroll has been created successfully")
            

        def update_payroll(self):
            self.button1_frame= ctk.CTkFrame(master=self.right_frame)
            
            self.label = ctk.CTkLabel(master=self.button1_frame, text="Update payroll", font=("Century Gothic", 30, "bold"))
            self.label.pack()

            self.label1 = ctk.CTkLabel(master=self.right_frame, text="Salary: ", font=("Century Gothic", 20, "italic"))
            self.label1.place(relx=0.115, rely=0.15, anchor=tkinter.CENTER)

            self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter payroll salary")
            entry_size(self.entry1)
            self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

            self.label2 = ctk.CTkLabel(master=self.right_frame, text="Bonus:", font=("Century Gothic", 20, "italic"))
            self.label2.place(relx=0.105, rely=0.275, anchor=tkinter.CENTER)

            self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter payroll bonus")
            entry_size(self.entry2)
            self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

            self.label3 = ctk.CTkLabel(master=self.right_frame, text="Tax: ", font=("Century Gothic", 20, "italic"))
            self.label3.place(relx=0.0925, rely=0.4, anchor=tkinter.CENTER)

            self.entry3 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter payroll tax")
            entry_size(self.entry3)
            self.entry3.place(relx=0.325, rely=0.445, anchor=tkinter.CENTER)

            self.label4 = ctk.CTkLabel(master=self.right_frame, text="Punishment: ", font=("Century Gothic", 20, "italic"))
            self.label4.place(relx=0.145, rely=0.525, anchor=tkinter.CENTER)

            self.entry4 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter payroll punishment")
            entry_size(self.entry4)
            self.entry4.place(relx=0.325, rely=0.57, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(master=self.right_frame, text="Update", command=(lambda: update_successfully(self)))
            self.button.configure(width=100, height = 40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
            self.button.place(relx=0.5, rely=0.675, anchor=tkinter.CENTER)

            self.button1_frame.pack(pady = 20)

            def update_successfully(self):
                salary = self.entry1.get()
                bonus = self.entry2.get()
                tax = self.entry3.get()
                punishment = self.entry4.get()
                if salary == "" or bonus == "" or tax == "" or punishment == "":
                    messagebox.showerror("Error", "Please fill in all the fields")
                elif not salary.isdigit() or not bonus.isdigit() or not tax.isdigit() or not punishment.isdigit():
                    messagebox.showerror("Error", "Please enter a valid number")
                else:
                    messagebox.showinfo("Success", "Payroll has been created successfully")

        # Destroy all frames
        def destroy_all_frames(self):
            for widget in self.right_frame.winfo_children():
                widget.destroy()

        self.left_frame = ctk.CTkFrame(master=self, corner_radius=10)

        def button_size(button):
            button.configure(width=260, height = 40, font=("Century Gothic", 15, "bold"), corner_radius=10)
        
        self.button1 = ctk.CTkButton(master=self.left_frame, text="Create Payroll", command=(lambda: [destroy_all_frames(self), create_payroll(self)]))
        button_size(self.button1)
        self.button1.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(master=self.left_frame, text="Update Payroll", command=(lambda : [destroy_all_frames(self), update_payroll(self)]))
        button_size(self.button2)
        self.button2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

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
    app = payrollgui()
    app.mainloop()