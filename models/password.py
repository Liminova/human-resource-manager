import hashlib

def hash(username: str, password: str) -> str:
    salt = hashlib.sha384(username.encode()).hexdigest()
    hashed_password = hashlib.sha384((password + salt).encode()).hexdigest()
    return hashed_password

def validate(username: str, input_password: str, hashed_password: str) -> bool:
    input_password = hash(username, input_password)
    return input_password == hashed_password