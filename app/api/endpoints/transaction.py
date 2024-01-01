from app.schemas import transaction as transaction_schema
from app.crud import crud_transactions
from typing import List, Optional
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from fastapi import APIRouter, HTTPException, status, Depends
from jose import JWTError
from app.schemas.token import Token, TokenData
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


@router.get("/{transaction_id}", response_model=transaction_schema.TransactionBase)
async def get_transaction(transaction_id: int) -> Optional[transaction_schema.TransactionBase]:
    try:
        db_transaction = crud_transactions.get_transaction_by_id(transaction_id=transaction_id)
        return db_transaction
    except DoesNotExist:
        logger.warning(f"Transaction not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    except Exception as e:
        logger.error(f"Unexpected error occurred while checking transaction by id {transaction_id}: {e}")


@router.delete("/{transaction_id}", response_model=transaction_schema.TransactionBase)
async def delete_transaction(transaction_id: int) -> transaction_schema.TransactionBase | False:
    try:
        transaction_to_delete = crud_transactions.delete_transaction_by_id(transaction_id=transaction_id)
        if not transaction_to_delete:
            logger.info(f"Transaction with ID {transaction_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found."
            )
        if transaction_to_delete:
            logger.info(f"Transaction with id: {transaction_id} deleted successfully")
            return transaction_to_delete

        else:
            logger.warning(
                f"Failed to delete transaction with ID {transaction_id}. Transaction may not exists or deleted already.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found or already deleted"
            )
    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.error(f"Unexpected error occurred while deleting transaction with ID {transaction_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting the transaction."
        )

@router.put("/{transaction_id}", response_model=transaction_schema.TransactionBase)
async def update_transaction(transaction_id: int, transactoin_data: transaction_schema.TransactionCreate) -> transaction_schema.TransactionBase | bool:
    try:
        updated_transaction = crud_transactions.update_transaction(transaction_id=transaction_id, transaction_data=transactoin_data)

    except Exception as e:
        pass