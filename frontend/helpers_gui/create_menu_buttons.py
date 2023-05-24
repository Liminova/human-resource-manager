import tkinter as tk
from typing import Callable

import customtkinter as ctk

from .global_styling import btn_exit_style, btn_menu_style
from .merge_callable import merge_callable


class MenuButtons:
    """Create a menu with multiple buttons.

    Parameters:
        _master (ctk.CTkFrame): The frame to place the buttons in.
        sub_menu (ctk.CTkFrame): The frame to be destroyed when the menu is closed.
        buttons (tuple[tuple[str, Callable]]): The buttons to be displayed. The first element of the tuple is the text to be displayed on the button, the second element is the command to be executed when the button is clicked.
    """

    def __init__(self, _master: ctk.CTkFrame, sub_menu: ctk.CTkFrame, buttons: dict[str, Callable]):
        self.master = _master
        self.sub_menu = sub_menu
        self.buttons = buttons

    def __clear_sub_menu_frame(self):
        for widget in self.sub_menu.winfo_children():
            widget.destroy()

    def __disable_clicked_enable_other(self, clicked: ctk.CTkButton, other_buttons: list[ctk.CTkButton]):
        clicked.configure(state=tk.DISABLED)
        for button in other_buttons:
            button.configure(state=tk.NORMAL)

    def create(self):
        # contains all the buttons, later used to disable the clicked button and enable the other buttons
        buttons: list[ctk.CTkButton] = []

        # iterate but exclude the last button
        for text, cmd in list(self.buttons.items())[:-1]:
            # create the button
            btn = ctk.CTkButton(master=self.master, text=text, command=cmd, **btn_menu_style)

            # add the button to the list
            buttons.append(btn)

            # place the button

        x = 0.5
        y = 0.1
        for btn in buttons:
            # create a lambda to chain to the button's command
            other_btns = [b for b in buttons if b != btn]

            def disable_clicked_enable_other(a=btn, b=other_btns):
                return self.__disable_clicked_enable_other(a, b)

            # chain the lambda to the button's command
            btn_origin_cmd = btn.cget("command")
            btn_chain_cmd = merge_callable(self.__clear_sub_menu_frame, btn_origin_cmd, disable_clicked_enable_other)
            btn.configure(command=btn_chain_cmd)

            # place the button
            btn.place(relx=x, rely=y, anchor=tk.CENTER)
            y += 0.1

        back_cmd = list(self.buttons.items())[-1][1]

        # create the back button
        back_button = ctk.CTkButton(master=self.master, text="Back", command=back_cmd, **btn_exit_style)
        back_button.place(relx=x, rely=0.9, anchor=tk.CENTER)
