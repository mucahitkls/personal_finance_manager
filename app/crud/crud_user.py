from app.schemas.user import UserCreate, UserBase
from app.models.user import User
from app.utils import security, logger
from mongoengine.errors import NotUniqueError, ValidationError
logger = logger.setup_logger()


def create_user(user: UserCreate) -> UserBase | None:
    """
    Creates a new user in the database with hashed password.

    Parameter:
        user(UserCreate): The user data transfer object containing the username, email, and password.

    Returns:
        UserBase: The created user's public information or None if creation failed.

    """

    try:
        hashed_pwd = security.hash_plain_password(user.password)
        db_user = User(username=user.username, email=user.email, hashed_password=hashed_pwd)
        db_user.save()
        logger.info(f"User {user.username} created successfully.")
        return UserBase(username=user.username, email=user.email)
    except NotUniqueError as e:
        logger.error(f"Attempt to create a duplicate user {user.username}: {e}")
    except ValidationError as e:
        logger.error(f"Validation error while creating user {user.username}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while creating user {user.username}: {e}")

    return None

