import tkinter as tk
from typing import Callable

import customtkinter as ctk

from frontend.helpers_gui.global_styling import btn_action_style, label_desc_style
from frontend.helpers_tui import clustering


def display_list(
    _master,
    err_msg: str,
    options: tuple[str],
    place: tuple[int, int] = (1, 0),
    returned_idx: list[ctk.IntVar] = [],
    page_size: int = 5,
    colspan: int = 2,
    cmd: Callable = lambda: None,
    **kwargs,
) -> ctk.CTkFrame:
    """Create a page with multiple options to choose from. The options are clustered into groups of 5 (by default).

    Parameters:
        _master (tkinter.Tk|tkinter.Toplevel): The parent window.
        options (tuple[str]): The options to be displayed.
        returned_idx (list[ctk.IntVar]): variable to store the index of the selected option, the list is used to pass by reference. Just put a square bracket around the variable when passing it in.
        selectable (bool): Whether the options are selectable or not.
        page_size (int): The number of options to be displayed in a page.
        err_msg (str): The error message to be displayed when there is no option to be displayed.
        place: The row/column to place the widget in the parent window.
        colspan: int result of x/y; x: # of cols in the parent window, y: # how many cols the widget should occupy. E.g. colspan=2 means the widget will occupy 2 cols in the parent window.
        cmd (Callable): The command to be executed when an option is selected.
        **kwargs: The keyword arguments to be passed to the child widgets `grid` method, created from the _master
    """

    selectable = False
    if len(returned_idx) > 0:
        selectable = True

    # add padding to **kwargs if not specified
    if "padx" not in kwargs:
        kwargs["padx"] = 20
    if "pady" not in kwargs:
        kwargs["pady"] = 20

    clustered = clustering(options, page_size)
    current_page = 0
    total_page = len(clustered)
    empl_page = ctk.CTkFrame(master=_master)
    empl_page.grid(row=place[0], column=place[1], columnspan=colspan, **kwargs)
    if total_page == 0:
        ctk.CTkLabel(master=empl_page, text=err_msg, **label_desc_style).grid(
            row=2, column=0, padx=20, pady=20, columnspan=colspan
        )
        return empl_page

    def __update_empl_page():
        nonlocal selectable, current_page, total_page
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
                ctk.CTkLabel(master=empl_page, text=option).grid(row=i + 1, column=0, padx=20, columnspan=2, sticky=tk.W)

        btn_prev = ctk.CTkButton(master=empl_page, text="<", command=__prev_page, **btn_action_style)
        btn_prev.grid(row=page_size + 1, column=0, padx=20, pady=20)
        btn_prev.configure(state=(tk.DISABLED if current_page == 0 else tk.NORMAL))

        btn_next = ctk.CTkButton(master=empl_page, text=">", command=__next_page, **btn_action_style)
        btn_next.grid(row=page_size + 1, column=1, padx=20, pady=20)
        btn_next.configure(state=(tk.DISABLED if current_page + 1 == total_page else tk.NORMAL))

    def __prev_page():
        nonlocal current_page
        if current_page > 0:
            current_page -= 1
            __update_empl_page()

    def __next_page():
        nonlocal current_page
        if current_page + 1 < total_page:
            current_page += 1
            __update_empl_page()

    __update_empl_page()

    return empl_page
