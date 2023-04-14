import customtkinter as ctk
import tkinter
from tkinter import messagebox

from .homepage import Homepage
from .signup import Signup

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
        self.frame = ctk.CTkFrame(master=self, width=320, height=360, corner_radius=20)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # create labels

        # sign in label
        self.label = ctk.CTkLabel(
            master=self.frame, text="Sign In", font=("Century Gothic", 30)
        )
        self.label.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        # self.label1 = ctk.CTkLabel(master=self.frame, text="Forgot password?", font=('Century Gothic', 12))
        # self.label1.place(x=155, y=195)

        # "here" label link to sign up page
        def callback(event):
            self.click_signup()

        self.label2 = ctk.CTkLabel(
            master=self.frame,
            text="Sign up",
            text_color="cyan",
            font=("Century Gothic", 12, "underline"),
        )
        self.label2.place(x=200, y=270)
        self.label2.bind("<Button-1>", callback)

        self.label3 = ctk.CTkLabel(
            master=self.frame,
            text="Don't have an account?",
            font=("Century Gothic", 12),
        )
        self.label3.place(x=50, y=270)

        # create entries
        # username entry
        self.entry1 = ctk.CTkEntry(
            master=self.frame,
            width=220,
            placeholder_text="Username",
            font=("Century Gothic", 14),
        )
        self.entry1.place(x=50, y=110)

        # password entry
        self.entry2 = ctk.CTkEntry(
            master=self.frame,
            width=220,
            placeholder_text="Password",
            show="*",
            font=("Century Gothic", 14),
        )
        self.entry2.place(x=50, y=165)

        # create sign in button
        self.button1 = ctk.CTkButton(
            master=self.frame,
            width=220,
            text="Sign in",
            command=self.login_successfully,
            corner_radius=6,
            font=("Century Gothic", 14),
        )
        self.button1.place(x=50, y=220)

        # listen for enter key
        self.bind("<Return>", lambda event: self.login_successfully())

    def signup(self):
        self.destroy()

    def run(self):
        self.mainloop()

    def login_successfully(self):
        username = self.entry1.get()
        password = self.entry2.get()
        if username == "" or password == "":
            messagebox.showerror("Error", "Please fill in all the fields")
        elif username == "admin" and password == "admin":
            self.destroy()
            Homepage().run()
        else:
            messagebox.showerror("Error", "Incorrect username or password")

    def click_signup(self):
        Signup.signup().run()
