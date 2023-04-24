import os


def refresh(msg: str) -> str:
    os.system("cls" if os.name == "nt" else "clear")
    print(msg) if msg else None
    return ""
