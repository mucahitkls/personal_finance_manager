from fastapi import APIRouter, HTTPException, status
from app.schemas import user as user_schema
from app.crud import crud_user
from app.models import user as user_model
from app.utils.logger import setup_logger

router = APIRouter()
logger = setup_logger()


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

