from .clrscr import clrscr
from .clustering import clustering
from .COLORS import FCOLORS


def listing(title: str, entries: tuple[str]) -> None:
    """Prints a list of entries in a nice format"""

    clusters = clustering(entries, 9)
    current_cluster = 0

    if not clusters:
        return

    while True:
        clrscr()
        print(f"--- {title} ---")
        entries = clusters[current_cluster]

        # options in current cluster
        for index, entry in enumerate(entries):
            print(f"{index+1}. {entry}")

        # navigation
        print(f"--- Page {current_cluster+1} of {len(clusters)} ---")

        user_choice = input(
            "{}[P]{}revious, {}[N]{}ext, enter a number to jump to a page or press enter to go back: ".format(
                FCOLORS.YELLOW, FCOLORS.END, FCOLORS.YELLOW, FCOLORS.END
            )
        )
        match user_choice.upper():
            case "":
                return
            case "P":
                if current_cluster == 0:
                    continue
                current_cluster -= 1
            case "N":
                if current_cluster == len(clusters) - 1:
                    continue
                current_cluster += 1
            case _:  # choose a page (1-(entries/9))
                try:
                    user_choice = int(user_choice)
                    if user_choice not in range(1, len(clusters) + 1):
                        raise ValueError
                    current_cluster = user_choice - 1
                except:
                    continue
