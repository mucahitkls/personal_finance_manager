from typing import List, Optional
from mongoengine.errors import DoesNotExist
from fastapi import APIRouter, HTTPException, status
from jose import JWTError
from app.schemas import user as user_schema
from app.schemas.token import Token
from app.crud import crud_user
from app.utils import security, logger

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404: {"description": "Not found"}}
)

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
    """
            Authenticate a user and provide an access token for future requests.
            This endpoint verifies the user's credentials and, if valid, generates a new access token for the user.

            Args:
                user (UserLogin): The user's login information including username and password.

            Raises:
                HTTPException: 401 error if the username or password is incorrect.

            Returns:
                Token: An object containing the access token and token type.
    """

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


@router.get("/", response_model=List[user_schema.UserBase])
async def read_users():
    try:
        users = crud_user.get_all_users()
        return users
    except DoesNotExist:
        logger.warning(f"Users not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users not found"
        )
    except JWTError as jwt_error:
        logger.error(f"JWT Error: {jwt_error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing login request."
        )
    except Exception as e:
        logger.error(f"Error occurred while processing getting users: {e}")


@router.get("/{user_id}", response_model=user_schema.UserBase)
async def read_user(user_id: int):
    try:
        user = crud_user.get_user_by_id(user_id=user_id)
        return user
    except DoesNotExist:
        logger.warning(f"User not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    except Exception as e:
        logger.error(f"Error occurred while processing getting user: {e}")


@router.delete("/{user_id}", response_model=user_schema.UserBase)
async def delete_user(user_id: int) -> Optional[user_schema.UserBase]:
    """
        Deletes a user from the database by their user ID.

        Parameters:
            user_id (int): The ID of the user to delete.

        Returns:
            Optional[user_schema.UserBase]: The deleted user's information if the operation was successful, None otherwise.

        Raises:
            HTTPException: With appropriate status code and detail message when errors occur.
    """
    try:
        db_user = crud_user.get_user_by_id(user_id=user_id)
        if not db_user:
            logger.info(f"User with ID {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        if crud_user.delete_user(user_id=user_id):
            logger.info(f"User with ID {user_id} has been deleted.")
            return db_user

        else:
            logger.warning(f"Failed to delete user with ID {user_id}. User may not exist.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or already deleted."
            )

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.error(f"Unexpected error occurred while deleting user with ID {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting the user."
        )


@router.put("/{user_id}", response_model=user_schema.UserBase)
async def update_user(user_id: int, user: user_schema.UserCreate) -> Optional[user_schema.UserBase]:


    pass
