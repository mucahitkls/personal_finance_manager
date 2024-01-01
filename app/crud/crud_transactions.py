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
