from .COLORS import FCOLORS


def __filter_colors(string: str) -> str:
    for color in FCOLORS.__dict__.values():
        if not isinstance(color, str):
            continue
        string = string.replace(color, "")
    return string


def print_menu(title: str, entries: list[str]) -> None:
    _entries = [__filter_colors(entry) for entry in entries] + [__filter_colors(title)]
    longest_entry = len(max(_entries, key=len)) + 9
    print(FCOLORS.GREEN + "╔" + "═" * (longest_entry - 1) + "╗" + FCOLORS.END)
    border = FCOLORS.GREEN + "║" + FCOLORS.END
    print(border + " " * (longest_entry - 1) + border)

    if len(title) < longest_entry:
        l_padding = " " * int(round(((longest_entry - len(title)) // 2), 0) - 4)
        r_padding = " " * (longest_entry - len(title) - len(l_padding) - 9)
        title = l_padding + title + r_padding
    title = " " * 4 + title + " " * 4
    print(border + title + border)
    print(border + " " * (longest_entry - 1) + border)
    print(border + "-" * (longest_entry - 1) + border)
    print(border + " " * (longest_entry - 1) + border)

    for entry in entries:
        if len(entry) < longest_entry:
            index = entry[0 : entry.index("]") + 1]
            entry = entry.replace(index, f"{FCOLORS.YELLOW}{index}{FCOLORS.END}")
            entry = entry + " " * (longest_entry - len(entry))
        entry = "    " + entry + "    "
        print(border + entry + border)

    print(border + " " * (longest_entry - 1) + border)
    print(FCOLORS.GREEN + "╚" + "═" * (longest_entry - 1) + "╝" + FCOLORS.END)


def get_user_option_from_menu(title: str, menu_list: list[str]) -> int:
    """Takes a list of menu entries and returns the user's choice | returns -1 if user cancels"""
    print_menu(title, menu_list)
    user_choice = 0
    while True:
        try:
            user_choice = input("Enter your choice: ")
            if user_choice == "":
                return -1
            user_choice = int(user_choice)
            if user_choice not in range(1, len(menu_list) + 1):
                raise ValueError
            return user_choice
        except KeyboardInterrupt:
            exit()
        except:
            continue
