import os
import tkinter
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox

from models import Company
from database.mongo import employee_repo
from frontend.helpers_gui import *
from frontend.helpers_gui.global_styling import *

the_company = Company()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

Width = 1024
Height = 768


class AttendanceGui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Attendance Management")
        self.geometry(f"{Width}x{Height}")
        self.resizable(False, False)
        self.left_frame = ctk.CTkFrame(master=self, corner_radius=10)

        self.admin() if the_company.logged_in_employee.is_admin else self.employee()

        self.left_frame.pack(side=ctk.LEFT)
        self.left_frame.pack_propagate(False)
        self.left_frame.configure(width=320, height=760)

        self.right_frame = ctk.CTkFrame(master=self)
        self.right_frame.pack(side=ctk.RIGHT, expand=True)
        self.right_frame.pack_propagate(False)

    def admin(self):
        pos = Position(x=0.5, y=0.0, increment_by_x=0, increment_by_y=0.1)

        ctk.CTkButton(
            master=self.left_frame,
            text="Check",
            command=merge_callable(self.__destroy_all_frames, self.__attendance_check),
            **btn_menu_style,
        ).place(relx=pos.x, rely=pos.y, anchor=tkinter.CENTER)

        ctk.CTkButton(
            master=self.left_frame,
            text="Update",
            command=merge_callable(self.__destroy_all_frames, self.__admin_attendance_update),
            **btn_menu_style,
        ).place(relx=pos.x, rely=pos.y, anchor=tkinter.CENTER)

        ctk.CTkButton(
            master=self.left_frame,
            text="Get report",
            command=merge_callable(self.__destroy_all_frames, self.__admin_attendance_report),
            **btn_menu_style,
        ).place(relx=pos.x, rely=pos.y, anchor=tkinter.CENTER)

        ctk.CTkButton(master=self.left_frame, text="Back", command=self.__back_to_homepage, **btn_exit_style).place(
            relx=pos.x, rely=0.9, anchor=tkinter.CENTER
        )

    def employee(self):
        pos = Position(x=0.5, y=0.0, increment_by_x=0, increment_by_y=0.1)

        ctk.CTkButton(
            master=self.left_frame,
            text="Check",
            command=merge_callable(self.__destroy_all_frames, self.__attendance_check),
            **btn_menu_style,
        ).place(relx=pos.x, rely=pos.y, anchor=tkinter.CENTER)

        ctk.CTkButton(
            master=self.left_frame,
            text="Get report",
            command=merge_callable(self.__destroy_all_frames, self.__employee_attendance_report),
            **btn_menu_style,
        ).place(relx=pos.x, rely=pos.y, anchor=tkinter.CENTER)

        ctk.CTkButton(master=self.left_frame, text="Back", command=self.__back_to_homepage, **btn_exit_style).place(
            relx=pos.x, rely=0.9, anchor=tkinter.CENTER
        )

    def __destroy_all_frames(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def __back_to_homepage(self):
        from .homepage import Homepage

        self.destroy()
        Homepage().mainloop()

    def __attendance_check(self):
        logged_in_employee = the_company.logged_in_employee
        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        ctk.CTkLabel(master=main_frame, text="Attendance Check", **label_title_style).grid(
            row=0, column=0, columnspan=2, pady=20, padx=20
        )

        ctk.CTkLabel(master=main_frame, text="Date", **label_desc_style).grid(row=1, column=0, pady=20, padx=20)
        today: str = datetime.now().strftime("%Y-%m-%d")

        ctk.CTkLabel(master=main_frame, text=today, **label_desc_style).grid(row=1, column=1, pady=20, padx=20)

        if today not in logged_in_employee.attendance.attendances:
            logged_in_employee.attendance.attendances[today] = False

        _status: bool = the_company.logged_in_employee.attendance.attendances[today]
        status: str = "Present" if _status else "Absent"
        ctk.CTkLabel(master=main_frame, text="Status", **label_desc_style).grid(row=2, column=0, pady=20, padx=20)
        status_label = ctk.CTkLabel(master=main_frame, text=status, **label_desc_style)
        status_label.grid(row=2, column=1, pady=20, padx=20)

        def _check_attendance():
            logged_in_employee = the_company.logged_in_employee
            nonlocal today
            nonlocal status_label
            if logged_in_employee.attendance.attendances[today]:
                messagebox.showinfo("Present", f"You are already present today ({today})")
                return

            status_label.configure(text="Present")
            logged_in_employee.attendance.attendances[today] = True
            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.update_one(
                    {"_id": logged_in_employee.id}, {"$set": logged_in_employee.dict(include={"attendance"})}, upsert=True
                )

        ctk.CTkButton(master=main_frame, text="Check", command=_check_attendance, **btn_action_style).grid(
            row=3, column=0, pady=20, padx=20, columnspan=2
        )

    def __admin_attendance_update(self):
        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        ctk.CTkLabel(master=main_frame, text="Attendance Update", **label_title_style).grid(
            row=0, column=0, columnspan=2, pady=(20, 0)
        )

        # Select employee from a list
        radio_empl_idx_select: ctk.Variable = ctk.IntVar(value=0)
        empl_items = tuple(f"{empl.employee_id} - {empl.name}" for empl in the_company.employees)
        _display_list = display_list(
            _master=main_frame, options=empl_items, returned_idx=[radio_empl_idx_select], selectable=True
        )
        if _display_list[0] is False:
            ctk.CTkLabel(master=main_frame, text="No employee found", **label_desc_style).grid(
                row=1, column=0, columnspan=2, pady=20, padx=20
            )

        # Input date
        ctk.CTkLabel(master=main_frame, text="Date: ", **label_desc_style).grid(row=2, column=0, sticky=tkinter.W, padx=20)
        input_date = ctk.CTkEntry(master=main_frame, placeholder_text="YYYY-MM-DD", **input_box_style)
        input_date.grid(row=2, column=1, sticky=tkinter.W, pady=5, padx=20)

        # Select present or absent
        radio_is_present: ctk.Variable = ctk.BooleanVar(value=True)
        ctk.CTkLabel(master=main_frame, text="Status: ", **label_desc_style).grid(row=3, column=0, sticky=tkinter.W, padx=20)
        ctk.CTkRadioButton(master=main_frame, text="Present", variable=radio_is_present, value=True).grid(
            row=3, column=1, sticky=tkinter.W, pady=5, padx=20
        )
        ctk.CTkRadioButton(master=main_frame, text="Absent", variable=radio_is_present, value=False).grid(
            row=4, column=1, sticky=tkinter.W, pady=5, padx=20
        )

        # Update button + handler
        data = {"is_present": radio_is_present, "empl_idx": radio_empl_idx_select, "date": input_date}

        def _attendance_update():
            nonlocal data
            empls = the_company.employees
            empl_idx: int = data["empl_idx"].get()
            date: str = data["date"].get()
            is_present: bool = data["is_present"].get()

            # Try to validate the date
            try:
                date = datetime.strftime(datetime.strptime(date, "%Y-%m-%d"), "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date, please enter in YYYY-MM-DD format")
                return

            # get the employee object
            empl = empls[empl_idx]

            if not the_company.can_modify("attendance", empl):
                messagebox.showerror("Error", "You don't have the permission to modify this employee's attendance")
                return

            # update the attendance
            empl.attendance.attendances[date] = is_present

            # show success message and update the database
            messagebox.showinfo(
                "Success", f"Attendance for {empl.name} on {date} updated to {'Present' if is_present else 'Absent'}"
            )
            if os.getenv("HRMGR_DB") == "TRUE":
                employee_repo.update_one(
                    {"_id": empls[empl_idx].id}, {"$set": empls[empl_idx].dict(include={"attendance"})}, upsert=True
                )

        ctk.CTkButton(master=main_frame, text="Update", command=_attendance_update, **btn_action_style).grid(
            row=5, column=0, columnspan=2, pady=20
        )

    def __admin_attendance_report(self):
        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        # Title for the page
        ctk.CTkLabel(master=main_frame, text="Attendance Report", **label_title_style).grid(
            row=0, column=0, pady=20, padx=20
        )

        # Select employee from a list
        radio_empl_idx_select: ctk.Variable = ctk.IntVar(value=0)
        empl_items = tuple(f"{empl.employee_id} - {empl.name}" for empl in the_company.employees)
        err = display_list(
            _master=main_frame, options=empl_items, selectable=True, returned_idx=[radio_empl_idx_select], page_size=9
        )
        if err is None:
            messagebox.showerror("Error", "No employees found")

        # Generate report button + handler
        def _get_report():
            nonlocal radio_empl_idx_select
            nonlocal main_frame
            nonlocal btn_action_report
            nonlocal self

            # Get the selected employee
            empl_idx = radio_empl_idx_select.get()

            # Destroy the current report frame
            main_frame.destroy()

            # Create a new frame for the report
            main_frame = ctk.CTkFrame(master=self.right_frame)
            main_frame.grid(row=0, column=0)
            ctk.CTkLabel(
                master=main_frame, text="Attendance Report for " + the_company.employees[empl_idx].name, **label_title_style
            ).grid(row=0, column=0, pady=20, padx=20)

            # Display the report
            _attendances = the_company.employees[empl_idx].attendance.attendances
            attendance_items = tuple(
                f"{date} - {'Present' if is_present else 'Absent'}" for date, is_present in _attendances.items()
            )
            display_list(
                _master=main_frame, options=attendance_items, selectable=False, page_size=9, err_msg="No attendance found"
            )

            # Create a new button to go back to the attendance report page
            ctk.CTkButton(
                master=main_frame,
                text="Back",
                command=merge_callable(main_frame.destroy, self.__admin_attendance_report),
                **btn_action_style,
            ).grid(row=2, column=0, pady=20)

        btn_action_report = ctk.CTkButton(master=main_frame, text="Report", command=_get_report, **btn_action_style)
        btn_action_report.grid(row=2, column=0, pady=20)

    def __employee_attendance_report(self):
        main_frame = ctk.CTkFrame(master=self.right_frame)
        main_frame.grid(row=0, column=0)

        # Title for the page
        ctk.CTkLabel(
            master=main_frame, text=f"Attendance Report for {the_company.logged_in_employee.name}", **label_title_style
        ).grid(row=0, column=0, pady=(20, 0), padx=20)

        # Display the report
        _attendances = the_company.logged_in_employee.attendance.attendances
        attendance_items = tuple(
            f"{date} - {'Present' if is_present else 'Absent'}" for date, is_present in _attendances.items()
        )
        display_list(
            _master=main_frame, options=attendance_items, selectable=False, page_size=9, err_msg="No attendance found"
        )
