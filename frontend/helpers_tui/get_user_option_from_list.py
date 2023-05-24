from .clrscr import clrscr
from .clustering import clustering
from .COLORS import FCOLORS


def get_user_option_from_list(title: str, options: tuple[str]) -> int:  # type: ignore
    """Takes a list of options and returns the users choice's index | returns -1 if options empty, -2 if user cancels"""

    if len(options) == 0:
        return -1

    # split options into clusters of 9
    clusters = clustering(options, 9)
    current_cluster = 0
    while True:
        clrscr()
        print(f"--- {title} ---")
        entries = clusters[current_cluster]

        # print entries in the current cluster
        for index, entry in enumerate(entries):
            print(f"{FCOLORS.YELLOW}[{index+1}]{FCOLORS.END} {entry}")

        # navigation bar
        print(f"--- Page {current_cluster+1} of {len(clusters)} ---")

        user_choice = input(
            "{}[P]{}revious, {}[N]{}ext, enter a number to choose an entry or press enter to go back: ".format(
                FCOLORS.YELLOW, FCOLORS.END, FCOLORS.YELLOW, FCOLORS.END
            )
        )
        match user_choice.upper():
            case "":
                return -2
            case "P":
                if current_cluster == 0:
                    continue
                current_cluster -= 1
            case "N":
                if current_cluster == len(clusters) - 1:
                    continue
                current_cluster += 1
            case _:  # assume user entered a number
                try:
                    user_choice = int(user_choice)
                    if user_choice not in range(1, len(entries) + 1):
                        raise ValueError
                    clrscr()
                    return (current_cluster * 9) + (user_choice - 1)
                except KeyboardInterrupt:
                    exit()
                except:
                    user_choice = input(f"{FCOLORS.RED}Invalid choice! Try again: {FCOLORS.END}")
                    continue
