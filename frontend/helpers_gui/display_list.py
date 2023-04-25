import tkinter as tk
import customtkinter as ctk
from frontend.helpers_tui import clustering
from frontend.helpers_gui.global_styling import btn_action_style, label_desc_style
from typing import Callable


def display_list(
    _master,
    options: tuple[str],
    returned_idx: list[ctk.IntVar] = [],
    selectable: bool = True,
    page_size: int = 5,
    err_msg: str = "",
    place_row: int = 1,
    place_col: int = 0,
    colspan: int = 2,
    cmd: Callable = lambda: None,
) -> tuple[bool, ctk.CTkFrame]:
    """Create a page with multiple options to choose from. The options are clustered into groups of 5 (by default).

    Parameters:
        _master (tkinter.Tk|tkinter.Toplevel): The parent window.
        options (tuple[str]): The options to be displayed.
        returned_idx (list[ctk.IntVar]): variable to store the index of the selected option, the list is used to pass by reference. Just put a square bracket around the variable when passing it in.
        selectable (bool): Whether the options are selectable or not.
        page_size (int): The number of options to be displayed in a page.
        err_msg (str): The error message to be displayed when there is no option to be displayed.
        place_row (int): The row to place the list in the subwidget, this should be 1 because the first row is reserved for the page indicator.
        place_col (int): The column to place the list in the subwidget, useful if you want to place multiple lists in the same subwidget.
        colspan: depends on the master widget. If the design has x columns, then colspan should be x.
        cmd (Callable): The command to be executed when an option is selected.
    """
    clustered = clustering(options, page_size)
    current_page = 0
    total_page = len(clustered)
    empl_page = ctk.CTkFrame(master=_master)
    empl_page.grid(row=place_row, column=place_col, columnspan=colspan, padx=20, pady=10)
    if total_page == 0:
        ctk.CTkLabel(master=empl_page, text=err_msg, **label_desc_style).grid(row=2, column=0, padx=20, pady=20)
        return False, empl_page

    def __update_empl_page(no_button: str = ""):
        for widget in empl_page.winfo_children():
            widget.destroy()

        ctk.CTkLabel(master=empl_page, text=f"Page {current_page + 1} of {total_page}", **label_desc_style).grid(
            row=0, column=0, columnspan=2, padx=10, pady=20
        )

        for i, option in enumerate(clustered[current_page]):
            if selectable:
                value = i + current_page * page_size
                ctk.CTkRadioButton(master=empl_page, text=option, variable=returned_idx[0], value=value, command=cmd).grid(
                    row=i + 1, column=0, padx=20, columnspan=2, sticky=tk.W
                )
            else:
                ctk.CTkLabel(master=empl_page, text=option, **label_desc_style).grid(
                    row=i + 1, column=0, padx=20, columnspan=2, sticky=tk.W
                )
        btn_prev = ctk.CTkButton(master=empl_page, text="<", command=__prev_page, **btn_action_style)
        btn_prev.grid(row=page_size + 1, column=0, padx=20, pady=20)
        if no_button == "prev":
            btn_prev.configure(state=tk.DISABLED)
        btn_next = ctk.CTkButton(master=empl_page, text=">", command=__next_page, **btn_action_style)
        btn_next.grid(row=page_size + 1, column=1, padx=20, pady=20)
        if no_button == "next":
            btn_next.configure(state=tk.DISABLED)

    def __prev_page():
        nonlocal current_page
        # if current_page > 0:
        #     current_page -= 1
        #     __update_empl_page()

        if current_page > 0:
            current_page -= 1
            __update_empl_page(no_button=("prev" if current_page == 0 else ""))

    def __next_page():
        nonlocal current_page
        if current_page + 1 < total_page:
            current_page += 1
            __update_empl_page(no_button=("next" if current_page + 1 == total_page else ""))

    __update_empl_page()

    return True, empl_page
