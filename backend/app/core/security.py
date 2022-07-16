import time
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from app.core.config import settings
from app.schemas.responses import AccessTokenResponse

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
ACCESS_TOKEN_EXPIRE_SECONDS = 30 * 60  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
REFRESH_TOKEN_EXPIRE_SECONDS = 60 * 24 * 7 * 60  # 7 days
ALGORITHM = "HS256"


context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTTokenPayload(BaseModel):
    sub: str | int
    refresh: bool
    issued_at: int
    expires_at: int


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


def create_jwt_token(subject: str | int, exp_secs: int, refresh: bool):
    """Creates a jwt access or refresh token for user


    Args:
        subject: anything unique to the user (id, email, etc.)
        exp_secs: expire time in seconds
        refresh: if True, this is a refresh token
    """

    issued_at = int(time.time())
    expires_at = issued_at + exp_secs

    to_encode: dict[str, int | str | bool] = {
        "issued_at": issued_at,
        "expires_at": expires_at,
        "sub": subject,
        "refresh": refresh,
    }
    encoded_jwt = jwt.encode(to_encode, key=settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expires_at, issued_at


def generate_access_token_response(subject: str | int):
    """Generate tokens & return TokenResponse"""
    access_token, expires_at, issued_at = create_jwt_token(
        subject, ACCESS_TOKEN_EXPIRE_SECONDS, refresh=False
    )
    refresh_token, refresh_expires_at, refresh_issued_at = create_jwt_token(
        subject, REFRESH_TOKEN_EXPIRE_SECONDS, refresh=True
    )
    return AccessTokenResponse(
        token_type="Bearer",
        access_token=access_token,
        expires_at=expires_at,
        issued_at=issued_at,
        refresh_token=refresh_token,
        refresh_token_expires_at=refresh_expires_at,
        refresh_token_issued_at=refresh_issued_at,
    )
