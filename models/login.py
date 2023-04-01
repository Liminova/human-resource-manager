class Login:
    def __init__(self) -> None:
        self.__username = ""
        self.__password = ""
        self.__role = ""

    @property
    def username(self) -> str:
        return self.__username

    @property
    def password(self) -> str:
        return self.__password

    @property
    def role(self) -> str:
        return self.__role

    def set_username(self, username: str = "") -> Result[Self, str]:
        self.__username = username
        return Ok(self) if username else Err("Username cannot be empty!")

    def set_password(self, password: str = "") -> Result[Self, str]:
        self.__password = password
        return Ok(self) if password else Err("Password cannot be empty!")

    def set_role(self, role: str = "") -> Result[Self, str]:
        self.__role = role
        return Ok(self) if role else Err("Role cannot be empty!")

    def __str__(self) -> str:
        data = textwrap.dedent(f"""\
            - Username: {self.__username}
            - Password: {self.__password}
            - Role: {self.__role}
        """)
        return data







