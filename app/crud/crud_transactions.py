from app.schemas.user import UserCreate, UserBase, UserInDB
from app.schemas.transaction import Transaction, TransactionCreate, TransactionBase
from typing import List, Optional
from app.models.user import User
from app.models.transaction import Transaction
from app.utils import security, logger
from mongoengine.errors import NotUniqueError, ValidationError, DoesNotExist
from fastapi import HTTPException, status

logger = logger.setup_logger()


def get_all_transactions() -> List[TransactionBase]:
    try:
        transactions = Transaction.objects().all()
        return [TransactionBase(**transaction.to_mongo().to_dict()) for transaction in transactions]
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")


def get_transaction_by_id(transaction_id) -> Optional[TransactionBase]:
    try:
        db_transaction = Transaction.objects(id=transaction_id).first()
        if db_transaction:
            return TransactionBase(**db_transaction.to_mongo().to_dict())
        else:
            logger.info(f"Transaction not found with ID {transaction_id}")
            return None

    except ValidationError as e:
        logger.error(f"Error validating while retrieving transaction with ID {transaction_id}: {e}")

    except Exception as e:
        logger.error(f"Error retrieving transaction by id {transaction_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error while retrieving the transaction."
        )


def delete_transaction_by_id(transaction_id: int) -> TransactionBase | bool:
    try:
        transaction_to_delete = get_transaction_by_id(transaction_id=transaction_id)
        if not transaction_to_delete:
            logger.warning(f"No transaction found")
            return False

        transaction_to_delete.delete()
        logger.info(f"Transaction with ID: {transaction_id} deleted successfully.")
        return TransactionBase(**transaction_to_delete.to_mongo().to_dict())

    except ValidationError as e:
        logger.error(f"Validation error for transaction with id: {transaction_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid transaction id format"
        )
    except Exception as e:
        logger.error(f"Unexpected error occurred while deleting transaction with id: {transaction_id}: {e}")


def update_transaction(transaction_id: int, transaction_data: TransactionCreate) -> TransactionBase | bool:
    try:
        transaction_to_update = get_transaction_by_id(transaction_id=transaction_id)
        if not transaction_to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )

        transaction_to_update.update(
            amount = transaction_data.amount,
            description=transaction_data.description,
            date=transaction_data.date
        )

        logger.info(f"Transaction updated successfully.")
        return TransactionBase(**transaction_to_update.to_mongo().to_dict())

    except ValidationError as e:
        logger.error(f"Validation Error: {e}")
        raise e
    except NotUniqueError as e:
        logger.error(f"Unique Constraint Error: {e}")
        raise e

    except Exception as e:
        logger.error(f"Unexpected error occurred while updating transaction with id: {transaction_id}: {e}")

    return False