from .COLORS import FCOLORS
def loop_til_valid_input(prompt: str, validator: callable) -> None: # type: ignore
    """Takes a prompt and a validator function and keeps asking for input until the validator returns True"""
    user_input = input(prompt)

    # convert to int if possible for payroll input
    try:
        user_input = int(user_input)
    except ValueError:
        pass

    while True:
        try:
            validator(user_input).unwrap() # type: ignore
            break
        except (ValueError, TypeError) as e:
            user_input = input(f"{FCOLORS.RED}{str(e)} Try again:{FCOLORS.END} {prompt}")