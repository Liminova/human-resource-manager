import tkinter
from tkinter import messagebox

import customtkinter as ctk
from dotenv import load_dotenv

from models import Company, hash

from .homepage import Homepage

the_company = Company()

load = load_dotenv()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

appWidth = 400
appHeight = 500


class Login(ctk.CTk):
    def __init__(self, master=None):
        super().__init__()

        # set title and size of the window
        self.title("Human Resources Information System Management")
        self.geometry(f"{appWidth}x{appHeight}")
        self.resizable(True, True)

        # create a frame
        main_frame = ctk.CTkFrame(master=self, width=320, height=360, corner_radius=20)
        main_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # sign in label
        ctk.CTkLabel(master=main_frame, text="Sign In", font=("Century Gothic", 30)).place(
            relx=0.5, rely=0.15, anchor=tkinter.CENTER
        )

        # NOTE: we don't allow employees to sign up, they are added by the admin
        ctk.CTkLabel(
            master=main_frame, text="Contact the HR", text_color="cyan", font=("Century Gothic", 12, "underline")
        ).place(x=200, y=270)

        ctk.CTkLabel(master=main_frame, text="Don't have an account?", font=("Century Gothic", 12)).place(x=50, y=270)

        # create entries
        input_style = dict(font=("Century Gothic", 14), width=220)
        input_username = ctk.CTkEntry(master=main_frame, placeholder_text="Username", **input_style)
        input_username.place(x=50, y=110)
        input_password = ctk.CTkEntry(master=main_frame, placeholder_text="Password", show="*", **input_style)
        input_password.place(x=50, y=165)

        self.data = {"username": input_username, "password": input_password}

        # create sign in button
        ctk.CTkButton(
            master=main_frame,
            width=220,
            text="Sign in",
            command=self.login_button_handler,
            corner_radius=6,
            font=("Century Gothic", 14),
        ).place(x=50, y=220)
        self.bind("<Return>", lambda _: self.login_button_handler())

    def login_button_handler(self):
        username, password = self.data["username"].get(), self.data["password"].get()

        if username == "" or password == "":
            messagebox.showerror("Error", "Please enter username and password")
            return

        hashed_password = hash(username=username, password=password)
        is_logged_in = False
        for employee in the_company.employees:
            if (employee.employee_id == username) and (employee.hashed_password == hashed_password):
                is_logged_in = True
                the_company.logged_in_employee = employee
                break

        if is_logged_in is True:
            self.destroy()
            Homepage().mainloop()
        else:
            messagebox.showerror("Error", "Incorrect username or password")


if __name__ == "__main__":
    Login().mainloop()
