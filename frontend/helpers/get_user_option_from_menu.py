from .COLORS import FCOLORS

def print_menu(title: str, entries: list[str]) -> None:
    longest_entry = len(max(entries, key=len)) + 9

    print(FCOLORS.GREEN + "╔" + "═" * (longest_entry - 1) + "╗" + FCOLORS.END)
    border = FCOLORS.GREEN + "║" + FCOLORS.END
    print(border + " " * (longest_entry - 1) + border)

    if len(title) < longest_entry:
        l_padding = " " * int(round(((longest_entry - len(title)) // 2), 0) - 4)
        r_padding = " " * (longest_entry - len(title) - len(l_padding) - 9)
        title = l_padding + title + r_padding
    title = " "*4 + title + " "*4
    print(border + title + border)
    print(border + " " * (longest_entry - 1) + border)
    print(border + "-" * (longest_entry - 1) + border)
    print(border + " " * (longest_entry - 1) + border)

    for entry in entries:
        if len(entry) < longest_entry:
            index = entry[0:entry.index("]")+1]
            entry = entry.replace(index, f"{FCOLORS.YELLOW}{index}{FCOLORS.END}")
            entry = entry + " " * (longest_entry - len(entry))
        entry = "    " + entry + "    "
        print(border + entry + border)

    print(border + " " * (longest_entry - 1) + border)
    print(FCOLORS.GREEN + "╚" + "═" * (longest_entry - 1) + "╝" + FCOLORS.END)

def get_user_option_from_menu(
        title: str,
        menu_list: list[str],
) -> int:
    """Takes a list of menu entries and returns the user's choice"""
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
