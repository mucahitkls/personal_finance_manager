from typing import List, Optional
from mongoengine.errors import DoesNotExist
from fastapi import APIRouter, HTTPException, status, Depends
from jose import JWTError
from app.schemas import user as user_schema
from app.schemas import transaction as transaction_schema
from app.schemas.token import Token, TokenData
from app.crud import crud_user
from app.utils import security, logger

router = APIRouter(
    prefix='/transactions',
    tags=['transactions'],
    responses={404: {"description": "Not found"}}
)

logger = logger.setup_logger()

@router.get("/", response_model=List[transaction_schema.TransactionCreate])
async def get_all_transactions():
    pass