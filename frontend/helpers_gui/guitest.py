import customtkinter
import tkinter
from tkinter import messagebox

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("925x600")
app.resizable(True, True)
app.title("Human Resources System Management")


def button_function():
    username = entry1.get()
    password = entry2.get()
    if username == "admin" and password == "1234":
        w = customtkinter.CTk()
        w.geometry("1024x768")
        w.title("Welcome")
        l1 = customtkinter.CTkLabel(master=w, text="Home Page", font=("Century Gothic", 60))
        l1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        w.mainloop()
    elif username == "admin" and password != "1234":
        messagebox.showerror("Login", "Password is incorrect")
    else:
        messagebox.showerror("Login", "Login Failed")


frame = customtkinter.CTkFrame(master=app, width=320, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

l2 = customtkinter.CTkLabel(master=frame, text="Sign In", font=("Century Gothic", 30))
l2.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="Username", font=("Century Gothic", 14))
entry1.place(x=50, y=110)

entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="Password", show="*", font=("Century Gothic", 14))
entry2.place(x=50, y=165)

l3 = customtkinter.CTkLabel(master=frame, text="Forget password?", font=("Century Gothic", 12))
l3.place(x=155, y=195)

button1 = customtkinter.CTkButton(
    master=frame, width=220, text="Login", command=button_function, corner_radius=6, font=("Century Gothic", 14)
)
button1.place(x=50, y=240)

l4 = customtkinter.CTkLabel(master=frame, text="Don't have an account? Sign up", font=("Century Gothic", 12))
l4.place(x=50, y=300)

app.mainloop()
