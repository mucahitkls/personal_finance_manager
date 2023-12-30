from app.schemas.user import UserCreate, UserBase, UserInDB
from typing import List, Optional
from app.models.user import User
from app.utils import security, logger
from mongoengine.errors import NotUniqueError, ValidationError, DoesNotExist
from fastapi import HTTPException, status

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


def get_all_users() -> List[UserBase]:
    """
    Retrieves all users from the database.
    Returns a list of UserBase objects representing the users.
    """
    try:
        users = User.objects.all()
        return [UserBase(**user.to_mongo().to_dict()) for user in users]
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")


def get_user_by_username(username: str) -> UserBase | None:
    try:
        db_user = User.objects(username=username).first()
        if db_user:
            return UserBase(**db_user.to_mongo().to_dict())
        else:
            logger.info(f"User not found: {username}")
            return None

    except Exception as e:
        logger.error(f"Error retrieving user by username {username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the user."
        )


def get_user_by_id(user_id: int) -> UserBase | None:
    try:
        db_user = User.objects(id=user_id).first()
        if db_user:
            return UserBase(**db_user.to_mongo().to_dict())
        else:
            logger.info(f"User not found: user_id: {user_id}")
            return None

    except Exception as e:
        logger.error(f"Error retrieving user by user_id: {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the user."
        )


def get_user_by_email(email: str) -> UserBase | None:
    try:
        db_user = User.objects(email=email).first()
        if db_user:
            return UserBase(**db_user.to_mongo().to_dict())
        else:
            logger.info(f"User not found: email: {email}")
            return None
    except Exception as e:
        logger.error(f"Error retrieving user by user mail: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occured while retrieving the user."
        )


def delete_user(user_id: int) -> bool:
    try:
        db_user = User.objects(id=user_id).first()
        if not db_user:
            logger.info(f"User with ID {user_id} not found.")
            return False
        db_user.delete()
        logger.info(f"User with ID {user_id} has been deleted.")
        return True

    except ValidationError as e:
        logger.error(f"Validation Error: Invalid user ID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format."
        )

    except DoesNotExist:
        logger.warning(f"User with ID {user_id} does not exist.")
        return False

    except Exception as e:
        logger.error(f"Unexpected error occurred while deleting user with ID {user_id}.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting the user."
        )


def update_user(user_id: int, user_data: UserCreate) -> Optional[UserBase]:
    try:
        user_in_db = User.objects(id=user_id).first()

        if not user_in_db:
            logger.info(f"User with ID {user_id} not found.")
            return None

        user_in_db.update(
            hashed_password=security.hash_plain_password(user_data.password),
            email=user_data.email,
            username=user_data.username
        )

        logger.info(f"User with ID {user_id} has been updated.")

        updated_user = User.objects(id=user_id).first()
        return UserBase(**updated_user.to_mongo().to_dict())

    except ValidationError as e:
        logger.error(f"Validation Error: {e}")
        # Todo: custom exception needed

    except NotUniqueError as e:
        logger.error(f"Unique Constraint Error: {e}")
        # # Todo: handling cases where the update might violate a unique constraint.

    except Exception as e:
        logger.error(f"Unexpected error occurred while updating user with ID {user_id}")
        # Todo: handle any other unexpected errors
    return None



























