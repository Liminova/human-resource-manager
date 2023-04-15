import customtkinter as ctk
import tkinter.messagebox as msgbox

from models import Company
from dotenv import load_dotenv

load_dotenv()

the_company = Company()

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
        self.label = ctk.CTkLabel(
            master=self.frame, text="Sign Up", font=("Century Gothic", 30)
        )
        self.label.place(relx=0.5, rely=0.15, anchor="center")

        # create entries
        # entry for username
        self.entry1 = ctk.CTkEntry(
            master=self.frame,
            width=220,
            placeholder_text="Username",
            font=("Century Gothic", 14),
        )
        self.entry1.place(x=50, y=110)

        # entry for password
        self.entry2 = ctk.CTkEntry(
            master=self.frame,
            width=220,
            placeholder_text="Password",
            show="*",
            font=("Century Gothic", 14),
        )
        self.entry2.place(x=50, y=165)

        # entry for confirm password
        self.entry3 = ctk.CTkEntry(
            master=self.frame,
            width=220,
            placeholder_text="Confirm Password",
            show="*",
            font=("Century Gothic", 14),
        )
        self.entry3.place(x=50, y=220)

        # create sign up button
        self.button2 = ctk.CTkButton(
            master=self.frame,
            width=220,
            text="Sign Up",
            command=self.click_signup,
            corner_radius=6,
            font=("Century Gothic", 14),
        )
        self.button2.place(x=50, y=275)

        def callback(event):
            self.click_signin()

        self.label2 = ctk.CTkLabel(
            master=self.frame,
            text="Sign in",
            text_color="cyan",
            font=("Century Gothic", 12, "underline"),
        )
        self.label2.place(x=215, y=315)
        self.label2.bind("<Button-1>", callback)

        self.label3 = ctk.CTkLabel(
            master=self.frame,
            text="Already have an account?",
            font=("Century Gothic", 12),
        )
        self.label3.place(x=50, y=315)

        self.bind("<Return>", lambda event: self.click_signup())

    def first_account(self):
        first_account_is_admin = the_company.employees[0].is_admin
        first_account_name_is_owner = the_company.employees[0].name == "Owner"
        only_one_owner = (
            len(
                [
                    employee
                    for employee in the_company.employees
                    if employee.name == "Owner"
                ]
            )
            == 1
        )
        if not first_account_is_admin:
            msgbox.showerror("Error", "First account is not an admin!")
            raise KeyboardInterrupt
        elif not first_account_name_is_owner:
            msgbox.showerror("Error", "First account name is not 'Owner'!")
            raise KeyboardInterrupt
        elif not only_one_owner:
            msgbox.showerror("Error", "There are more than one 'Owner' account!")
            raise KeyboardInterrupt

    def signup_successfully(self):
        msgbox.showinfo("Sign up", "Sign up successful!")
        self.destroy()

    def get_username(self) -> bool:
        username = self.entry1.get()
        if username == "":
            msgbox.showerror("Error", "Username cannot be empty!")
            return False

        return True

    def get_password(self) -> bool:
        password = self.entry2.get()
        confirm_password = self.entry3.get()
        if password != confirm_password:
            msgbox.showerror("Error", "Password does not match!")
            return False
        elif password == "":
            msgbox.showerror("Error", "Password cannot be empty!")
            return False

        return True

    def click_signup(self):
        if self.get_username() and self.get_password():
            self.signup_successfully()

    def run(self):
        self.mainloop()

    def click_signin(self):
        self.destroy()
        from .login import Login

        window = Login()
        window.run()


if __name__ == "__main__":
    test = Signup().run()
