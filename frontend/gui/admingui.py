# Admin GUI: impolement add benefit plan, remove benefit plan, view requests, accept benefit enrollment, decline benefit enrollment, remove benefit enrollment

import customtkinter
from customtkinter import *
from tkinter import messagebox
from models.admin import Admin
from models.company import Company
from models.benefits import BenefitPlan
from typing import List, Tuple, Callable, Any

class AdminGUI:
    def __init__(self, company: Company):
        self.__company = company
        self.__admin = Admin()
        self.__benefits = company.benefits

    def start(self) -> Tuple[bool, str]:
        self.__root = Tk()
        self.__root.title("Admin Menu")
        self.__root.geometry("500x500")
        self.__root.resizable(False, False)

        self.__frame = Frame(self.__root)
        self.__frame.pack(fill=BOTH, expand=True)

        self.__main_menu = [
            ("Add benefit plan", self.__add),
            ("Remove benefit plan", self.__remove),
            ("View requests", self.__view),
            ("Accept benefit enrollment", self.__accept),
            ("Decline benefit enrollment", self.__decline),
            ("Remove benefit enrollment", self.__remove_benefit),
            ("Exit", self.__exit),
        ]

        self.__last_msg = ""
        self.__last_msg_label = Label(self.__frame, text=self.__last_msg)
        self.__last_msg_label.pack()

        self.__buttons = []
        for text, command in self.__main_menu:
            button = Button(self.__frame, text=text, command=command)
            button.pack(fill=X, expand=True)
            self.__buttons.append(button)

        self.__root.mainloop()

    def __add(self) -> None:
        self.__root.destroy()
        self.__root = Tk()
        self.__root.title("Add Benefit Plan")
        self.__root.geometry("500x500")
        self.__root.resizable(False, False)

        self.__frame = Frame(self.__root)
        self.__frame.pack(fill=BOTH, expand=True)

        self.__last_msg = ""
        self.__last_msg_label = Label(self.__frame, text=self.__last_msg)
        self.__last_msg_label.pack()

        self.__input_fields = [
            ("Enter benefit plan name: ", self.__set_name),
            ("Enter benefit plan description: ", self.__set_description),
            ("Enter benefit plan cost: ", self.__set_cost),
        ]

        self.__input_entries = []
        for text, command in self.__input_fields:
            label = Label(self.__frame, text=text)
            label.pack()
            entry = Entry(self.__frame)
            entry.pack()
            self.__input_entries.append(entry)

        self.__buttons = []
        button = Button(self.__frame, text="Submit", command=self.__submit)
        button.pack(fill=X, expand=True)
        self.__buttons.append(button)

        self.__root.mainloop()

    def __set_name(self, name: str) -> None:
        self.__name = name

    def __set_description(self, description: str) -> None:
        self.__description = description

    def __set_cost(self, cost: float) -> None:
        self.__cost = cost

    def __submit(self) -> None:
        name = self.__input_entries[0].get()
        description = self.__input_entries[1].get()
        cost = self.__input_entries[2].get()
        try:
            cost = float(cost)
        except ValueError:
            messagebox.showerror("Error", "Cost must be a number")
            return
        self.__admin.add_benefit_plan(self.__company, name, description, cost)
        self.__last_msg = "Benefit plan added"
        self.__last_msg_label.config(text=self.__last_msg)

    def __remove(self) -> None:
        self.__root.destroy()
        self.__root = Tk()
        self.__root.title("Remove Benefit Plan")
        self.__root.geometry("500x500")
        self.__root.resizable(False, False)

        self.__frame = Frame(self.__root)
        self.__frame.pack(fill=BOTH, expand=True)

        self.__last_msg = ""
        self.__last_msg_label = Label(self.__frame, text=self.__last_msg)
        self.__last_msg_label.pack()

        self.__input_fields = [
            ("Enter benefit plan name: ", self.__set_name),
        ]

        self.__input_entries = []
        for text, command in self.__input_fields:
            label = Label(self.__frame, text=text)
            label.pack()
            entry = Entry(self.__frame)
            entry.pack()
            self.__input_entries.append(entry)

        self.__buttons = []
        button = Button(self.__frame, text="Submit", command=self.__submit)
        button.pack(fill=X, expand=True)
        self.__buttons.append(button)

        self.__root.mainloop()

    def __submit(self) -> None:
        name = self.__input_entries[0].get()
        self.__admin.remove_benefit_plan(self.__company, name)
        self.__last_msg = "Benefit plan removed"
        self.__last_msg_label.config(text=self.__last_msg)

    def __view(self) -> None:
        self.__root.destroy()
        self.__root = Tk()
        self.__root.title("View Requests")
        self.__root.geometry("500x500")
        self.__root.resizable(False, False)

        self.__frame = Frame(self.__root)
        self.__frame.pack(fill=BOTH, expand=True)

        self.__last_msg = ""
        self.__last_msg_label = Label(self.__frame, text=self.__last_msg)
        self.__last_msg_label.pack()

        self.__buttons = []
        button = Button(self.__frame, text="View", command=self.__view_requests)
        button.pack(fill=X, expand=True)
        self.__buttons.append(button)

        self.__root.mainloop()

    def __view_requests(self) -> None:
        self.__root.destroy()
        self.__root = Tk()
        self.__root.title("View Requests")
        self.__root.geometry("500x500")
        self.__root.resizable(False, False)

        self.__frame = Frame(self.__root)
        self.__frame.pack(fill=BOTH, expand=True)

        self.__last_msg = ""
        self.__last_msg_label = Label(self.__frame, text=self.__last_msg)
        self.__last_msg_label.pack()

        self.__requests = self.__admin.view_requests(self.__company)
        self.__request_buttons = []
        for request in self.__requests:
            button = Button(self.__frame, text=request, command=self.__view_request(request))
            button.pack(fill=X, expand=True)
            self.__request_buttons.append(button)

        self.__root.mainloop()

    def __view_request(self, request: str) -> None: 
        self.__root.destroy()
        self.__root = Tk()
        self.__root.title("View Request")
        self.__root.geometry("500x500")
        self.__root.resizable(False, False)

        self.__frame = Frame(self.__root)
        self.__frame.pack(fill=BOTH, expand=True)

        self.__last_msg = ""
        self.__last_msg_label = Label(self.__frame, text=self.__last_msg)
        self.__last_msg_label.pack()

        self.__buttons = []
        button = Button(self.__frame, text="Accept", command=self.__accept_request(request))
        button.pack(fill=X, expand=True)
        self.__buttons.append(button)

        button = Button(self.__frame, text="Decline", command=self.__decline_request(request))
        button.pack(fill=X, expand=True)
        self.__buttons.append(button)

        self.__root.mainloop()

    def __accept_request(self, request: str) -> None:
        self.__admin.accept_request(self.__company, request)
        self.__last_msg = "Request accepted"
        self.__last_msg_label.config(text=self.__last_msg)

    def __decline_request(self, request: str) -> None:
        self.__admin.decline_request(self.__company, request)
        self.__last_msg = "Request declined"
        self.__last_msg_label.config(text=self.__last_msg)

