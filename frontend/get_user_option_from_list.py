from .COLORS import FCOLORS, BCOLORS
from .clrscr import clrscr
from .clustering import clustering


def get_user_option_from_list(title: str, options: list[str]) -> int:
    """Takes a list of options and returns the users choice's index"""

    clusters = clustering(options, 9)
    current_cluster = 0
    while True:
        clrscr()
        print(f"--- {title} ---")
        entries = clusters[current_cluster]

        # options in current cluster
        for index, entry in enumerate(entries):
            print(f"{FCOLORS.YELLOW}[{index+1}]{FCOLORS.END} {entry}")

        # navigation
        print(f"--- Page {current_cluster+1} of {len(clusters)} ---")

        user_choice = input("{}[P]{}revious, {}[N]{}ext, enter a number to choose an entry or press enter to go back: ".format(FCOLORS.YELLOW, FCOLORS.END, FCOLORS.YELLOW, FCOLORS.END))
        match user_choice.upper():
            case "":
                return -1
            case "P":
                if current_cluster == 0:
                    continue
                current_cluster -= 1
                break
            case "N":
                if current_cluster == len(clusters) - 1:
                    continue
                current_cluster += 1
                break
            case _:  # choose an entry from the current cluster (1-9)
                try:
                    user_choice = int(user_choice)
                    if user_choice not in range(1, 10):
                        raise ValueError
                    clrscr()
                    return (current_cluster * 9) + (user_choice - 1)
                except KeyboardInterrupt:
                    exit()
                except:
                    user_choice = input(f"{FCOLORS.RED}Invalid choice! Try again: {FCOLORS.END}")
                    continue

