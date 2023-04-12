from .COLORS import FCOLORS
def loop_til_valid_input(prompt: str, validator: callable) -> str: # type: ignore
    """Takes a prompt and a validator function and keeps asking for input until the validator returns True"""
    user_input = input(f"{prompt}, leave blank to cancel: ")
    if user_input == "":
        return "Input cancelled!"
    while True:
        try:
            validator(user_input).unwrap() # type: ignore
            break
        except (ValueError, TypeError) as e:
            user_input = input(f"{FCOLORS.RED}{str(e)} Try again:{FCOLORS.END} {prompt}")
    return ""