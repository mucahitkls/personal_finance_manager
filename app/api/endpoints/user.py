import hashlib
from mongoengine.errors import DoesNotExist
from fastapi import APIRouter, HTTPException, status
from jose import JWTError
from app.schemas import user as user_schema
from app.schemas.token import Token
from app.crud import crud_user
from app.models import user as user_model
from app.utils import security, logger

router = APIRouter()
logger = logger.setup_logger()


@router.post("/register", response_model=user_schema.UserBase)
async def create_user(user: user_schema.UserCreate):
    """
    Register a new user.
    This endpoint allows anyone to register a new user with a username, email and password
    It checks if the email and username already exists and, if not, creates a new user.

    Parameters:
        user (UserCreate): The user data transfer object containing the username, email, and password.

    Returns:
        UserBase: The created user's public information.

    Raises:
        HTTPException: 400 error if the user could not be created due to validation or other issues.
    """

    try:
        new_user = crud_user.create_user(user)
        if new_user:
            logger.info(f"New user registered: {new_user.username}")
        else:
            logger.error(f"Failed to register user: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create the user. The username or email might already be in use."
            )
    except Exception as e:
        logger.exception(f"Unexpected error occurred while registering user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.post("/login")
async def login(user: user_schema.UserLogin) -> Token:
    try:
        user_obj = security.authenticate_user(user.username, user.password)
        if not user_obj:
            logger.info(f"Login attempt for username: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = security.create_access_token(data={"sub": user.username})
        logger.info(f"User {user_obj.username} logged in successfully.")
        return Token(access_token=access_token, token_type="bearer")

    except DoesNotExist:
        logger.warning(f"User not found: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    except JWTError as jwt_error:
        logger.error(f"JWT Error: {jwt_error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing login request."
        )

