from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Returns a hashed version of the plaintext password

    :param password: The plaintext password to hash
    """
    return context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Given a plaintext password and hashes password, returns True if the password
    matches the hashed password, otherwise returns False.

    :param password: The plaintext password to verify against the hashed password
    :param hashed_password: The hashed password to verify against the plaintext password
    """
    return context.verify(password, hashed_password)
