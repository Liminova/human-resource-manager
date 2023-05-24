import os
import tkinter.messagebox as msgbox

import customtkinter as ctk
from dotenv import load_dotenv

from database.mongo import employee_repo
from models import Company, Employee, hash

from .homepage import Homepage

the_company = Company()

load_dotenv()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

appWidth = 400
appHeight = 500


class Signup(ctk.CTk):
    def __init__(self, master=None):
        super().__init__()

        self.title("Human Resources Information System Management")
        self.geometry(f"{appWidth}x{appHeight}")
        self.resizable(True, True)

        # create a frame
        self.frame = ctk.CTkFrame(master=self, width=320, height=400, corner_radius=20)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # create label
        ctk.CTkLabel(master=self.frame, text="Sign Up", font=("Century Gothic", 30)).place(
            relx=0.5, rely=0.15, anchor="center"
        )

        # create entries
        # entry for username
        self.input_username = ctk.CTkEntry(
            master=self.frame, width=220, placeholder_text="Username", font=("Century Gothic", 14)
        )
        self.input_username.place(x=50, y=110)

        # entry for password
        self.input_password = ctk.CTkEntry(
            master=self.frame, width=220, placeholder_text="Password", show="*", font=("Century Gothic", 14)
        )
        self.input_password.place(x=50, y=165)

        # entry for confirm password
        self.confirm_password = ctk.CTkEntry(
            master=self.frame, width=220, placeholder_text="Confirm Password", show="*", font=("Century Gothic", 14)
        )
        self.confirm_password.place(x=50, y=220)

        # create sign up button
        ctk.CTkButton(
            master=self.frame,
            width=220,
            text="Sign Up",
            command=self.click_signup,
            corner_radius=6,
            font=("Century Gothic", 14),
        ).place(x=50, y=275)

        self.bind("<Return>", lambda event: self.click_signup())

    def get_username(self) -> bool:
        username = self.input_username.get()
        if username == "":
            msgbox.showerror("Error", "Username cannot be empty!")
            return False
        self.__input_username = username
        return True

    def get_password(self) -> bool:
        password = self.input_password.get()
        confirm_password = self.confirm_password.get()
        if password != confirm_password:
            msgbox.showerror("Error", "Password does not match!")
            return False
        elif password == "":
            msgbox.showerror("Error", "Password cannot be empty!")
            return False
        self.__input_hashed_password = hash(username=self.__input_username, password=password)
        return True

    def click_signup(self):
        if self.get_username() and self.get_password():
            msgbox.showinfo("Sign up", "Sign up successful!")
            self.create_owner()

            if os.getenv("HRMGR_DB") == "TRUE":
                confirm = msgbox.askyesno("Confirm", "Do you want to generate random data into the database?")
                if confirm:
                    from test.randomize_db import generate_random_data_into_db

                    generate_random_data_into_db()

            self.destroy()

    def click_signin(self):
        self.destroy()
        from .login import Login

        Login().mainloop()

    def create_owner(self):
        owner = Employee()
        owner.employee_id = self.__input_username
        owner.hashed_password = self.__input_hashed_password
        owner.is_admin = True
        owner.name = "Owner"

        the_company.employees.append(owner)
        the_company.logged_in_employee = owner

        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.insert_one(owner.dict(by_alias=True))

        self.destroy()
        Homepage().mainloop()


if __name__ == "__main__":
    Signup().mainloop()
