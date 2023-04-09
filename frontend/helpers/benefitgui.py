# GUI for the benefit system
# NOTE for Rylie: I'm not sure if each function (benefit, attendance, department...) should be in a seperate file and defined as a class? 
# Also not sure about where this file should be located.
# Pretty shit atm, pls guide me through this :c 

import customtkinter
from customtkinter import *
from models import BenefitPlan
from typing import List, Tuple, Callable, Any

class BenefitGUI:
    def __init__(self, company: Company):
        self.__company = company
        self.__benefits = company.benefits

    def start(self) -> Tuple[bool, str]:
        self.__root = Tk()
        self.__root.title("Benefit Plan Management")
        self.__root.geometry("500x500")
        self.__root.resizable(False, False)

        self.__frame = Frame(self.__root)
        self.__frame.pack(fill=BOTH, expand=True)

        self.__main_menu = [
            ("Add benefit plan", self.__add),
            ("Apply benefit plan to employee", self.__apply),
            ("Remove benefit plan", self.__remove),
            ("Update benefit plan", self.__update),
            ("View benefit plan", self.__view),
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
        for prompt, _ in self.__input_fields:
            entry = Entry(self.__frame)
            entry.pack(fill=X, expand=True)
            self.__input_entries.append(entry)

        self.__buttons = []
        for text, command in [
            ("Add", self.__add_benefit),
            ("Back", self.__back),
        ]:
            button = Button(self.__frame, text=text, command=command)
            button.pack(fill=X, expand=True)
            self.__buttons.append(button)

    def __set_name(self, name: str) -> None:
        self.__name = name

    def __set_description(self, description: str) -> None:
        self.__description = description

    def __set_cost(self, cost: str) -> None:
        self.__cost = cost

    def __add_benefit(self) -> None:
        for entry, (prompt, setter) in zip(self.__input_entries, self.__input_fields):
            try:
                setter(entry.get())
            except ValueError:
                self.__last_msg = f"Invalid input for {prompt}"
                self.__last_msg_label["text"] = self.__last_msg
                return

        benefit = BenefitPlan()
        benefit.set_name(self.__name)
        benefit.set_description(self.__description)
        benefit.set_cost(self.__cost)
        self.__benefits.append(benefit)

        self.__last_msg = "Benefit plan added!"
        self.__last_msg_label["text"] = self.__last_msg

    def __apply(self) -> None:
        pass

    def __remove(self) -> None:
        pass

    def __update(self) -> None:
        pass

    def __view(self) -> None:
        pass

    def __exit(self) -> None:
        self.__root.destroy()

    def __back(self) -> None:
        self.__root.destroy()
        self.start()


