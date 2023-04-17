import customtkinter as ctk
import tkinter
from tkinter import messagebox
import os

from models import Company, Department
from database.mongo import department_repo, employee_repo
from frontend.helpers import merge_callable

the_company = Company()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

Width = 1024
Height = 768


class DepartmentGui(ctk.CTk):
    def __init__(self, master=None):
        super().__init__()
        self.title("Department Management")
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
            master=self.left_frame, text="Add Department", command=merge_callable(self.__destroy_all_frames, self.__admin_add_department)
        )
        self.__button_style(self.button1)
        self.button1.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(
            master=self.left_frame, text="Remove Department", command=merge_callable(self.__destroy_all_frames, self.__admin_remove_department)
        )
        self.__button_style(self.button2)
        self.button2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.button3 = ctk.CTkButton(
            master=self.left_frame, text="Update Department", command=merge_callable(self.__destroy_all_frames, self.__admin_update_department)
        )
        self.__button_style(self.button3)
        self.button3.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

        self.button4 = ctk.CTkButton(
            master=self.left_frame, text="View Department", command=merge_callable(self.__destroy_all_frames, self.__admin_view_department)
        )
        self.__button_style(self.button4)
        self.button4.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        self.button5 = ctk.CTkButton(
            master=self.left_frame, text="List All Departments", command=merge_callable(self.__destroy_all_frames, self.__admin_list_all_department)
        )
        self.__button_style(self.button5)
        self.button5.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

        self.button6 = ctk.CTkButton(
            master=self.left_frame,
            text="List Employees Without Department",
            command=merge_callable(self.__destroy_all_frames, self.__admin_list_employees_wo_department),
        )
        self.__button_style(self.button6)
        self.button6.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        self.button7 = ctk.CTkButton(
            master=self.left_frame, text="Add Employee", command=merge_callable(self.__destroy_all_frames, self.__admin_add_employee)
        )
        self.__button_style(self.button7)
        self.button7.place(relx=0.5, rely=1.05, anchor=tkinter.CENTER)

        self.button8 = ctk.CTkButton(
            master=self.left_frame, text="Remove Employee", command=merge_callable(self.__destroy_all_frames, self.__admin_remove_employee)
        )
        self.__button_style(self.button8)
        self.button8.place(relx=0.5, rely=1.2, anchor=tkinter.CENTER)

        self.button9 = ctk.CTkButton(master=self.left_frame, text="Back", command=merge_callable(self.__destroy_all_frames, self.__back_to_homepage))
        self.__button_style(self.button9)
        self.button9.place(relx=0.5, rely=1.35, anchor=tkinter.CENTER)

    def employee(self):
        self.button1 = ctk.CTkButton(
            master=self.left_frame, text="View Department", command=merge_callable(self.__destroy_all_frames, self.__employee_view_department)
        )
        self.__button_style(self.button1)
        self.button1.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(
            master=self.left_frame,
            text="List All Departments",
            command=merge_callable(self.__destroy_all_frames, self.__employee_list_all_department),
        )
        self.__button_style(self.button2)
        self.button2.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        self.button3 = ctk.CTkButton(master=self.left_frame, text="Back", command=merge_callable(self.__destroy_all_frames, self.__back_to_homepage))
        self.__button_style(self.button3)
        self.button3.place(relx=0.5, rely=1.35, anchor=tkinter.CENTER)

    def __input_box_style(self, element):
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
    def __admin_add_department(self):
        self.button1_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button1_frame, text="Information", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Department Name: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.185, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Name")
        self.__input_box_style(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.label2 = ctk.CTkLabel(master=self.right_frame, text="Department ID: ", font=("Century Gothic", 20, "italic"))
        self.label2.place(relx=0.155, rely=0.275, anchor=tkinter.CENTER)

        self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
        self.__input_box_style(self.entry2)
        self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="Confirm", command=(lambda: add_successfully(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button.place(relx=0.5, rely=0.425, anchor=tkinter.CENTER)

        self.button1_frame.pack(pady=20)

        def add_successfully(self):
            name = self.entry1.get()
            id = self.entry2.get()
            # create a blank Department object
            new_department = Department()
            if name == "" or id == "":
                messagebox.showerror("Error", "Please fill in all the fields")
            elif not name.isalpha():
                messagebox.showerror("Error", "Please enter a valid name")
            elif not id.isdigit():
                messagebox.showerror("Error", "Please enter a valid ID")
            else:
                # assign values to the department object
                new_department.name = name
                new_department.dept_id = id
                # add the department to the company and database
                the_company.departments.append(new_department)

                if os.getenv("HRMGR_DB") == "TRUE":
                    department_repo.insert_one(new_department.dict(by_alias=True))
                messagebox.showinfo("Success", "Employee added successfully")

    def __admin_remove_department(self):
        self.button2_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button2_frame, text="Remove Department", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Department Name: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.185, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter Name")
        self.__input_box_style(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.label2 = ctk.CTkLabel(master=self.right_frame, text="Department ID: ", font=("Century Gothic", 20, "italic"))
        self.label2.place(relx=0.155, rely=0.275, anchor=tkinter.CENTER)

        self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
        self.__input_box_style(self.entry2)
        self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="Remove", command=(lambda: remove_successfully(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="red")
        self.button.place(relx=0.5, rely=0.425, anchor=tkinter.CENTER)

        self.button2_frame.pack(pady=20)

        def remove_successfully(self):
            name = self.entry1.get()
            id = self.entry2.get()

            departments = the_company.departments

            if name == "" or id == "":
                messagebox.showerror("Error", "Please fill in all the fields")
            elif not name.isalpha():
                messagebox.showerror("Error", "Please enter a valid name")
            elif not id.isdigit():
                messagebox.showerror("Error", "Please enter a valid ID")
            else:
                for department in departments:
                    if department.name == name and department.dept_id == id:
                        the_company.departments.remove(department)
                        if os.getenv("HRMGR_DB") == "TRUE":
                            department_repo.delete_one({"name": name, "id": id})
                        break
                messagebox.showinfo("Success", "Department removed successfully")

    def __admin_update_department(self):
        self.button3_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button3_frame, text="Update Department", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label0 = ctk.CTkLabel(
            master=self.right_frame, text="(You are currently update the information of: ) ", font=("Century Gothic", 14, "italic")
        )
        self.label0.place(relx=0.5, rely=0.095, anchor=tkinter.CENTER)

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Old Name: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.135, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter old name")
        self.__input_box_style(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.label2 = ctk.CTkLabel(master=self.right_frame, text="Old ID: ", font=("Century Gothic", 20, "italic"))
        self.label2.place(relx=0.105, rely=0.275, anchor=tkinter.CENTER)

        self.entry2 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter old ID")
        self.__input_box_style(self.entry2)
        self.entry2.place(relx=0.325, rely=0.32, anchor=tkinter.CENTER)

        self.label3 = ctk.CTkLabel(master=self.right_frame, text="New name: ", font=("Century Gothic", 20, "italic"))
        self.label3.place(relx=0.135, rely=0.4, anchor=tkinter.CENTER)

        self.entry3 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter new name")
        self.__input_box_style(self.entry3)
        self.entry3.place(relx=0.325, rely=0.445, anchor=tkinter.CENTER)

        self.label4 = ctk.CTkLabel(master=self.right_frame, text="New ID: ", font=("Century Gothic", 20, "italic"))
        self.label4.place(relx=0.105, rely=0.525, anchor=tkinter.CENTER)

        self.entry4 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter new ID")
        self.__input_box_style(self.entry4)
        self.entry4.place(relx=0.325, rely=0.57, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="Update", command=(lambda: update_successfully(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button.place(relx=0.5, rely=0.685, anchor=tkinter.CENTER)

        self.button3_frame.pack(pady=20)

        def update_successfully(self):
            name = self.entry1.get()
            id = self.entry2.get()
            new_name = self.entry3.get()
            new_id = self.entry4.get()

            departments = the_company.departments

            # if exist new_name or new_id -> update them. if it doesn't exist, skip
            if name == "" or id == "":
                messagebox.showerror("Error", "Please fill in all the fields")
            elif not name.isalpha():
                messagebox.showerror("Error", "Please enter a valid name")
            elif not id.isdigit():
                messagebox.showerror("Error", "Please enter a valid ID")
            else:
                for department in departments:
                    if department.name == name and department.dept_id == id:
                        if new_name != "":
                            department.name = new_name
                            if os.getenv("HRMGR_DB") == "TRUE":
                                department_repo.update_one({"name": name, "dept_id": id}, {"$set": {"name": new_name}})
                        if new_id != "":
                            department.dept_id = new_id
                            if os.getenv("HRMGR_DB") == "TRUE":
                                department_repo.update_one({"name": name, "dept_id": id}, {"$set": {"dept_id": new_id}})
                        break
                messagebox.showinfo("Success", "Department updated successfully")

    def __admin_view_department(self):
        self.button2_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button2_frame, text="View Department", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Department ID: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.155, rely=0.15, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
        self.__input_box_style(self.entry1)
        self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="View", fg_color="purple", command=(lambda: view(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10)
        self.button.place(relx=0.5, rely=0.295, anchor=tkinter.CENTER)

        self.button2_frame.pack(pady=20)

        def view(self):
            id = self.entry1.get()
            departments = the_company.departments
            if id == "":
                messagebox.showerror("Error", "Please enter a valid ID")
            else:
                for department in departments:
                    if department.dept_id == id:
                        messagebox.showinfo("Department", f"{department}")
                        break
                else:
                    messagebox.showerror("Error", "Department not found")

    def __admin_add_employee(self):
        self.button3_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button3_frame, text="Add Employee", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Select Department: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.155, rely=0.15, anchor=tkinter.CENTER)

        self.combobox = ctk.CTkComboBox(master=self.right_frame)
        self.combobox["values"] = [department.name for department in the_company.departments]
        self.combobox.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.label2 = ctk.CTkLabel(master=self.right_frame, text="Employee ID: ", font=("Century Gothic", 20, "italic"))
        self.label2.place(relx=0.155, rely=0.25, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
        self.__input_box_style(self.entry1)
        self.entry1.place(relx=0.325, rely=0.295, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="Add", command=lambda self=self: added_successfully(self))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button.place(relx=0.5, rely=0.395, anchor=tkinter.CENTER)

        self.button3_frame.pack(pady=20)

        def added_successfully(self):
            employee_id = self.entry1.get()
            employee = the_company.employees.index(employee_id)
            departments = the_company.departments
            if employee_id == "":
                messagebox.showerror("Error", "Please enter a valid employee ID")
                return

            for department in departments:
                if department.name != self.combobox.get():
                    continue

                # add employee to department and update database
                department.members.append(the_company.employees[employee])
                if os.getenv("HRMGR_DB") == "TRUE":
                    department_repo.update_one({"name": department.name}, {"$push": {"employees": id}})

                # update employee's department and update database
                the_company.employees[employee].department_id = department.name
                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one({"_id": the_company.employees[employee].id}, {"$set": department.dict(include={"dept_id"})})

                messagebox.showinfo("Success", "Employee added successfully")

    def __admin_remove_employee(self):
        self.button4_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button4_frame, text="Remove Employee", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Select Department: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.155, rely=0.15, anchor=tkinter.CENTER)

        self.combobox = ctk.CTkComboBox(master=self.right_frame)
        self.combobox["values"] = [department.name for department in the_company.departments]
        self.combobox.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

        self.label2 = ctk.CTkLabel(master=self.right_frame, text="Employee ID: ", font=("Century Gothic", 20, "italic"))
        self.label2.place(relx=0.155, rely=0.25, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
        self.__input_box_style(self.entry1)
        self.entry1.place(relx=0.325, rely=0.295, anchor=tkinter.CENTER)

        self.button = ctk.CTkButton(master=self.right_frame, text="Remove", command=(lambda: removed_successfully(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button.place(relx=0.5, rely=0.395, anchor=tkinter.CENTER)

        self.button4_frame.pack(pady=20)

        def removed_successfully(self):
            employee_id = self.entry1.get()
            departments = the_company.departments
            employee = [employee for employee in the_company.employees if employee.employee_id == employee_id][0]

            if employee_id == "":
                messagebox.showerror("Error", "Please enter a valid employee ID")
                return

            if employee.department_id == "":
                messagebox.showerror("Error", "Employee is not in any department")
                return

            for department in departments:
                if department.name != self.combobox.get():
                    continue

                # remove employee from department and update database
                department.members.remove([employee for employee in department.members if employee.id == employee_id][0])
                if os.getenv("HRMGR_DB") == "TRUE":
                    department_repo.update_one({"name": department.name}, {"$pull": {"employees": id}}, upsert=True)

                # remove department_id from employee and update database
                employee.department_id = ""
                if os.getenv("HRMGR_DB") == "TRUE":
                    employee_repo.update_one({"_id": employee.id}, {"$set": employee.dict(include={"dept_id"})}, upsert=True)
            messagebox.showinfo("Success", "Employee removed successfully")

    def __admin_list_all_department(self):
        self.button5_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button5_frame, text="List All Departments", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.button = ctk.CTkButton(master=self.right_frame, text="List", command=(lambda: list_departments(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button.place(relx=0.5, rely=0.395, anchor=tkinter.CENTER)

        self.button5_frame.pack(pady=20)

        def list_departments(self):
            departments = the_company.departments
            if len(departments) == 0:
                messagebox.showerror("Error", "No departments found")
            else:
                messagebox.showinfo("Departments", "Departments: " + ", ".join([department.name for department in departments]))

    def __admin_list_employees_wo_department(self):
        self.button6_frame = ctk.CTkFrame(master=self.right_frame)

        self.label = ctk.CTkLabel(master=self.button6_frame, text="List Employees Without Department", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.button = ctk.CTkButton(master=self.right_frame, text="List", command=(lambda: list_employees(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10, fg_color="purple")
        self.button.place(relx=0.5, rely=0.395, anchor=tkinter.CENTER)

        self.button6_frame.pack(pady=20)

        def list_employees(self):
            employees = the_company.employees
            if len(employees) == 0:
                messagebox.showerror("Error", "No employees found")
            else:
                messagebox.showinfo(
                    "Employees", "Employees: " + ", ".join([employee.employee_id for employee in employees if employee.department_id == ""])
                )

    # endregion

    # region: employee functions
    def __employee_view_department(self):
        self.button1_frame = ctk.CTkFrame(master=self.right_frame, corner_radius=10)
        self.label = ctk.CTkLabel(master=self.button1_frame, text="View Department", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.label1 = ctk.CTkLabel(master=self.right_frame, text="Department ID: ", font=("Century Gothic", 20, "italic"))
        self.label1.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.right_frame, placeholder_text="Enter ID")
        self.__input_box_style(self.entry1)
        self.entry1.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.button1 = ctk.CTkButton(master=self.right_frame, text="View", fg_color="purple", command=(lambda: view(self)))
        self.button.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10)
        self.button1.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        self.button1_frame.pack()

        def view(self):
            id = self.entry1.get()
            departments = the_company.departments
            if id == "":
                messagebox.showerror("Error", "Please enter a valid ID")
            else:
                for department in departments:
                    if department.dept_id == id:
                        messagebox.showinfo("Department", f"{department}")
                        break
                else:
                    messagebox.showerror("Error", "Department not found")

    def __employee_list_all_department(self):
        self.button2_frame = ctk.CTkFrame(master=self.right_frame, corner_radius=10)
        self.label = tkinter.Label(master=self.button2_frame, text="List All Departments", font=("Century Gothic", 30, "bold"))
        self.label.pack()

        self.button2 = ctk.CTkButton(master=self.right_frame, text="List", fg_color="purple", command=(lambda: list_departments(self)))
        self.button2.configure(width=100, height=40, font=("Century Gothic", 15, "bold"), corner_radius=10)
        self.button2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.button2_frame.pack()

        def list_departments(self):
            departments = the_company.departments
            if len(departments) == 0:
                messagebox.showerror("Error", "No departments found")
            else:
                messagebox.showinfo("Departments", "Departments: " + ", ".join([department.name for department in departments]))

    # endregion
