from .COLORS import FCOLORS

def loop_til_valid_input(prompt: str, validator: callable) -> None:
    """Takes a prompt and a validator function and keeps asking for input until the validator returns True"""
    user_input = input(prompt)
    while True:
        try:
            validator(user_input).unwrap()
            break
        except (ValueError, TypeError) as e:
            user_input = input(f"{FCOLORS.RED}{str(e)} Try again:{FCOLORS.END} {prompt}")