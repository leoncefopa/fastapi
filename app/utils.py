from passlib.context import CryptContext

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hashing(password: str):
    return password_context.hash(password)


def verify(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)
