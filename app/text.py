from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserBase
from app.utils import security
from logger import setup_logger
from mongoengine.errors import ValidationError, NotUniqueError

logger = setup_logger()

def update_user(user_id: int, user_data: UserCreate) -> Optional[UserBase]:
    """
    Updates an existing user's details in the database.

    Args:
        user_id (int): The ID of the user to update.
        user_data (UserCreate): The updated user data.

    Returns:
        Optional[UserBase]: The updated user's information if the update was successful, None otherwise.
    """
    try:
        user_in_db = User.objects(id=user_id).first()
        if not user_in_db:
            logger.info(f"User with ID {user_id} not found.")
            return None

        # Update the user's details
        user_in_db.update(
            hashed_password=security.hash_plain_password(user_data.password),
            email=user_data.email,
            username=user_data.username
        )
        logger.info(f"User with ID {user_id} has been updated.")

        # Fetch and return the updated user details
        updated_user = User.objects(id=user_id).first()
        return UserBase(**updated_user.to_mongo().to_dict())

    except ValidationError as e:
        logger.error(f"Validation Error: {e}")
        # You might want to handle this with a custom exception or different return value in a real app

    except NotUniqueError as e:
        logger.error(f"Unique Constraint Error: {e}")
        # Handle cases where the update might violate a unique constraint (e.g., username)

    except Exception as e:
        logger.error(f"Unexpected error occurred while updating user with ID {user_id}: {e}")
        # Handle any other unexpected errors

    return None
