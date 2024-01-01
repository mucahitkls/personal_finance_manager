from typing import List, Optional
from mongoengine.errors import DoesNotExist
from fastapi import APIRouter, HTTPException, status, Depends
from jose import JWTError
from app.schemas import user as user_schema
from app.schemas import transaction as transaction_schema
from app.schemas.token import Token, TokenData
from app.crud import crud_user
from app.crud import crud_transactions
from app.utils import security, logger
from typing import List, Optional
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from fastapi import APIRouter, HTTPException, status, Depends
from jose import JWTError
from app.models.user import User
from app.schemas import user as user_schema
from app.schemas.token import Token, TokenData
from app.crud import crud_user
from app.utils import security, logger

router = APIRouter(
    prefix='/transactions',
    tags=['transactions'],
    responses={404: {"description": "Not found"}}
)

logger = logger.setup_logger()


@router.get("/", response_model=List[transaction_schema.TransactionBase])
async def get_all_transactions(current_user: TokenData = Depends(security.get_current_active_admin)) -> Optional[
    List[transaction_schema.TransactionBase]]:
    try:
        transactions = crud_transactions.get_all_transactions()
        if transactions:
            return transactions
        else:
            logger.warning(f"No transaction found")
            return []
    except DoesNotExist as e:
        logger.warning(f"Transactions not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transactions not found."
        )

    except JWTError as jwt_error:
        logger.error(f"JWT Error: {jwt_error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing get transactions request."
        )

    except Exception as e:
        logger.error(f"Unexpected error occurred while retrieving transactions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
