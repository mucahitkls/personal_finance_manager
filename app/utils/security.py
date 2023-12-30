"""
This module handles user authentication for the FastAPI application, including password verification,
token generation, and user authentication based on tokens.

It utilizes the Passlib library for password hashing and the python-jose library for creating and verifying JWT tokens.
"""


from passlib.context import CryptContext
from typing import Optional, Any
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from app.models.user import User
from app.schemas.user import UserInDB
from app.schemas.token import TokenData
from utilities import get_data
from logger import setup_logger

logger = setup_logger()

SECRET_KEY = get_data("SECRET_KEY")
ALGORITHM = get_data("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = get_data("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_plain_password(password: str) -> str:
    """
    Hashes a plain text password using bcrypt
    Parameters:
        password (str): The plain text password to hash.
    Returns:
        str: The hashed password.
    """
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Error when hashing password: {e}")


def verify_password(plain_text_password: str, hashed_password: str):
    """
    Verify a password against a hashed version.
    :param plain_text_password:
    :param hashed_password:
    :return:
    """

    return pwd_context.verify(plain_text_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a JWT access token.
    :param data: The data to encode in the token (e.g., the username)
    :param expires_delta: (Optional[timedelta], optional): The time delta in which the token will expire.
    :return: str: The encoded JWT token
    """

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def decode_token(token: str) -> Optional[dict]:
    """
    Decodes a JWT token.
    :param token: The JWT token to decode.
    :return: The decoded token data, or None if the token is invalid.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def authenticate_user(username: str, password: str) -> bool | Any:
    """
    Authenticate a user by username and password.
    :param username:
    :param password:
    :return:
    """
    user = User.objects(username=username).first()
    if not user:
        return False
    if not verify_password(plain_text_password=password, hashed_password=user.hashed_password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:

    """
    Retrieve the current user based on the JWT token.

    Parameters:
        token(str): The JWT token to authenticate.

    Raises:
        HTTPException: 401 error if the token is invalid or the user does not exist.

    Returns:
         UserInDB: The authenticated User object

    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token=token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = User.objects(username=token_data.username).first()
    if user is None:
        raise credentials_exception
    return user
