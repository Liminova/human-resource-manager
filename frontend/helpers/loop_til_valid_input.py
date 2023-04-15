from .COLORS import FCOLORS


def loop_til_valid_input(prompt: str, validator: callable) -> str:
    """Takes a prompt and a validator function and keeps asking for input until the validator returns True"""
    user_input = input(f"{prompt}, leave blank to cancel: ")
    if user_input == "":
        confirm = input("Are you sure you want to cancel? (Y/n): ")
        if confirm.lower() != "n":
            return "Input cancelled!"
        user_input = input(f"{prompt}, leave blank to cancel: ")
    while True:
        try:
            validator(user_input).unwrap()
            break
        except (ValueError, TypeError) as e:
            user_input = input(f"{FCOLORS.RED}{str(e)} Try again: {FCOLORS.END}")
    return ""
