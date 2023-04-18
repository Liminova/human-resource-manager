import customtkinter as ctk
import tkinter
import os

from tkinter import messagebox as msgbox
from models import Company, BenefitPlan
from database.mongo import employee_repo, benefit_repo
from frontend.helpers import merge_callable

the_company = Company()

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
        self.left_frame = ctk.CTkFrame(master=self, corner_radius=10)

        if the_company.logged_in_employee.is_admin:
            self.admin()
        else:
            self.employee()

        self.left_frame.pack(side=ctk.LEFT)
        self.left_frame.pack_propagate(False)
        self.left_frame.configure(width=320, height=760)

        self.right_frame = ctk.CTkFrame(master=self, border_width=2, corner_radius=10)
        self.right_frame.pack(side=ctk.RIGHT)
        self.right_frame.pack_propagate(False)
        self.right_frame.configure(width=700, height=760)

    def admin(self):
        self.button1 = ctk.CTkButton(
            master=self.left_frame, text="Add Benefit Plan", command=merge_callable(self.__destroy_all_frames, self.__admin_add_benefit_plan)
        )
        self.__button_style(self.button1)
        self.button1.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(
            master=self.left_frame, text="Remove Benefit Plan", command=merge_callable(self.__destroy_all_frames, self.__admin_remove_benefit_plan)
        )
        self.__button_style(self.button2)
        self.button2.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        self.button3 = ctk.CTkButton(
            master=self.left_frame, text="Update Benefit Plan", command=merge_callable(self.__destroy_all_frames, self.__admin_update_benefit_plan)
        )
        self.__button_style(self.button3)
        self.button3.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.button4 = ctk.CTkButton(
            master=self.left_frame, text="View Benefit Plan", command=merge_callable(self.__destroy_all_frames, self.__admin_view_benefit_plan)
        )
        self.__button_style(self.button4)
        self.button4.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        self.button5 = ctk.CTkButton(
            master=self.left_frame, text="Apply to the employee", command=merge_callable(self.__destroy_all_frames, self.__admin_apply_benefit_plan)
        )
        self.__button_style(self.button5)
        self.button5.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.button6 = ctk.CTkButton(
            master=self.left_frame, text="List all", command=merge_callable(self.__destroy_all_frames, self.__admin_list_all_plans)
        )
        self.__button_style(self.button6)
        self.button6.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        self.button7 = ctk.CTkButton(master=self.left_frame, text="Back", command=lambda self=self: self.__back_to_homepage())
        self.button7.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="red")
        self.button7.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

    def employee(self):
        self.button1 = ctk.CTkButton(
            master=self.left_frame, text="View Benefit Plan", command=merge_callable(self.__destroy_all_frames, self.__employee_view_benefit_plan)
        )
        self.__button_style(self.button1)
        self.button1.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(
            master=self.left_frame, text="List all", command=merge_callable(self.__destroy_all_frames, self.__employee_list_all_plans)
        )
        self.__button_style(self.button2)
        self.button2.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

        self.button3 = ctk.CTkButton(master=self.left_frame, text="Back", command=lambda self=self: self.__back_to_homepage())
        self.button3.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="red")
        self.button3.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

    def __style_input_box(self, element):
        element.configure(width=400, height=30, font=("Century Gothic", 14), corner_radius=10)

    def __button_style(self, button):
        button.configure(width=260, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10)

    def __destroy_all_frames(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def __back_to_homepage(self):
        from .homepage import Homepage

        self.destroy()
        Homepage().mainloop()

    # region: admin functions

    def __admin_add_benefit_plan(self):
        self.button1_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button1_frame, text="Information", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Name: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.1, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Name")
        self.__style_input_box(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.label2 = ctk.CTkLabel(master=self.right_frame, text="Description: ", font=("Century Gothic", 20, "italic"))
        self.label2.place(relx=0.135, rely=0.275, anchor=tkinter.CENTER)

        self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Description")
        self.__style_input_box(self.entry2)
        self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

        self.label3 = ctk.CTkLabel(master=self.right_frame, text="Cost: ", font=("Century Gothic", 20, "italic"))
        self.label3.place(relx=0.085, rely=0.4, anchor=tkinter.CENTER)

        self.entry3 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Cost")
        self.__style_input_box(self.entry3)
        self.entry3.place(relx=0.325, rely=0.445, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="Confirm", command=(lambda: add_successfully(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

        self.button1_frame.pack(pady=20)

        def add_successfully(self):
            name = self.entry1.get()
            description = self.entry2.get()
            cost = self.entry3.get()
            # create a blank benefit plan object
            benefit = BenefitPlan()
            if name == "" or description == "" or cost == "":
                msgbox.showerror("Error", "Please fill in all the fields")
            elif not name.isalpha():
                msgbox.showerror("Error", "Name must be a string")
            elif not cost.isdigit():
                msgbox.showerror("Error", "Cost must be a number")
            else:
                # assign values to the benefit plan object
                benefit.name = name
                benefit.description = description
                benefit.cost = cost

                # add the benefit plan to the company and database
                the_company.benefits.append(benefit)

                if os.getenv("HRMGR_DB") == "TRUE":
                    benefit_repo.insert_one(benefit.dict(by_alias=True))
                msgbox.showinfo("Success", "Benefit Plan added successfully")

    def __admin_remove_benefit_plan(self):
        self.button2_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button2_frame, text="Remove Benefit Plan", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Benefit Plan ID: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.145, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
        self.__style_input_box(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="Remove", fg_color="red", command=(lambda: remove_successfully(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10)
        self.button.place(relx=0.5, rely=0.295, anchor=tkinter.CENTER)

        self.button2_frame.pack(pady=20)

        def remove_successfully(self):
            benefit_name = self.entry1.get()

            if benefit_name == "":
                msgbox.showerror("Error", "Please fill in all the fields")

            for bp in the_company.benefits:
                if bp.name == benefit_name:
                    the_company.benefits.remove(bp)
                    if os.getenv("HRMGR_DB") == "TRUE":
                        benefit_repo.delete_one({"name": bp.name})
                    msgbox.showinfo("Success", "Benefit Plan removed successfully")
                    break
            else:
                msgbox.showerror("Error", "Benefit Plan not found")

    def __admin_update_benefit_plan(self):
        self.button3_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button3_frame, text="Update Information", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Benefit Plan Name: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.175, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter name")
        self.__style_input_box(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.label2 = ctk.CTkLabel(master=self.right_frame, text="New name: ", font=("Century Gothic", 20, "italic"))
        self.label2.place(relx=0.135, rely=0.275, anchor=tkinter.CENTER)

        self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter new name")
        self.__style_input_box(self.entry2)
        self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

        self.label3 = ctk.CTkLabel(master=self.right_frame, text="New Description: ", font=("Century Gothic", 20, "italic"))
        self.label3.place(relx=0.175, rely=0.4, anchor=tkinter.CENTER)

        self.entry3 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter new description")
        self.__style_input_box(self.entry3)
        self.entry3.place(relx=0.325, rely=0.445, anchor=tkinter.CENTER)

        self.label4 = ctk.CTkLabel(master=self.right_frame, text="New cost: ", font=("Century Gothic", 20, "italic"))
        self.label4.place(relx=0.135, rely=0.525, anchor=tkinter.CENTER)

        self.entry4 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter new cost")
        self.__style_input_box(self.entry4)
        self.entry4.place(relx=0.325, rely=0.57, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="Update", command=(lambda: update_successfully(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button.place(relx=0.5, rely=0.675, anchor=tkinter.CENTER)

        self.button3_frame.pack(pady=20)

        def update_successfully(self):
            input_benefit_name = self.entry1.get()
            new_name = self.entry2.get()
            new_description = self.entry3.get()
            new_cost = self.entry4.get()

            if input_benefit_name == "" or new_name == "" or new_description == "" or new_cost == "":
                msgbox.showerror("Error", "Please fill in all the fields")
            elif not new_name.isalpha():
                msgbox.showerror("Error", "Please enter a valid name")
            elif not new_cost.isdigit():
                msgbox.showerror("Error", "Please enter a valid cost")
            else:
                for bp in the_company.benefits:
                    if bp.name == input_benefit_name:
                        if new_name != "":
                            bp.name = new_name
                            if os.getenv("HRMGR_DB") == "TRUE":
                                benefit_repo.update_one({"name": bp.name}, {"$set": {"name": new_name}})
                        if new_description != "":
                            bp.description = new_description
                            if os.getenv("HRMGR_DB") == "TRUE":
                                benefit_repo.update_one({"name": bp.name}, {"$set": {"description": new_description}})
                        if new_cost != "":
                            bp.cost = new_cost
                            if os.getenv("HRMGR_DB") == "TRUE":
                                benefit_repo.update_one({"name": bp.name}, {"$set": {"cost": new_cost}})
                msgbox.showinfo("Success", "Benefit Plan Updated")

    def __admin_apply_benefit_plan(self):
        self.button5_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button5_frame, text="Apply Benefit Plan", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Benefit Plan Name: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.175, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter name")
        self.__style_input_box(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.label2 = ctk.CTkLabel(master=self.right_frame, text="Employee ID: ", font=("Century Gothic", 20, "italic"))
        self.label2.place(relx=0.135, rely=0.275, anchor=tkinter.CENTER)

        self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
        self.__style_input_box(self.entry2)
        self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="Apply", command=(lambda: apply_successfully(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button.place(relx=0.5, rely=0.425, anchor=tkinter.CENTER)

        self.button5_frame.pack(pady=20)

        def apply_successfully(self):
            input_benefit_id = self.entry1.get()
            input_employee_id = self.entry2.get()

            if input_benefit_id == "" or input_employee_id == "":
                msgbox.showerror("Error", "Please fill in all the fields")
                return

            for bp in the_company.benefits:
                if bp.id != input_benefit_id:
                    continue
                for emp in the_company.employees:
                    if emp.id != input_employee_id:
                        continue
                    emp.benefits.append(bp.name)
                    bp.enrolled_employees.append(emp)
                    msgbox.showinfo("Success", "Benefit Plan applied successfully")
                    if os.getenv("HRMGR_DB") == "TRUE":
                        employee_repo.update_one({"id": emp.id}, {"$set": {"benefits": emp.benefits}})
                        benefit_repo.update_one({"id": bp.id}, {"$set": {"enrolled_employees": bp.enrolled_employees}})
            else:
                msgbox.showerror("Error", "Benefit Plan or Employee does not exist")

    def __admin_view_benefit_plan(self):
        self.button2_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button2_frame, text="View Benefit Plan", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Benefit Plan Name: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.175, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Name")
        self.__style_input_box(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="View", fg_color="purple", command=(lambda: view_benefit(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10)
        self.button.place(relx=0.5, rely=0.295, anchor=tkinter.CENTER)

        self.button2_frame.pack(pady=20)

        def view_benefit(self):
            benefit_name = self.entry1.get()
            benefits = the_company.benefits

            if benefit_name == "":
                msgbox.showerror("Error", "Please fill in all the fields")
            else:
                for bp in benefits:
                    if bp.name == benefit_name:
                        msgbox.showinfo("Benefit Plan", f"Name: {bp.name}\nDescription: {bp.description}\nCost: {bp.cost}")
                        break
                else:
                    msgbox.showerror("Error", "Benefit Plan does not exist")

    def __admin_list_all_plans(self):
        self.button3_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button3_frame, text="List All Benefit Plans", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.button = ctk.CTkButton(master=self.right_frame, text="List", fg_color="purple", command=(lambda: list_benefits(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10)
        self.button.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        self.button3_frame.pack(pady=20)

        def list_benefits(self):
            benefits = the_company.benefits
            if len(benefits) == 0:
                msgbox.showerror("Error", "There are no benefit plans")
            else:
                msgbox.showinfo("Benefit Plans", f"Benefit Plans: {[bp.name for bp in benefits]}")

    # endregion

    # region: employee functions

    def __employee_view_benefit_plan(self):
        self.button2_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button2_frame, text="View Benefit Plan", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Benefit Plan Name: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.175, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Name")
        self.__style_input_box(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="View", fg_color="purple", command=(lambda: view_benefit(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10)
        self.button.place(relx=0.5, rely=0.295, anchor=tkinter.CENTER)

        self.button2_frame.pack(pady=20)

        def view_benefit(self):
            benefit_name = self.entry1.get()
            benefits = the_company.benefits

            if benefit_name == "":
                msgbox.showerror("Error", "Please fill in all the fields")
            else:
                for bp in benefits:
                    if bp.name == benefit_name:
                        msgbox.showinfo("Benefit Plan", f"Name: {bp.name}\nDescription: {bp.description}\nCost: {bp.cost}")
                        break
                else:
                    msgbox.showerror("Error", "Benefit Plan does not exist")

    def __employee_list_all_plans(self):
        self.button3_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button3_frame, text="List All Benefit Plans", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.button = ctk.CTkButton(master=self.right_frame, text="List", fg_color="purple", command=(lambda: list_benefits(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10)
        self.button.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        self.button3_frame.pack(pady=20)

        def list_benefits(self):
            benefits = the_company.benefits
            if len(benefits) == 0:
                msgbox.showerror("Error", "There are no benefit plans")
            else:
                msgbox.showinfo("Benefit Plans", f"Benefit Plans: {[bp.name for bp in benefits]}")

    # endregion
