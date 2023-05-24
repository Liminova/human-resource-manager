from .COLORS import FCOLORS


def __filter_colors(string: str) -> str:
    for color in FCOLORS.__dict__.values():
        if not isinstance(color, str):
            continue
        string = string.replace(color, "")
    return string


def print_menu(title: str, entries: list[str], padding: int = 5) -> None:
    _entries = [__filter_colors(entry) for entry in entries] + [__filter_colors(title)]
    border = FCOLORS.GREEN + "║" + FCOLORS.END
    longest_entry = len(max(_entries, key=len)) + padding * 2
    data_to_print = []

    data_to_print.append(FCOLORS.GREEN + "╔" + ("═" * longest_entry) + "╗" + FCOLORS.END)
    data_to_print.append(border + " " * longest_entry + border)

    title_left_padding = (longest_entry - len(title)) // 2
    title_right_padding = longest_entry - title_left_padding - len(title)
    title = (" " * title_left_padding) + title + (" " * title_right_padding)

    data_to_print.append(border + title + border)
    data_to_print.append(border + " " * longest_entry + border)
    data_to_print.append(border + "-" * longest_entry + border)
    data_to_print.append(border + " " * longest_entry + border)

    for entry in entries:
        left_padding = " " * padding
        right_padding = " " * (longest_entry - padding - len(entry))
        entry = FCOLORS.YELLOW + entry[0 : entry.index("]") + 1] + FCOLORS.END + entry[entry.index("]") + 1 :]
        data_to_print.append(border + left_padding + entry + right_padding + border)

    data_to_print.append(border + " " * longest_entry + border)
    data_to_print.append(FCOLORS.GREEN + "╚" + ("═" * longest_entry) + "╝" + FCOLORS.END)

    print("\n".join(data_to_print))


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
