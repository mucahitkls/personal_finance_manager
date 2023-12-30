from dotenv import load_dotenv
from logger import setup_logger
import os

logger = setup_logger()

load_dotenv()


def get_data(key: str) -> str | None:
    try:
        value = os.getenv(key)
        if value:
            logger.info(f"{key} value fetched successfully.")
        else:
            logger.error(f"{key} value not found.")
        return value
    except Exception as e:
        logger.error(f"Error while fetching {key} value: {e}")
        return None
