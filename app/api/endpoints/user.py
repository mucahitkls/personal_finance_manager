from fastapi import APIRouter, HTTPException
from app.schemas import user as user_schema
from app.models import user as user_model
from app.crud import crud_user

router = APIRouter()


@router.post("/register", response_model=user_schema.UserInDB)
async def create_user(user: user_schema.UserCreate):
    """
    Register a new user.
    This endpoint allows anyone to register a new user with a username, email and password
    It checks if the email and username already exists and, if not, creates a new user.

    :param user:
    :return:
    """
    user = user_model.User()
    created_user = crud_user.create_user(user)
